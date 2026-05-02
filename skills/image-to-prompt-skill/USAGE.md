# 图片反推提示词使用指南

## 功能概述

`image-to-prompt` Agent 可以从图片中提取视觉描述，生成可用于文生图的提示词。支持四种分析维度：
- **full**：完整分析（默认）
- **character**：聚焦人物
- **scene**：聚焦场景
- **composition**：聚焦构图

## 使用方法

### 方法 1：通过命令行直接调用

```bash
# 完整分析
python scripts/reverse_prompt.py \
  --image path/to/image.jpg \
  --output-dir outputs/剧本名/reverse-prompts

# 聚焦人物
python scripts/reverse_prompt.py \
  --image path/to/image.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode character

# 聚焦场景
python scripts/reverse_prompt.py \
  --image path/to/image.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode scene

# 聚焦构图
python scripts/reverse_prompt.py \
  --image path/to/image.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode composition
```

### 方法 2：通过 Showrunner 调用

```
~reverse-prompt path/to/image.jpg [mode]
```

示例：
```
~reverse-prompt outputs/剧本名/images/characters/char-01.png character
~reverse-prompt outputs/剧本名/images/scenes/scene-03.png scene
~reverse-prompt reference-images/style-ref.jpg full
```

## 输出示例

### 完整分析（full）

**输入**：一张办公室场景的图片

**输出**：`outputs/剧本名/reverse-prompts/office-scene-prompt.md`

```markdown
# 图片反推提示词

**原图路径**：`reference-images/office-scene.jpg`
**分析维度**：full
**生成时间**：2026-03-15 16:30:00

---

## 提示词

一位身穿深蓝色西装的中年男性站在现代办公室的落地窗前，表情严肃，目光锐利。他的右手插在口袋里，左手自然垂放，身体微微侧向窗外。背景是城市天际线，高楼林立，天空呈现出黄昏时分的暖橙色调。办公室内部光线柔和，来自顶部的筒灯和窗外的自然光形成明暗对比，营造出一种冷静、专业的氛围。

## 关键元素

**人物**：
- 外观：中年男性，短发，五官立体
- 服装：深蓝色西装，白色衬衫，深色领带
- 表情：严肃，目光锐利
- 姿态：站立，右手插口袋，左手垂放，身体微侧

**场景**：
- 环境：现代办公室，落地窗，城市天际线
- 道具：无明显道具
- 空间关系：人物站在窗前，背景是城市

**构图**：
- 景别：中景
- 角度：平视
- 视角：正面偏侧

**色彩**：
- 主色调：深蓝、暖橙、灰白
- 色彩对比：冷暖对比（室内冷色 vs 窗外暖色）
- 色彩情绪：冷静、专业

**光影**：
- 光源：顶部筒灯 + 窗外自然光
- 明暗对比：中等对比
- 光影氛围：柔和、专业

**氛围**：
- 情绪基调：冷静、严肃、专业
- 叙事意图：展现人物的权威感和决断力

---

**使用说明**：
- 此提示词由 AI 从图片中提取生成
- 可直接用于文生图工具（如 Seedance、Midjourney 等）
- 可根据需要修改和优化
- 建议与项目已有的角色/场景提示词保持风格一致
```

### 聚焦人物（character）

**输入**：一张人物特写图片

**输出**：`outputs/剧本名/reverse-prompts/character-closeup-prompt.md`

```markdown
# 图片反推提示词

**原图路径**：`reference-images/character-closeup.jpg`
**分析维度**：character
**生成时间**：2026-03-15 16:35:00

---

## 提示词

一位中年男性，短发，五官立体，表情严肃，目光锐利。他身穿深蓝色西装，内搭白色衬衫和深色领带，右手插在口袋里，左手自然垂放，身体微微侧向一侧，展现出冷静、专业的气质。

## 关键元素

**人物**：
- 外观：中年男性，短发，五官立体
- 服装：深蓝色西装，白色衬衫，深色领带
- 表情：严肃，目光锐利
- 姿态：站立，右手插口袋，左手垂放，身体微侧
- 气质：冷静、专业、权威

---

**使用说明**：
- 此提示词由 AI 从图片中提取生成
- 可直接用于文生图工具（如 Seedance、Midjourney 等）
- 可根据需要修改和优化
- 建议与项目已有的角色/场景提示词保持风格一致
```

## 使用场景

### 1. 参考图分析

当你有一张参考图片，想要生成风格一致的新图片时：

```bash
# 分析参考图
python scripts/reverse_prompt.py \
  --image reference-images/style-ref.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode full

# 使用生成的提示词创建新图片
# 将提示词复制到 character-prompts.md 或 scene-prompts.md
# 然后调用 image-generator 生成新图片
```

### 2. 风格迁移

从现有图片提取风格特征，应用到新场景：

```bash
# 提取场景风格
python scripts/reverse_prompt.py \
  --image outputs/剧本名/images/scenes/scene-01.png \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode scene

# 将提取的场景风格应用到新场景
# 编辑生成的提示词，替换场景内容但保留风格特征
```

### 3. 提示词优化

对比生成图片与目标效果，优化提示词：

```bash
# 分析目标图片
python scripts/reverse_prompt.py \
  --image target-image.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode full

# 对比生成图片的提示词和目标图片的提示词
# 找出差异，优化生成提示词
```

### 4. 资产复用

从历史项目图片中提取提示词，复用到新项目：

```bash
# 批量提取历史项目的角色提示词
for img in old-project/images/characters/*.png; do
  python scripts/reverse_prompt.py \
    --image "$img" \
    --output-dir new-project/reverse-prompts \
    --mode character
done

# 整理提取的提示词，集成到新项目
```

## 注意事项

1. **API 配置**：确保 `.env` 或环境变量中配置了 `NANO_BANANA_API_KEY` 和 `NANO_BANANA_BASE_URL`
2. **图片格式**：支持 PNG、JPG、JPEG、WEBP、GIF 等常见格式
3. **图片大小**：建议不超过 10MB，过大的图片可能导致 API 调用失败
4. **敏感内容**：避免分析包含敏感内容的图片
5. **版权问题**：确保图片来源合法，避免侵权

## 与其他 Agent 的协作

### 与 art-designer 协作

```bash
# 1. 从参考图提取角色提示词
python scripts/reverse_prompt.py \
  --image reference-images/character-ref.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode character

# 2. art-designer 将提示词集成到 character-prompts.md
# 手动编辑或使用 art-designer 自动集成
```

### 与 image-generator 协作

```bash
# 1. 从参考图提取提示词
python scripts/reverse_prompt.py \
  --image reference-images/style-ref.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode full

# 2. 使用提取的提示词生成新图片
python scripts/generate_image.py \
  --prompt "$(cat outputs/剧本名/reverse-prompts/style-ref-prompt.md | grep -A 100 '## 提示词' | tail -n +2 | head -n 1)" \
  --output-dir outputs/剧本名/images/test
```

### 与 storyboard-artist 协作

```bash
# 1. 从分镜参考图提取构图提示词
python scripts/reverse_prompt.py \
  --image reference-images/storyboard-ref.jpg \
  --output-dir outputs/剧本名/reverse-prompts \
  --mode composition

# 2. storyboard-artist 参考提取的构图提示词优化分镜描述
```

## 常见问题

### Q1: API 调用失败怎么办？

**A**: 检查以下几点：
1. `.env` 或环境变量中是否配置了正确的 `NANO_BANANA_API_KEY` 和 `NANO_BANANA_BASE_URL`
2. 网络连接是否正常
3. 图片文件是否存在且可读
4. 图片大小是否超过限制（建议 < 10MB）

### Q2: 生成的提示词不够精确怎么办？

**A**: 可以尝试：
1. 使用更具体的分析维度（character / scene / composition）
2. 手动编辑生成的提示词，添加更多细节
3. 使用多张参考图，综合提取特征

### Q3: 如何批量处理多张图片？

**A**: 使用 bash 循环：
```bash
for img in reference-images/*.jpg; do
  python scripts/reverse_prompt.py \
    --image "$img" \
    --output-dir outputs/剧本名/reverse-prompts \
    --mode full
done
```

### Q4: 生成的提示词如何集成到项目中？

**A**: 有两种方式：
1. **手动集成**：复制提示词内容到 `character-prompts.md` 或 `scene-prompts.md`
2. **自动集成**：使用 `art-designer` Agent 自动集成（需要实现集成功能）

## 技术细节

### API 调用格式

```python
from openai import OpenAI
import base64
import os

client = OpenAI(
    api_key="your-api-key",
    base_url=os.environ["NANO_BANANA_BASE_URL"]
)

# 读取并编码图片
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

# 调用 API
response = client.chat.completions.create(
    model="gemini-3.1-pro-preview",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            },
            {
                "type": "text",
                "text": "请详细描述这张图片..."
            }
        ]
    }]
)

prompt = response.choices[0].message.content
```

### 图片编码

图片通过 base64 编码传递给 API：
- 支持的格式：PNG、JPG、JPEG、WEBP、GIF
- MIME 类型自动识别：`image/png`、`image/jpeg`、`image/webp`、`image/gif`
- 编码格式：`data:{mime};base64,{base64_string}`

### 提示词生成

根据不同的分析维度，使用不同的提示词模板：
- **full**：完整分析所有元素
- **character**：重点分析人物元素
- **scene**：重点分析场景元素
- **composition**：重点分析构图元素

每个模板都包含详细的分析要求和输出格式规范。
