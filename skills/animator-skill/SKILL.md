---
name: animator-skill
description: 动画师技能。将静态分镜转化为图生视频的动态提示词（Motion Prompt）。
---

# 动画师技能

## 必读
1. `../../references/00-first-principles.md`
2. `../../references/08-camera-and-cinematography.md`
3. `../../references/11b-image-motion-prompt.md`

## 技能说明

动画师技能，用于将静态分镜转化为图生视频的动态提示词。为每个关键帧和四宫格展开生成简洁、具体、可执行的 Motion Prompt，用于 Runway、Kling、Pika 等 AI 视频工具。

## 输入
1. Beat breakdown（节拍拆解，理解叙事目的与情绪）
2. Beat board prompt（九宫格提示词）
3. Sequence board prompt（四宫格提示词）

## 输出
1. Motion prompts（动态提示词）— 每个 Beat Anchor 一组，每组包含关键帧和四宫格的动态提示词

## 执行流程

### 第一步：读取上游产物
- 读取 beat-breakdown.md（节拍拆解，理解叙事目的与情绪）
- 读取 beat-board-prompt.md（九宫格提示词）
- 读取 sequence-board-prompt.md（四宫格提示词）

### 第二步：生成动态提示词
为每个 Beat Anchor 生成一组 Motion Prompt：
- 1 个关键帧动态提示词（对应九宫格该格）
- 4 个四宫格动态提示词（对应四宫格展开）

### 第三步：输出
创建 motion-prompt.md，按标准格式写入

## 动态提示词核心原则

### 图片已见原则
- AI 能"看到"输入图片，不需要重复描述图片内容
- 只描述"变化"：动作、运动、情绪转变
- 重复描述图片内容会导致运动减少或异常

### 简洁优先原则
- 最佳长度：50-200 字符（英文）
- 聚焦 2-3 个核心元素
- 信息过载会导致模型困惑

### 具体动作原则
- 用具体的物理动作，避免抽象概念
- ✓ "hair flowing in wind"
- ✗ "embodies the essence of freedom"

### 运动限制原则
- 镜头运动：最多 1-2 种
- 主体运动：最多 1-2 种
- 过多运动会产生混乱

## 提示词结构

**基本公式**：
镜头运动 + 主体动作 + 速度/节奏 + 氛围/风格

**完整公式（复杂场景）**：
镜头运动 + 主体动作 + 环境动态 + 速度/节奏 + 氛围/风格 + 技术参数

**示例**：
- 基本：Camera slowly pushes in while subject turns head
- 完整：Slow dolly in, subject turns head, hair flowing gently in wind, golden hour lighting, cinematic 24fps

## 镜头运动词汇库

### 推拉类（Dolly）
- dolly in / push in：推近，聚焦、紧张、亲密
- dolly out / pull back：拉远，揭示、疏离、结束感
- dolly zoom / vertigo effect：眩晕效果，心理冲击

### 横纵摇类（Pan/Tilt）
- pan left / pan right：横摇，环顾、跟随水平运动
- tilt up / tilt down：纵摇，强调高度、规模、威严
- whip pan：快速横摇，转场、惊讶

### 环绕类（Orbit/Arc）
- orbit around subject：环绕主体，立体感、动感
- arc shot：弧形运动，戏剧性、强调
- 180-degree orbit：半环绕，常用于对话、对峙
- 360-degree orbit：全环绕，产品展示、英雄时刻

### 跟拍类（Tracking）
- tracking shot：跟随主体移动
- follow from behind：背后跟拍
- side tracking：侧面跟拍
- leading shot：前方引导

### 变焦类（Zoom）
- zoom in：变焦推近，强调、戏剧性
- zoom out：变焦拉远，揭示全貌
- slow zoom：缓慢变焦，悬疑、张力

### 升降类（Crane/Jib）
- crane up / rising shot：上升，史诗感、希望
- crane down / descending shot：下降，压迫、沉重
- aerial / drone shot：航拍，规模、全景

### 手持与稳定（Handheld/Stabilized）
- handheld：手持，真实感、紧张、纪录片风格
- steady / locked camera：固定机位，稳定、庄重
- floating camera：漂浮感，梦幻、超现实

### 焦点类（Focus）
- rack focus：焦点转移，引导注意力
- shallow depth of field：浅景深，突出主体
- deep focus：深焦，环境信息丰富

## 主体动作词汇库

### 面部动作
- eyes open slowly：缓慢睁眼
- subtle smile forming：微笑浮现
- gaze shifts：目光转移
- eyebrows raise：眉毛上扬
- blinks naturally：自然眨眼
- expression transitions from X to Y：表情从X转为Y

### 头部动作
- head turns：转头
- head tilts slightly：微微歪头
- nods slowly：缓慢点头
- looks up / down / away：抬头/低头/移开视线

### 身体动作
- breathing motion：呼吸起伏
- shoulders rise and fall：肩膀起伏
- leans forward / back：前倾/后仰
- stands up / sits down：站起/坐下
- walks forward / toward camera：向前走/走向镜头
- reaches out hand：伸出手

### 手部动作
- hand raises：举手
- fingers move：手指动作
- grips tighter：握紧
- gestures while speaking：说话时比划

### 环境互动
- hair flowing in wind：头发随风飘动
- clothes rustling：衣服飘动
- fabric billowing：布料鼓起
- water splashing：水花飞溅
- leaves falling：落叶飘落
- smoke rising：烟雾升起
- dust particles floating：尘埃飘浮

## 速度与强度修饰词

### 缓慢/轻柔
- slowly, gently, gradually, softly
- subtle, slight, delicate
- natural, organic, barely perceptible
- micro-movements, minimal motion

### 中等/自然
- smoothly, steadily, naturally
- moderate, balanced, controlled
- fluid, flowing, continuous

### 快速/强烈
- quickly, rapidly, suddenly
- dramatic, bold, powerful, intense
- explosive, dynamic, energetic
- sweeping, grand, epic

## 氛围与风格词汇

### 电影风格
- cinematic, filmic, movie-quality
- blockbuster style, Hollywood quality
- indie film aesthetic
- documentary style

### 情绪氛围
- dramatic, intense, suspenseful
- romantic, dreamy, nostalgic
- mysterious, eerie, haunting
- joyful, energetic, uplifting
- melancholic, somber, contemplative

### 技术参数（可选）
- 24fps：电影感
- 60fps：流畅、慢动作素材
- slow motion：慢动作
- film grain：胶片颗粒感
- lens flare：镜头光晕
- bokeh：背景虚化光斑

## 从分镜到动态提示词的转化

### 转化步骤
1. **识别画面核心动作**
   - 从分镜的"视角"描述中提取关键动作
   - 确定主体运动和镜头运动

2. **简化为核心元素**
   - 删除外观描述（AI已从图片获取）
   - 保留动作、运动、氛围
   - 控制在 2-3 个核心元素

3. **选择镜头运动**
   - 根据情绪选择镜头运动类型
   - 紧张/聚焦 → push in
   - 揭示/疏离 → pull back
   - 动感/立体 → orbit
   - 跟随/沉浸 → tracking

4. **添加速度修饰**
   - 根据情绪节奏选择速度词
   - 平静 → slowly, gently
   - 紧张 → quickly, suddenly
   - 戏剧 → dramatically

5. **补充氛围（可选）**
   - 添加风格参考或技术参数
   - 保持简洁，不超过 1-2 个

### 转化示例
**四宫格描述**：
"中景，教室内，林书白站在窗边，阳光斜射进来，他缓缓转头看向门口"

**Motion Prompt**：
"Slow pan, subject turns head toward door, sunlight streaming through window, cinematic"

## 禁忌规则

### 绝对禁忌
- ❌ 否定句（No movement, Don't zoom）
  - AI 不理解否定，可能产生相反效果
  - ✓ 用肯定句：The camera stays still / locked camera

- ❌ 重复图片内容
  - 会导致运动减少或静止
  - ✓ 只描述动作变化

- ❌ 抽象概念（embodies freedom, manifests joy）
  - AI 无法解释抽象意图
  - ✓ 用具体物理动作

- ❌ 多重场景变化
  - 模型无法处理复杂转场
  - ✓ 单一场景、单一动作链

### 避免事项
- ⚠️ 超过 2 种镜头运动组合
- ⚠️ 超过 2 种主体运动组合
- ⚠️ 过长提示词（超过 300 字符）
- ⚠️ 违反物理规律的动作
- ⚠️ 与图片内容矛盾的描述

## 成功标准
1. 每个动态提示词长度在 50-200 字符（英文）
2. 聚焦 2-3 个核心元素
3. 只描述变化，不重复图片内容
4. 使用具体物理动作，避免抽象概念
5. 镜头运动和主体运动各不超过 2 种
6. 不使用否定句
7. 速度修饰词与情绪节奏匹配
8. 氛围风格词汇简洁（不超过 1-2 个）
9. 符合物理规律，不与图片内容矛盾
10. 可直接用于 Runway、Kling、Pika 等 AI 视频工具