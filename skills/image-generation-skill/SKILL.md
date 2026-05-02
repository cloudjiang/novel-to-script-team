---
name: image-generation-skill
description: 调用 nano banana API（gemini-3.1-flash-image-preview）生成图片。支持纯文本生图和参考图生图。
---

# image-generation-skill

## 概述
调用 nano banana API 将服化道/分镜提示词转化为图片。支持两种模式：
1. 纯文本生图：提示词 → API → PNG 图片
2. 参考图生图：提示词 + 本地参考图（base64 编码）→ API → PNG 图片

## 前置条件
- `.env` 或环境变量中配置了 `NANO_BANANA_API_KEY` 和 `NANO_BANANA_BASE_URL`
- Python 3 已安装
- `requests` 库已安装（`pip install requests`）

## 输入
- 提示词文件：`outputs/{剧本名}/assets/character-prompts.md`、`scene-prompts.md` 或 `prop-prompts.md`
- 单条提示词：直接传入文本
- 可选参考图：本地图片路径

## 输出
- 角色图：`outputs/{剧本名}/images/characters/{前缀}-{序号}.png`
- 场景图：`outputs/{剧本名}/images/scenes/{前缀}-{序号}.png`
- 物品图：`outputs/{剧本名}/images/props/{前缀}-{序号}.png`

## 执行流程

### 步骤1：环境检查
确认 `.env` 中有 `NANO_BANANA_API_KEY` 和 `NANO_BANANA_BASE_URL`：
```bash
test -f .env && grep -q "NANO_BANANA_API_KEY" .env && grep -q "NANO_BANANA_BASE_URL" .env
```

### 步骤2：生成角色图（第一批，无外部依赖）
```bash
python scripts/generate_image.py \
  --prompt-file "outputs/{剧本名}/assets/character-prompts.md" \
  --output-dir "outputs/{剧本名}/images/characters" \
  --prefix char
```

### 步骤3：生成物品图（第二批，白底独立策略，仅同族物品间有依赖）
```bash
python scripts/generate_image.py \
  --prompt-file "outputs/{剧本名}/assets/prop-prompts.md" \
  --output-dir "outputs/{剧本名}/images/props" \
  --image-base-dir "outputs/{剧本名}/images" \
  --prefix prop
```

### 步骤4：生成场景图（第三批，依赖角色图和物品图，通过 --image-base-dir 跨文件引用）
```bash
python scripts/generate_image.py \
  --prompt-file "outputs/{剧本名}/assets/scene-prompts.md" \
  --output-dir "outputs/{剧本名}/images/scenes" \
  --image-base-dir "outputs/{剧本名}/images" \
  --prefix scene
```

**生成顺序很重要**：角色 → 物品 → 场景 → 帧图，确保被引用的图先生成。场景引用角色图和物品图，所以必须在场景之前生成。帧图依赖角色图和场景图，所以最后生成。

### 步骤5：生成帧图（第四批，按集组织，依赖角色图 + 场景图）

帧图由 `seedance-storyboard-skill` 在生成提示词时同步输出到 `03-frame-requests.md`。帧图按集组织，不跨集累积。

```bash
python scripts/generate_image.py \
  --prompt-file "outputs/{剧本名}/storyboard/ep<N>/03-frame-requests.md" \
  --output-dir "outputs/{剧本名}/images/frames/ep<N>" \
  --image-base-dir "outputs/{剧本名}/images" \
  --prefix frame
```

帧图类型说明：
- **首帧图**：用于 I2V-首帧模式，锁定开场构图
- **尾帧图**：用于首尾帧模式，锁定结束画面
- **分镜参考图**：用于多参考模式多时段，引导各时段画面

### 步骤6（可选）：参考图生图
```bash
python scripts/generate_image.py \
  --prompt "根据参考图风格生成..." \
  --reference-image /path/to/reference.png \
  --output-dir "outputs/{剧本名}/images/characters" \
  --prefix char-ref
```

### 步骤7：检查输出
- 确认图片文件存在且非空
- 报告生成成功/失败的数量

## 成功标准
- [ ] 所有提示词都已处理
- [ ] 图片文件存在且大小 > 0
- [ ] 文件命名符合 `{prefix}-{序号}.png` 规范
- [ ] 无 API 调用错误

## 错误处理
- API key 缺失：提示用户配置 `.env`
- API 调用失败：记录错误，继续处理下一条
- 图片解码失败：记录错误，跳过该条
