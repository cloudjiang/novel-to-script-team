#!/usr/bin/env python3
"""
generate_image.py — 调用 nano banana API 生成图片（支持并行 + 依赖重试）

用法：
  # 单条提示词
  python scripts/generate_image.py --prompt "画一只龙虾" --output-dir /tmp/test

  # 从 md 文件批量生成（自动依赖分析 + 并行）
  python scripts/generate_image.py --prompt-file assets/character-prompts.md --output-dir images/characters --prefix char

  # 带参考图
  python scripts/generate_image.py --prompt "参考风格" --reference-image ref.png --output-dir /tmp/test

  # 自定义并行数和超时
  python scripts/generate_image.py --prompt-file assets/scene-prompts.md --output-dir images/scenes --prefix scene --max-workers 4 --timeout 360
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("错误：需要 requests 库。请运行: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from .env_config import chat_completions_url, get_optional_env, get_required_env, load_env
except ImportError:
    from env_config import chat_completions_url, get_optional_env, get_required_env, load_env

DEFAULT_IMAGE_MODEL = "gemini-3.1-flash-image-preview"


def load_image_api_config():
    env = load_env()
    api_key = get_required_env(env, "NANO_BANANA_API_KEY")
    api_url = chat_completions_url(get_required_env(env, "NANO_BANANA_BASE_URL"))
    model = get_optional_env(env, "NANO_BANANA_IMAGE_MODEL", DEFAULT_IMAGE_MODEL)
    return api_key, api_url, model


def encode_image_to_base64(image_path):
    """将本地图片编码为 base64 data URI"""
    path = Path(image_path)
    if not path.exists():
        print(f"  ⚠ 参考图不存在: {image_path}", file=sys.stderr)
        return None

    suffix = path.suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}
    mime = mime_map.get(suffix, "image/png")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def clean_prompt_content(raw_content):
    """清洗 markdown 格式符号，保留描述性内容。

    保留：出图布局、多角度布局、对应分镜、出图视角、所有描述段落
    去除：纯标签行（**提示词**：）、markdown 格式（**、---）、尾部元数据
    """
    lines = raw_content.split('\n')
    cleaned = []
    # 尾部元数据关键词：遇到这些开头的行就停止（它们不是图片描述）
    tail_meta_patterns = ['文档完成日期', '版本：', '版本:', '下一步：', '下一步:']

    for line in lines:
        stripped = line.strip()

        # 跳过分隔线
        if stripped == '---':
            continue

        # 跳过纯标签行
        if stripped in ('**提示词**：', '**提示词**:'):
            continue

        # 跳过参考图/参考角色/关联角色标记行（由脚本单独处理或仅作元数据）
        if re.match(r'^\*\*(参考角色|参考图|关联角色)\*\*', stripped):
            continue

        # 跳过所在场景标记行（由脚本单独处理）
        if re.match(r'^\*\*所在场景\*\*', stripped):
            continue

        # 跳过尾部元数据行
        clean_stripped = stripped.replace('**', '')
        if any(clean_stripped.startswith(pat) for pat in tail_meta_patterns):
            continue

        # 去除 markdown 加粗符号
        cleaned_line = stripped.replace('**', '')

        if cleaned_line:
            cleaned.append(cleaned_line)

    return '\n'.join(cleaned)


def extract_style_declaration(filepath):
    """从 md 文件头部提取视觉风格声明"""
    path = Path(filepath)
    if not path.exists():
        return ""

    text = path.read_text(encoding="utf-8")
    match = re.search(r'\*\*(?:视觉风格声明|整体风格声明)\*\*[：:]\s*(.+?)(?:\n\n|\n---|\n##|\n###|$)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def extract_references(raw_content):
    """提取所有参考图标记，支持多张参考图。

    支持格式：
      **参考角色**：人物 01a      → [("人物", "01a")]
      **参考图**：场景 01          → [("场景", "01")]
      **参考图**：人物 02          → 可与上面并存，返回多个
      **参考图**：人物 01a, 场景 03 → [("人物", "01a"), ("场景", "03")]
    返回 [(类型, 编号), ...] 列表，无参考时返回空列表
    """
    refs = []
    # 匹配所有 **参考图** 行（整行提取后拆分逗号）
    for line_match in re.finditer(r'\*\*参考图\*\*[：:]\s*(.+)', raw_content):
        line_content = line_match.group(1)
        for item_match in re.finditer(r'(人物|场景|物品|帧图)\s*(\w+)', line_content):
            ref = (item_match.group(1), item_match.group(2).strip())
            if ref not in refs:
                refs.append(ref)
    # 匹配所有 **参考角色** 行（与参考图合并，不互斥）
    for match in re.finditer(r'\*\*参考角色\*\*[：:]\s*人物\s*(\w+)', raw_content):
        ref = ("人物", match.group(1).strip())
        if ref not in refs:
            refs.append(ref)
    return refs


# 类型 → (子目录, 文件前缀) 的映射
REF_TYPE_MAP = {
    "人物": ("characters", "char"),
    "场景": ("scenes", "scene"),
    "物品": ("props", "prop"),
    "帧图": ("frames", "frame"),
}


def extract_item_id(name):
    """从标题中提取编号，如 '人物 01a：归档者' → '01a'，'帧图 F01：...' → 'F01'"""
    match = re.search(r'(?:人物|场景|物品|帧图)\s*(\w+)[：:]', name)
    if match:
        return match.group(1)
    return None


def parse_prompts_from_md(filepath):
    """从 md 文件中按标题分割提示词。"""
    path = Path(filepath)
    if not path.exists():
        print(f"错误：提示词文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    style = extract_style_declaration(filepath)

    has_h3 = bool(re.search(r'\n###\s', text))
    if has_h3:
        sections = re.split(r'\n(?=###\s)', text)
        header_re = re.compile(r'^###\s+(.+)')
    else:
        sections = re.split(r'\n(?=##\s)', text)
        header_re = re.compile(r'^##\s+(.+)')

    prompts = []
    skip_keywords = ["整体风格声明", "文档完成", "版本", "下一步", "项目", "生成日期", "基于"]
    # 只有标题匹配「人物/场景/物品 XX」格式的段落才是可生图条目
    item_header_re = re.compile(r'(?:人物|场景|物品|帧图)\s*\w+[：:]')

    for section in sections:
        section = section.strip()
        if not section:
            continue
        match = header_re.match(section)
        if not match:
            continue
        name = match.group(1).strip()
        if any(kw in name for kw in skip_keywords):
            continue
        # 跳过非条目段落（如"家族共性说明"等说明性段落）
        if not item_header_re.search(name):
            continue

        lines = section.split('\n', 1)
        raw_content = lines[1].strip() if len(lines) > 1 else ""

        # 提取参考图标记（支持多张：人物/场景/物品）
        refs = extract_references(raw_content)

        # 提取条目编号
        item_id = extract_item_id(name)

        # 清洗内容
        content = clean_prompt_content(raw_content)
        if len(content) < 20:
            continue

        prompts.append({
            "name": name,
            "content": content,
            "style": style,
            "item_id": item_id,     # 如 '01a', '01b', '02'
            "refs": refs,           # 如 [("场景", "03"), ("人物", "02")]
        })

    return prompts


def generate_image(api_key, api_url, model, prompt_text, reference_images=None, timeout=360):
    """调用 API 生成图片，返回 base64 图片数据。纯透传，不添加额外指令。

    reference_images: 单个路径字符串或路径列表
    timeout: API 请求超时秒数（默认 360）
    """
    messages_content = []

    if reference_images:
        if isinstance(reference_images, str):
            reference_images = [reference_images]
        for ref_img in reference_images:
            data_uri = encode_image_to_base64(ref_img)
            if data_uri:
                messages_content.append({
                    "type": "image_url",
                    "image_url": {"url": data_uri}
                })

    messages_content.append({
        "type": "text",
        "text": prompt_text
    })

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": messages_content}],
        "response_modalities": ["IMAGE", "TEXT"],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    resp = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()

    for choice in data.get("choices", []):
        message = choice.get("message", {})
        content = message.get("content", [])
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        _, encoded = url.split(",", 1)
                        return base64.b64decode(encoded)
        if isinstance(content, str):
            match = re.search(r'data:image/\w+;base64,([A-Za-z0-9+/=]+)', content)
            if match:
                return base64.b64decode(match.group(1))

    print("  ⚠ API 响应中未找到图片数据", file=sys.stderr)
    return None


def extract_entry_type(name):
    """从条目名推断类型：人物/场景/物品"""
    for t in ("人物", "场景", "物品", "帧图"):
        if t in name:
            return t
    return None


def make_item_key(name, item_id):
    """生成条目的唯一键，如 '人物_01a'、'场景_03'"""
    entry_type = extract_entry_type(name)
    if entry_type and item_id:
        return f"{entry_type}_{item_id}"
    return None


def build_waves(prompts, id_to_path):
    """拓扑排序：按依赖关系将条目分成多个波次。

    wave 0: 无文件内依赖（所有 ref 已在 id_to_path 中预加载，或无 ref）
    wave N+1: 依赖的条目全部在 wave 0..N 中

    返回 (waves, item_keys)
      waves: [[idx, ...], [idx, ...], ...]  每个波次包含的 prompts 索引
      item_keys: {idx: key}  每个条目的唯一键
    """
    # 建立条目索引 → 键的映射
    item_keys = {}
    key_to_idx = {}
    for i, p in enumerate(prompts):
        key = make_item_key(p["name"], p["item_id"])
        if key:
            item_keys[i] = key
            key_to_idx[key] = i

    # 计算每个条目的文件内依赖（ref 指向同文件中的其他条目）
    in_file_deps = {}  # idx → set of dep idx
    for i, p in enumerate(prompts):
        deps = set()
        for ref_type, ref_id in p["refs"]:
            ref_key = f"{ref_type}_{ref_id}"
            # 如果 ref 已在预加载映射中，不算文件内依赖
            if ref_key in id_to_path:
                continue
            # 如果 ref 指向同文件中的另一个条目，算文件内依赖
            if ref_key in key_to_idx:
                deps.add(key_to_idx[ref_key])
        in_file_deps[i] = deps

    # 拓扑排序分波
    assigned = set()
    waves = []
    remaining = set(range(len(prompts)))

    while remaining:
        # 本波次：所有依赖都已被分配到之前波次的条目
        wave = []
        for i in remaining:
            if in_file_deps[i].issubset(assigned):
                wave.append(i)
        if not wave:
            # 存在循环依赖，强制把剩余的都放进最后一波
            print(f"  ⚠ 检测到循环依赖，强制处理剩余 {len(remaining)} 个条目")
            wave = list(remaining)
        waves.append(wave)
        for i in wave:
            assigned.add(i)
            remaining.discard(i)

    return waves, item_keys


def generate_one_item(api_key, api_url, model, p, idx, total, prefix, output_dir, id_to_path,
                      reference_image_override, timeout):
    """生成单个条目的图片。返回 (idx, success, outpath_or_none)"""
    suffix = p["item_id"] if p["item_id"] else f"{idx+1:02d}"
    filename = f"{prefix}-{suffix}.png"
    prompt_filename = f"{prefix}-{suffix}_prompt.txt"
    outpath = output_dir / filename
    prompt_path = output_dir / prompt_filename

    # 构建发给 API 的提示词（风格 + 内容）
    actual_prompt = p["content"]
    if p.get("style"):
        actual_prompt = f"[视觉风格] {p['style']}\n\n{actual_prompt}"

    # 确定参考图（支持多张）
    ref_images = []
    ref_labels = []
    if reference_image_override:
        ref_images = [reference_image_override]
        ref_labels = [Path(reference_image_override).stem]
    elif p["refs"]:
        for ref_type, ref_id in p["refs"]:
            ref_key = f"{ref_type}_{ref_id}"
            ref_path = id_to_path.get(ref_key)
            if ref_path and Path(ref_path).exists():
                ref_images.append(str(ref_path))
                ref_labels.append(f"{ref_type} {ref_id}")
            else:
                print(f"  ⚠ [{filename}] 参考图未找到: {ref_type} {ref_id}（键={ref_key}）")

    # 多参考图时，在提示词前插入编号说明
    if len(ref_images) > 1:
        legend_lines = ["[参考图说明]"]
        for i, label in enumerate(ref_labels, 1):
            legend_lines.append(f"参考图{i}: {label}")
        legend = "\n".join(legend_lines)
        actual_prompt = f"{legend}\n\n{actual_prompt}"

    ref_display = ", ".join(Path(r).name for r in ref_images) if ref_images else "(无)"

    print(f"[{idx+1}/{total}] 生成: {p['name'][:50]}... → {filename}")
    if ref_images:
        for i, (img, label) in enumerate(zip(ref_images, ref_labels), 1):
            print(f"  ↳ 参考图{i}: {label} → {Path(img).name}")

    # 保存提示词到 txt
    prompt_path.write_text(
        f"=== 条目名称 ===\n{p['name']}\n\n"
        f"=== 条目编号 ===\n{suffix}\n\n"
        f"=== 风格声明 ===\n{p.get('style', '(无)')}\n\n"
        f"=== 参考图 ===\n{ref_display}\n\n"
        f"=== 发送给 API 的提示词 ===\n{actual_prompt}\n",
        encoding="utf-8"
    )

    try:
        img_data = generate_image(
            api_key, api_url, model, actual_prompt,
            ref_images if ref_images else None,
            timeout=timeout
        )
        if img_data:
            outpath.write_bytes(img_data)
            print(f"  ✓ [{filename}] 成功 ({len(img_data)} bytes)")
            return (idx, True, outpath)
        else:
            print(f"  ✗ [{filename}] 失败：未获取到图片数据")
            return (idx, False, None)
    except requests.exceptions.RequestException as e:
        print(f"  ✗ [{filename}] API 错误: {e}", file=sys.stderr)
        return (idx, False, None)
    except Exception as e:
        print(f"  ✗ [{filename}] 错误: {e}", file=sys.stderr)
        return (idx, False, None)


def main():
    import concurrent.futures

    parser = argparse.ArgumentParser(description="调用 nano banana API 生成图片")
    parser.add_argument("--prompt", help="单条提示词文本")
    parser.add_argument("--prompt-file", help="从 md 文件批量读取提示词")
    parser.add_argument("--reference-image", help="可选参考图路径")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--prefix", default="img", help="文件名前缀（默认 img）")
    parser.add_argument("--image-base-dir", help="图片根目录（用于跨文件引用）")
    parser.add_argument("--timeout", type=int, default=360, help="API 超时秒数（默认 360）")
    parser.add_argument("--max-retries", type=int, default=2, help="失败重试次数（默认 2）")
    parser.add_argument("--max-workers", type=int, default=3, help="并行线程数（默认 3）")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已存在的 PNG 文件，只生成缺失的")
    args = parser.parse_args()

    if not args.prompt and not args.prompt_file:
        print("错误：必须指定 --prompt 或 --prompt-file", file=sys.stderr)
        sys.exit(1)

    api_key, api_url, model = load_image_api_config()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 收集提示词
    prompts = []
    if args.prompt_file:
        prompts = parse_prompts_from_md(args.prompt_file)
    if args.prompt:
        prompts.append({
            "name": args.prefix,
            "content": args.prompt,
            "style": "",
            "item_id": None,
            "refs": [],
        })

    if not prompts:
        print("错误：未解析到任何提示词", file=sys.stderr)
        sys.exit(1)

    # 建立 (类型, 编号) → 生成图路径的映射（供引用查找参考图）
    id_to_path = {}

    # 预扫描已有图片（跨文件引用）
    if args.image_base_dir:
        base = Path(args.image_base_dir)
        for ref_type, (subdir, prefix) in REF_TYPE_MAP.items():
            scan_dir = base / subdir
            if scan_dir.exists():
                for img_file in scan_dir.glob(f"{prefix}-*.png"):
                    stem = img_file.stem
                    parts = stem.split("-", 1)
                    if len(parts) == 2:
                        img_id = parts[1]
                        key = f"{ref_type}_{img_id}"
                        id_to_path[key] = img_file
                        print(f"  📎 预加载参考图: {ref_type} {img_id} → {img_file.name}")

    # 构建依赖波次
    waves, item_keys = build_waves(prompts, id_to_path)
    total = len(prompts)

    print(f"\n📊 依赖分析：{total} 个条目，{len(waves)} 个波次")
    for wi, wave in enumerate(waves):
        names = [prompts[i]["name"][:20] for i in wave]
        print(f"  波次 {wi}: {len(wave)} 个条目 — {', '.join(names)}")
    print()

    success, fail, skipped = 0, 0, 0
    failed_keys = set()  # 最终失败的条目键（重试后仍失败）

    for wi, wave in enumerate(waves):
        print(f"{'='*60}")
        print(f"▶ 波次 {wi}/{len(waves)-1}：{len(wave)} 个条目（并行 max_workers={args.max_workers}）")
        print(f"{'='*60}")

        # 检查本波次中是否有条目因依赖失败而需要跳过
        runnable = []
        for idx in wave:
            p = prompts[idx]
            # 检查是否有依赖项最终失败
            dep_failed = False
            for ref_type, ref_id in p["refs"]:
                ref_key = f"{ref_type}_{ref_id}"
                if ref_key in failed_keys:
                    dep_failed = True
                    print(f"  ⏭ 跳过: {p['name'][:40]}（依赖 {ref_key} 已失败）")
                    skipped += 1
                    # 把自己也标记为失败，传播给下游
                    my_key = item_keys.get(idx)
                    if my_key:
                        failed_keys.add(my_key)
                    break
            if not dep_failed:
                # --skip-existing：跳过已有 PNG 的条目
                if args.skip_existing:
                    suffix = p["item_id"] if p["item_id"] else f"{idx+1:02d}"
                    existing = output_dir / f"{args.prefix}-{suffix}.png"
                    if existing.exists() and existing.stat().st_size > 0:
                        print(f"  ⏩ 已存在: {p['name'][:40]} → {existing.name}")
                        success += 1
                        my_key = item_keys.get(idx)
                        if my_key:
                            id_to_path[my_key] = existing
                        continue
                runnable.append(idx)

        if not runnable:
            continue

        # 并行执行本波次的可运行条目
        results = {}  # idx → (success, outpath)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            futures = {}
            for idx in runnable:
                f = executor.submit(
                    generate_one_item,
                    api_key, api_url, model, prompts[idx], idx, total, args.prefix,
                    output_dir, id_to_path, args.reference_image, args.timeout
                )
                futures[f] = idx

            for f in concurrent.futures.as_completed(futures):
                idx, ok, outpath = f.result()
                results[idx] = (ok, outpath)

        # 处理结果 + 重试失败项
        for idx in runnable:
            ok, outpath = results[idx]
            p = prompts[idx]
            my_key = item_keys.get(idx)

            if ok and outpath:
                success += 1
                # 注册到映射供后续波次使用
                if my_key:
                    id_to_path[my_key] = outpath
            else:
                # 重试
                retried_ok = False
                for attempt in range(1, args.max_retries + 1):
                    print(f"  🔄 重试 ({attempt}/{args.max_retries}): {p['name'][:40]}")
                    _, retry_ok, retry_path = generate_one_item(
                        api_key, api_url, model, p, idx, total, args.prefix,
                        output_dir, id_to_path, args.reference_image, args.timeout
                    )
                    if retry_ok and retry_path:
                        success += 1
                        if my_key:
                            id_to_path[my_key] = retry_path
                        retried_ok = True
                        break

                if not retried_ok:
                    fail += 1
                    if my_key:
                        failed_keys.add(my_key)
                    print(f"  ✗ 最终失败: {p['name'][:40]}（已重试 {args.max_retries} 次）")

    # 汇总
    print(f"\n{'='*60}")
    print(f"完成：成功 {success}，失败 {fail}，跳过 {skipped}，共 {total} 条")
    if failed_keys:
        print(f"失败项: {', '.join(sorted(failed_keys))}")
    if skipped > 0:
        print(f"（跳过的条目因依赖项失败而无法生成）")
    print(f"{'='*60}")
    sys.exit(1 if fail > 0 and success == 0 else 0)


if __name__ == "__main__":
    main()
