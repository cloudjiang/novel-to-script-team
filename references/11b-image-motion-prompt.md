> 本文件从 11-video-prompt-engineering.md 拆分而来。相关文件：[11a](11a-seedance-prompt-methodology.md) | [11c](11c-sora2-rhythm-control.md)

# 11b. 图像与动态提示词方法论

## 第二部分：Gemini 图像生成提示词方法论

### 核心原则

#### 叙事描述优先（Narrative Over Keywords）
- Gemini 的核心优势是深度语言理解
- 用完整的叙事性段落描述场景，而非逗号分隔的关键词堆叠
- 错误示范：中景, 低角度, 冷蓝色调, 戏剧性光影
- 正确示范：中景，略微仰拍。冷蓝色的光线打在他脸上，勾勒出深刻的阴影。

#### 场景化思维（Scene-Based Thinking）
- 把每个画面当作电影中的一个镜头来描述
- 回答：谁在哪里、做什么、环境如何、光线如何、情绪如何
- 用短句分层描述，先整体后细节

#### 摄影术语融入自然语言（Photography Terms in Context）
- 不要孤立列出术语，而是描述其效果
- 错误：85mm镜头, 浅景深, 虚化
- 正确：85mm人像镜头，背景柔和虚化，主体从环境中跃然而出。

#### 情绪与氛围具体化（Specific Mood Description）
- 不只说"戏剧性"或"紧张"，而是描述具体的视觉表现
- 用光影、色彩、空间关系来传达情绪
- 例：顶光在他眼窝下刻出深深的阴影，疲惫与挫败感扑面而来。

---

### 提示词结构模板

#### 通用模板
```
[景别]，[环境]。
[主体描述]，[动作/状态]。
[光线描述]，[光影效果]。
[角度/构图说明]。
[氛围/情绪]。
```

#### 写实场景模板
```
写实风格，[景别]。[环境：时间、地点]。
[主体]，[表情/动作/状态]。
[光源]从[位置]照来，[光影效果]。
[景深效果说明]。
氛围[情绪]。
```

#### 动作场景模板
```
[景别]，[动作]的瞬间。
[主体]，[肢体位置、运动方向]。
[环境元素：碎片/尘土/水花]。
[角度]，[角度效果]。
[光线]。氛围[情绪]。
```

#### 对话/对峙场景模板
```
[景别]，[环境]。
[人物A]与[人物B][位置关系]。
[人物A状态]，[人物B状态]。
[光线如何区分/连接两人]。
[构图效果]。氛围[情绪]。
```

#### 情绪特写模板
```
特写，[主体的具体部位]。
[细节描述：皱纹/伤痕/表情/动作]。
[光质]从[方向]照来，[光影强化情绪]。
背景[虚化/暗化]。
传达出[内在情绪/心理状态]。
```

#### 建立镜头模板
```
[极远景/远景]，[地点/世界观]。
[环境宏观描述：地形/建筑/天气]。
[画面小元素：人物剪影/车辆等]。
[光线/时间段]，[天空/云层/雾气]。
构图强调[空旷/压迫/神秘]。氛围[情绪]。
```

---

### 影视术语自然语言转换参考

#### 景别写法
- 极远景 → "极远景，[地点]。" / "极远景，[环境全貌]。"
- 远景 → "远景，[场景全貌]。"
- 全景 → "全景，[角色]从头到脚可见。"
- 中景 → "中景，[角色]腰部以上。"
- 近景 → "近景，[角色]面部。"
- 特写 → "特写，[具体部位/物件]。"
- 极特写 → "极特写，[眼睛/嘴唇/手指等细节]。"

#### 角度写法
- 平视 → "平视。" / 不写默认平视
- 俯拍 → "俯拍，[主体]显得渺小/脆弱。"
- 仰拍 → "仰拍，[主体]显得威严/高大。"
- 荷兰角 → "略微倾斜的荷兰角，不安感。"
- 主观视角 → "主观视角，[角色]眼中所见。"

#### 光线写法
- 硬光 → "硬光，轮廓分明的阴影，高对比。"
- 柔光 → "柔光包裹，阴影淡化。"
- 逆光 → "逆光，人物轮廓发光，面部剪影。"
- 顶光 → "顶光，眼窝下刻出深影。"
- 侧光 → "侧光雕塑面部，半明半暗。"

#### 色调写法
- 冷色调 → "冷蓝灰色调。" / "冷色调，冷漠孤立。"
- 暖色调 → "暖金琥珀色调。" / "暖色调，舒适怀旧。"
- 低饱和 → "低饱和，沉郁写实。"
- 高对比 → "高对比，深黑与高光。"

#### 情绪写法
- 直接用短句收尾，不需要"氛围是..."
- 紧张 → "一触即发。" / "紧张对峙。"
- 忧郁 → "沉静忧郁。" / "无言的悲伤。"
- 宁静 → "安详平和。" / "静谧。"
- 不祥 → "不祥的气息。" / "危险逼近。"
- 希望 → "一丝希望。" / "黑暗中的微光。"

---

### Gemini 特有参数说明

#### 画幅比例（Aspect Ratio）
- 可用比例：1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
- 16:9：标准宽银幕，适合大多数影视分镜
- 21:9：超宽银幕，适合史诗感建立镜头
- 9:16：竖屏，适合移动端短视频
- 在提示词中可用自然语言描述："Horizontal widescreen format" 或 "Vertical portrait orientation"

#### 分辨率（仅 Gemini 3 Pro / Nano Banana Pro）
- 1K（默认）：约 1024px
- 2K：约 2048px
- 4K：约 4096px
- 高分辨率适合需要放大查看细节的场景

#### 模型选择建议
- **Gemini 2.5 Flash Image（Nano Banana）**：
  - 速度快、成本低
  - 适合快速迭代、批量生成
  - 分辨率最高 1024px
- **Gemini 3 Pro Image Preview（Nano Banana Pro）**：
  - 质量更高、支持复杂指令
  - 内置 Thinking 过程优化构图
  - 支持 Google Search 实时信息
  - 支持最高 4K 分辨率
  - 适合最终成品输出

---

### 常见问题与优化技巧

#### 人物一致性
- 使用参考图片（垫图）时，明确描述要保留的元素
- 例："保持参考图片中的同一角色——一位三十多岁的女性，黑色短发，左脸颊有一道明显的伤疤..."

#### 避免模糊输出
- 具体化所有描述，避免抽象词汇
- 错误："一个戏剧性的场景"
- 正确："一束来自头顶的聚光灯照亮场景，在地板上投下长长的阴影"

#### 控制画面复杂度
- 分镜通常需要清晰的视觉焦点
- 明确指出主体、次要元素、背景的层次关系
- 使用"焦点在于..."、"背景中..."、"前景部分可见..."

#### 迭代优化
- Gemini 支持多轮对话式编辑
- 初次生成后可要求："把光线调得更戏剧化"、"把角色稍微往左移"、"背景加一些雾气"

---

## 第三部分：图生视频动态提示词方法论

### 第一性原则

#### 图片已见原则
- AI 能"看到"输入图片，不需要重复描述图片内容
- 只描述"变化"：动作、运动、情绪转变
- 重复描述图片内容会导致运动减少或异常

#### 简洁优先原则
- 最佳长度：50-200 字符（英文）
- 聚焦 2-3 个核心元素
- 信息过载会导致模型困惑

#### 具体动作原则
- 用具体的物理动作，避免抽象概念
- "hair flowing in wind" ✓
- "embodies the essence of freedom" ✗

#### 运动限制原则
- 镜头运动：最多 1-2 种
- 主体运动：最多 1-2 种
- 过多运动会产生混乱

---

### 提示词结构

#### 基本公式
```
镜头运动 + 主体动作 + 速度/节奏 + 氛围/风格
```

#### 完整公式（复杂场景）
```
镜头运动 + 主体动作 + 环境动态 + 速度/节奏 + 氛围/风格 + 技术参数
```

#### 示例
- 基本：Camera slowly pushes in while subject turns head
- 完整：Slow dolly in, subject turns head, hair flowing gently in wind, golden hour lighting, cinematic 24fps

---

### 镜头运动词汇库

#### 推拉类（Dolly）
- dolly in / push in：推近，聚焦、紧张、亲密
- dolly out / pull back：拉远，揭示、疏离、结束感
- dolly zoom / vertigo effect：眩晕效果，心理冲击

#### 横纵摇类（Pan/Tilt）
- pan left / pan right：横摇，环顾、跟随水平运动
- tilt up / tilt down：纵摇，强调高度、规模、威严
- whip pan：快速横摇，转场、惊讶

#### 环绕类（Orbit/Arc）
- orbit around subject：环绕主体，立体感、动感
- arc shot：弧形运动，戏剧性、强调
- 180-degree orbit：半环绕，常用于对话、对峙
- 360-degree orbit：全环绕，产品展示、英雄时刻

#### 跟拍类（Tracking）
- tracking shot：跟随主体移动
- follow from behind：背后跟拍
- side tracking：侧面跟拍
- leading shot：前方引导

#### 变焦类（Zoom）
- zoom in：变焦推近，强调、戏剧性
- zoom out：变焦拉远，揭示全貌
- slow zoom：缓慢变焦，悬疑、张力

#### 升降类（Crane/Jib）
- crane up / rising shot：上升，史诗感、希望
- crane down / descending shot：下降，压迫、沉重
- aerial / drone shot：航拍，规模、全景

#### 手持与稳定（Handheld/Stabilized）
- handheld：手持，真实感、紧张、纪录片风格
- steady / locked camera：固定机位，稳定、庄重
- floating camera：漂浮感，梦幻、超现实

#### 焦点类（Focus）
- rack focus：焦点转移，引导注意力
- shallow depth of field：浅景深，突出主体
- deep focus：深焦，环境信息丰富

---

### 主体动作词汇库

#### 面部动作
- eyes open slowly：缓慢睁眼
- subtle smile forming：微笑浮现
- gaze shifts：目光转移
- eyebrows raise：眉毛上扬
- blinks naturally：自然眨眼
- expression transitions from X to Y：表情从X转为Y

#### 头部动作
- head turns：转头
- head tilts slightly：微微歪头
- nods slowly：缓慢点头
- looks up / down / away：抬头/低头/移开视线

#### 身体动作
- breathing motion：呼吸起伏
- shoulders rise and fall：肩膀起伏
- leans forward / back：前倾/后仰
- stands up / sits down：站起/坐下
- walks forward / toward camera：向前走/走向镜头
- reaches out hand：伸出手

#### 手部动作
- hand raises：举手
- fingers move：手指动作
- grips tighter：握紧
- gestures while speaking：说话时比划

#### 环境互动
- hair flowing in wind：头发随风飘动
- clothes rustling：衣服飘动
- fabric billowing：布料鼓起
- water splashing：水花飞溅
- leaves falling：落叶飘落
- smoke rising：烟雾升起
- dust particles floating：尘埃飘浮

---

### 速度与强度修饰词

#### 缓慢/轻柔
- slowly, gently, gradually, softly
- subtle, slight, delicate
- natural, organic, barely perceptible
- micro-movements, minimal motion

#### 中等/自然
- smoothly, steadily, naturally
- moderate, balanced, controlled
- fluid, flowing, continuous

#### 快速/强烈
- quickly, rapidly, suddenly
- dramatic, bold, powerful, intense
- explosive, dynamic, energetic
- sweeping, grand, epic

---

### 氛围与风格词汇

#### 电影风格
- cinematic, filmic, movie-quality
- blockbuster style, Hollywood quality
- indie film aesthetic
- documentary style

#### 导演风格（参考）
- Christopher Nolan cinematography：史诗、庄重
- David Fincher style：悬疑、精准
- Terrence Malick aesthetic：诗意、自然光
- Wes Anderson style：对称、色彩饱和

#### 情绪氛围
- dramatic, intense, suspenseful
- romantic, dreamy, nostalgic
- mysterious, eerie, haunting
- joyful, energetic, uplifting
- melancholic, somber, contemplative

#### 技术参数（可选）
- 24fps：电影感
- 60fps：流畅、慢动作素材
- slow motion：慢动作
- film grain：胶片颗粒感
- lens flare：镜头光晕
- bokeh：背景虚化光斑

---

### 禁忌规则

#### 绝对禁忌
- ❌ 否定句（No movement, Don't zoom）
  → AI 不理解否定，可能产生相反效果
  → ✓ 用肯定句：The camera stays still / locked camera

- ❌ 重复图片内容
  → 会导致运动减少或静止
  → ✓ 只描述动作变化

- ❌ 抽象概念（embodies freedom, manifests joy）
  → AI 无法解释抽象意图
  → ✓ 用具体物理动作

- ❌ 多重场景变化
  → 模型无法处理复杂转场
  → ✓ 单一场景、单一动作链

#### 避免事项
- ⚠️ 超过 2 种镜头运动组合
- ⚠️ 超过 2 种主体运动组合
- ⚠️ 过长提示词（超过 300 字符）
- ⚠️ 违反物理规律的动作
- ⚠️ 与图片内容矛盾的描述

---

### 提示词模板

#### 人物肖像动态化
```
[镜头运动], [面部动作], [环境动态], [氛围]
```
示例：Slow dolly in, eyes open slowly, hair flowing gently in wind, cinematic lighting

#### 产品展示
```
[环绕运动], [光影变化], [材质强调], [风格]
```
示例：360-degree orbit around product, reflections dancing on surface, premium feel, Apple commercial style

#### 动作场景
```
[跟拍运动], [主体动作], [环境反应], [节奏]
```
示例：Tracking shot following subject, walking forward confidently, dust particles flying, high energy

#### 情绪转变
```
[镜头运动], [表情变化], [光影配合], [风格参考]
```
示例：Slow zoom in, expression transitions from neutral to smile, warm lighting enhancement, intimate portrait feel

#### 环境氛围
```
[镜头运动], [环境动态], [氛围元素], [风格]
```
示例：Slow pan across landscape, clouds drifting, golden hour lighting, epic cinematic scale

---

### 从分镜到动态提示词的转化

#### 输入
- Beat Board 九宫格提示词（关键帧）
- Sequence Board 四宫格提示词（段落展开）

#### 输出
- 每个 Beat Anchor 一组 Motion Prompt
- 每组 5 个：1 关键帧 + 4 四宫格
- 共 9 组 45 个

#### 转化步骤

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

#### 转化示例
四宫格描述：
```
中景，教室内，林书白站在窗边，阳光斜射进来，他缓缓转头看向门口
```

Motion Prompt：
```
Slow pan, subject turns head toward door, sunlight streaming through window, cinematic
```

---

## 跨体系协作工作流

### 标准工作流

1. **Gemini 生成参考图**
   - 使用 Gemini 图像生成提示词方法论
   - 生成人物设定图、场景环境图
   - 输出：静态参考图（character-prompts.md, scene-prompts.md）

2. **Seedance 2.0 生成动态视频**
   - 使用 Seedance 2.0 提示词方法论
   - 引用步骤1生成的参考图（@图片1, @图片2...）
   - 输出：动态视频片段（4-15秒）

### 图生视频增强工作流

1. **Gemini 生成关键帧**
   - 使用 Gemini 生成 Beat Board 九宫格（9个关键帧）
   - 使用 Gemini 生成 Sequence Board 四宫格（每个 Beat 的4个展开帧）

2. **图生视频工具动态化**
   - 使用图生视频动态提示词方法论
   - 为每个关键帧编写 Motion Prompt
   - 输出：短视频片段（2-5秒）

3. **后期剪辑拼接**
   - 将所有片段按 Beat 顺序拼接
   - 添加转场、音效、配乐
   - 输出：完整视频

---

## 质量检查清单

### Seedance 2.0 提示词检查
- [ ] 每个 @引用 都有明确的用途说明
- [ ] 素材数量未超过平台限制（图片≤9，视频≤3，音频≤3，总≤12）
- [ ] 提示词采用叙事描述式，非关键词堆叠
- [ ] 未重复描述参考图中已有的静态内容
- [ ] 节拍密度符合约束（1拍≈2.5秒）
- [ ] 头尾安全区（前后0.5s）未放置关键内容
- [ ] 时长与内容密度匹配
- [ ] 无否定句、无抽象概念
- [ ] 音频设计完整（BGM、音效、对白）

### Gemini 图像提示词检查
- [ ] 采用叙事描述式，非关键词堆叠
- [ ] 摄影术语融入自然语言，非孤立列出
- [ ] 情绪通过具体视觉表现传达，非抽象词汇
- [ ] 景别、角度、光线、色调描述完整
- [ ] 画幅比例符合需求（16:9 / 9:16 / 21:9）
- [ ] 分辨率选择合理（1K快速迭代 / 4K最终输出）
- [ ] 人物一致性描述明确（如使用垫图）

### 图生视频动态提示词检查
- [ ] 未重复描述图片中已有内容
- [ ] 提示词长度控制在50-200字符
- [ ] 聚焦2-3个核心元素
- [ ] 镜头运动≤2种，主体运动≤2种
- [ ] 无否定句、无抽象概念
- [ ] 动作符合物理规律
- [ ] 与输入图片内容无矛盾
- [ ] 速度修饰词使用恰当

---

## 参考资源

### 相关文档
- `08-camera-and-cinematography.md`：镜头语言与摄影技术
- `09-storyboard-methodology.md`：分镜方法论
- `10a-action-dialogue-scenes.md`：动作与对话场景设计
- `10b-atmosphere-fantasy.md`：氛围营造与奇幻视觉设计
- `10c-suspense-montage.md`：悬疑惊悚与蒙太奇设计

### 工具平台
- **Seedance 2.0**：火山方舟 Doubao-Seedance-2.0
- **Gemini 图像生成**：Nano Banana / Nano Banana Pro
- **图生视频工具**：Runway, Kling, Pika 等

---

---

