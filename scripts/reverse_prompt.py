#!/usr/bin/env python3
"""
reverse_prompt.py — 从图片反推生成提示词

用法：
  # 完整分析
  python scripts/reverse_prompt.py --image path/to/image.jpg --output-dir outputs/剧本名/reverse-prompts

  # 聚焦人物
  python scripts/reverse_prompt.py --image path/to/image.jpg --output-dir outputs/剧本名/reverse-prompts --mode character

  # 聚焦场景
  python scripts/reverse_prompt.py --image path/to/image.jpg --output-dir outputs/剧本名/reverse-prompts --mode scene

  # 聚焦构图
  python scripts/reverse_prompt.py --image path/to/image.jpg --output-dir outputs/剧本名/reverse-prompts --mode composition
"""

import argparse
import base64
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("错误：需要 openai 库。请运行: pip install openai", file=sys.stderr)
    sys.exit(1)

try:
    from .env_config import get_optional_env, get_required_env, load_env
except ImportError:
    from env_config import get_optional_env, get_required_env, load_env

DEFAULT_REVERSE_MODEL = "gemini-3.1-pro-preview"


def encode_image_to_base64(image_path):
    """将本地图片编码为 base64 data URI"""
    path = Path(image_path)
    if not path.exists():
        print(f"错误：图片文件不存在: {image_path}", file=sys.stderr)
        sys.exit(1)

    suffix = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif"
    }
    mime = mime_map.get(suffix, "image/png")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def get_analysis_prompt(mode):
    """根据分析维度生成提示词"""
    prompts = {
        "full": """请详细分析这张图片的所有视觉元素，���生成可用于文生图的提示词。

分析要求：
1. 使用叙事描述式，避免关键词堆叠
2. 覆盖以下元素：
   - 人物：外观、服装、表情、姿态、动作
   - 场景：环境、道具、空间关系
   - 构图：景别、角度、视角
   - 色彩：主色调、色彩对比、色彩情绪
   - 光影：光源、明暗对比、光影氛围
   - 氛围：情绪基调、叙事意图
3. 描述要精确，能够生成相似的图片

请按以下格式输出：

## 提示词

[完整的叙事描述式提示词]

## 关键元素

**人物**：
- [人物相关元素]

**场景**：
- [场景相关元素]

**构图**：
- [构图相关元素]

**色彩**：
- [色彩相关元素]

**光影**：
- [光影相关元素]

**氛围**：
- [氛围相关元素]""",

        "character": """请重点分析这张图片中的人物元素，并生成可用于角色设定的提示词。

分析要求：
1. 使用叙事描述式，避免关键词堆叠
2. 重点关注：
   - 外观：年龄、性别、发型、五官特征
   - 服装：款式、颜色、材质、配饰
   - 表情：情绪、眼神、面部细节
   - 姿态：站姿、坐姿、动作、身体语言
   - 气质：整体印象、性格暗示
3. 描述要精确，能够生成相似的人物

请按以下格式输出：

## 提示词

[聚焦人物的叙事描述式提示词]

## 关键元素

**人物**：
- 外观：[外观描述]
- 服装：[服装描述]
- 表情：[表情描述]
- 姿态：[姿态描述]
- 气质：[气质描述]""",

        "scene": """请重点分析这张图片中的场景元素，并生成可用于场景设定的提示词。

分析要求：
1. 使用叙事描述式，避免关键词堆叠
2. 重点关注：
   - 环境：室内/室外、建筑风格、空间特征
   - 道具：重要物品、装饰、细节
   - 空间关系：前景、中景、背景的布局
   - 光线：光源类型、光线方向、光线质感
   - 氛围：环境情绪、叙事暗示
3. 描述要精确，能够生成相似的场景

请按以下格式输出：

## 提示词

[聚焦场景的叙事描述式提示词]

## 关键元素

**场景**：
- 环境：[环境描述]
- 道具：[道具描述]
- 空间关系：[空间关系描述]
- 光线：[光线描述]
- 氛围：[氛围描述]""",

        "composition": """请重点分析这张图片的构图元素，并生成可用于分镜参考的提示词。

分析要求：
1. 使用叙事描述式，避免关键词堆叠
2. 重点关注：
   - 景别：特写、近景、中景、全景、远景
   - 角度：平视、俯视、仰视、侧视
   - 视角：正面、侧面、背面、斜侧
   - 人物位置：在画面中的位置和比例
   - 背景：背景元素和层次
   - 色彩：主色调、色彩对比、色彩情绪
   - 光影：光源、明暗对比、光影氛围
3. 描述要精确，能够复现相似的构图

请按以下格式输出：

## 提示词

[聚焦构图的叙事描述式提示词]

## 关键元素

**构图**：
- 景别：[景别描述]
- 角度：[角度描述]
- 视角：[视角描述]
- 人物位置：[位置描述]
- 背景：[背景描述]

**色彩**：
- 主色调：[色调描述]
- 色彩对比：[对比描述]
- 色彩情绪：[情绪描述]

**光影**：
- 光源：[光源描述]
- 明暗对比：[对比描述]
- 光影氛围：[氛围描述]"""
    }
    return prompts.get(mode, prompts["full"])


def reverse_prompt(api_key, base_url, model, image_path, mode="full"):
    """调用 API 从图片反推提示词"""
    print(f"正在分析图片: {image_path}")
    print(f"分析维度: {mode}")

    # 编码图片
    print("编码图片...")
    data_uri = encode_image_to_base64(image_path)

    # 初始化客户端
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # 构建消息
    messages = [{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": data_uri}
            },
            {
                "type": "text",
                "text": get_analysis_prompt(mode)
            }
        ]
    }]

    # 调用 API
    print("调用 API...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        prompt_text = response.choices[0].message.content
        print("✓ 分析完成")
        return prompt_text
    except Exception as e:
        print(f"✗ API 调用失败: {e}", file=sys.stderr)
        sys.exit(1)


def save_prompt(prompt_text, image_path, output_dir, mode):
    """保存提示词到文件"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成输出文件名
    image_name = Path(image_path).stem
    output_file = output_dir / f"{image_name}-prompt.md"

    # 构建输出内容
    content = f"""# 图片反推提示词

**原图路径**：`{image_path}`
**分析维度**：{mode}
**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{prompt_text}

---

**使用说明**：
- 此提示词由 AI 从图片中提取生成
- 可直接用于文生图工具（如 Seedance、Midjourney 等）
- 可根据需要修改和优化
- 建议与项目已有的角色/场景提示词保持风格一致
"""

    # 保存文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ 提示词已保存: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="从图片反推生成提示词")
    parser.add_argument("--image", required=True, help="图片文件路径")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument(
        "--mode",
        choices=["full", "character", "scene", "composition"],
        default="full",
        help="分析维度（默认：full）"
    )

    args = parser.parse_args()

    # 加载 API 配置
    env = load_env()
    api_key = get_required_env(env, "NANO_BANANA_API_KEY")
    base_url = get_required_env(env, "NANO_BANANA_BASE_URL")
    model = get_optional_env(env, "NANO_BANANA_REVERSE_MODEL", DEFAULT_REVERSE_MODEL)

    # 反推提示词
    prompt_text = reverse_prompt(api_key, base_url, model, args.image, args.mode)

    # 保存提示词
    output_file = save_prompt(prompt_text, args.image, args.output_dir, args.mode)

    print(f"\n完成！提示词文件：{output_file}")


if __name__ == "__main__":
    main()
