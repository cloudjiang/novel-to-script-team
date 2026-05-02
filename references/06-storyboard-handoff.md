# 分镜桥接规范

## 前置

1. 剧本已通过业务审核
2. 剧本已通过合规审核
3. 角色与场景命名稳定

## 两种桥接流

### 1. 标准分镜流（Film Storyboard）

**适用场景**：传统影视分镜需求，需要静态分镜图 + 图生视频提示词

**工作流**：Beat 拆解 → Beat Board（九宫格）→ Sequence Board（四宫格）→ Motion Prompt

**产物**：
- `outputs/{剧本名}/storyboard/ep<N>/beat-breakdown.md` — 节拍拆解表
- `outputs/{剧本名}/storyboard/ep<N>/beat-board.md` — Beat Board 九宫格提示词
- `outputs/{剧本名}/storyboard/ep<N>/sequence-board.md` — Sequence Board 四宫格提示词
- `outputs/{剧本名}/storyboard/ep<N>/motion-prompt.md` — 动态提示词

**执行流程**：
1. **Beat Breakdown（节拍拆解）**
   - `storyboard-artist` 使用 `film-storyboard-skill` 识别叙事曲线的关键拐点
   - 生成 9 个 Beat Anchor，每个对应一个叙事目的和情绪
   - `storyboard-director` 使用 `storyboard-review-skill` 审核

2. **Beat Board（九宫格）**
   - `storyboard-artist` 使用 `film-storyboard-skill` 为 9 个 Beat Anchor 生成九宫格提示词
   - 九宫格用于"选点与定锚"，生成后作为四宫格的参考图片（垫图）
   - `storyboard-director` 使用 `storyboard-review-skill` 审核

3. **Sequence Board（四宫格）**
   - `storyboard-artist` 使用 `film-storyboard-skill` 为每个 Beat Anchor 生成一组四宫格提示词
   - 四宫格必须继承九宫格对应格的人物/场景/光色描述
   - `storyboard-director` 使用 `storyboard-review-skill` 审核

4. **Motion Prompt（动态提示词）**
   - `animator` 使用 `animator-skill` 为每个关键帧和四宫格生成动态提示词
   - 用于 Runway、Kling、Pika 等 AI 视频工具
   - `storyboard-director` 使用 `storyboard-review-skill` 审核

### 2. Seedance 流（Seedance Storyboard）

**适用场景**：Seedance 2.0 文生视频，需要可直接复制到 Seedance 平台的提示词脚本

**工作流**：导演讲戏分析 → 服化道设计 → Seedance 2.0 提示词

**产物**：
- `outputs/{剧本名}/storyboard/ep<N>/01-director-analysis.md` — 导演分析（讲戏本 + 人物清单 + 场景清单）
- `outputs/{剧本名}/assets/character-prompts.md` — 人物提示词（跨集累积）
- `outputs/{剧本名}/assets/scene-prompts.md` — 场景提示词（跨集累积）
- `outputs/{剧本名}/storyboard/ep<N>/02-seedance-prompts.md` — Seedance 2.0 提示词脚本

**执行流程**：
1. **Director Analysis（导演分析）**
   - `storyboard-director` 使用 `director-skill` 将剧本转化为导演讲戏本
   - 拆解剧情点（P01、P02...），每个剧情点是一个完整的叙事段落
   - 提取人物清单和场景清单，标注素材状态（新增/复用/变体）
   - `storyboard-director` 使用 `script-analysis-review-skill` 自审

2. **Art Design（服化道设计）**
   - `art-designer` 使用 `art-design-skill` 为人物和场景生成提示词
   - 人物提示词：左半边面部特写 + 右半边全身三视图，白色背景
   - 场景提示词：宫格图（3×3、3×4 或 4×4），每格一个场景
   - 只为标注为"新增"或"变体"的项设计提示词，"复用"项跳过
   - `storyboard-director` 使用 `art-direction-review-skill` 审核

3. **Seedance Prompts（Seedance 提示词）**
   - `storyboard-artist` 使用 `seedance-storyboard-skill` 将导演讲戏转化为 Seedance 2.0 提示词
   - 使用 @引用语法关联人物和场景素材（@图片1、@视频1、@音频1）
   - 每个剧情点 = 一条提示词 = 一次 Seedance 2.0 生成任务
   - `storyboard-director` 使用 `seedance-prompt-review-skill` 审核

## 审核机制

每阶段都执行：**生成 → 导演审核 → 回改 → 复审**

### 审核标准
- 业务审核：叙事结构、视觉质量、技术规范
- 合规审核：真人限制、版权 IP、政治敏感、色情/暴力尺度

### 审核产物
- 每次审核生成 `outputs/{剧本名}/storyboard/ep<N>/review-<stage>.md`
- 记录审核结果（PASS/FAIL）、问题清单、修改建议

### 审核流程
1. 业务审核（使用阶段专属审核技能）
2. 合规审核（使用 `compliance-review-skill`）
3. 两步全 PASS → 进入下一阶段
4. 任一 FAIL → 合并所有修改意见 → agent 一次性修改 → 覆盖写入 → 重新两步审核 → 循环直到全 PASS

## Resumable Subagents 机制

**目的**：确保每个 subagent 的上下文连续，避免重复理解和丢失信息

**状态记录文件**：`.agent-state.json`
```json
{
  "storyboard-director": "<agentId>",
  "storyboard-artist": "<agentId>",
  "art-designer": "<agentId>",
  "animator": "<agentId>"
}
```

**作用域**：同一集内有效，跨集重置

**调用规则**：
- 同一集内首次调用 subagent：正常调用，记录返回的 agentId
- 同一集内后续调用同一个 subagent：使用 resume 参数恢复 agent
- 跨集时重置：进入新一集时，清空 `.agent-state.json` 中所有 agentId

## 工程约束

### 标准分镜流
- 九宫格用于"选点与定锚"，生成后作为四宫格的参考图片（垫图）
- 四宫格生成时，使用九宫格对应格作为参考图片输入
- 四宫格提示词必须继承九宫格对应格的人物/场景/光色描述

### Seedance 流
- 平台约束（单条提示词维度）：
  - 图片 ≤ 9 张 / 条
  - 视频 ≤ 3 个 / 条
  - 音频 ≤ 3 个 / 条
  - 总文件数 ≤ 12 个 / 条
- 时长控制：Seedance 2.0 单次生成 4-15 秒
- 节拍密度：每个连续镜头内 1 拍 ≈ 2.5 秒屏幕时间
- 头尾安全区：每次生成前 0.5s 和后 0.5s 为安全区，不放关键内容

## 成功标准

### 标准分镜流
1. 节拍拆解识别 9 个关键拐点
2. 九宫格提示词保持视觉风格统一
3. 四宫格提示词继承九宫格对应格的描述
4. 动态提示词简洁、具体、可执行（50-200 字符）
5. 所有阶段通过导演审核

### Seedance 流
1. 导演讲戏本每个剧情点至少 3-5 句话，有足够的视觉信息
2. 人物清单和场景清单的外观关键词足够具体
3. 素材状态标注准确（新增/复用/变体）
4. Seedance 提示词使用叙事描述式，不要关键词堆叠
5. @引用语法正确，明确说明每个引用的作用
6. 所有阶段通过导演审核

## 错误处理

1. 剧本不存在 → 提示用户先执行 `~write N`
2. 剧本未通过审核 → 提示用户先执行 `~review N`
3. 审核 FAIL 超过 3 次 → 暂停流程，提示用户介入
4. 文件写入失败 → 检查目录权限，重试
5. 上下文窗口溢出 → 跨集时重置 `.agent-state.json`，清空所有 agentId

## 参考文档

- `08-camera-and-cinematography.md` — 镜头与摄影技巧
- `09-storyboard-methodology.md` — 分镜方法论
- `10a-action-dialogue-scenes.md` — 动作与对话场景设计
- `10b-atmosphere-fantasy.md` — 氛围营造与奇幻视觉设计
- `10c-suspense-montage.md` — 悬疑惊悚与蒙太奇设计
- `11a-seedance-prompt-methodology.md` — Seedance 2.0 提示词方法论
- `11b-image-motion-prompt.md` — 图像与动态提示词方法论
- `11c-sora2-rhythm-control.md` — Sora2 方法论与节奏控制
- `12-genre-specific-techniques.md` — 类型化技巧
