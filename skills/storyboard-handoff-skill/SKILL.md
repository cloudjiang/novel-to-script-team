---
name: storyboard-handoff-skill
description: 分镜交接技能。把通过审核的剧本桥接到标准分镜流或 Seedance 流。协调 storyboard-director、storyboard-artist、art-designer、animator 完成分镜生产。
---

# 分镜交接技能

## 必读
1. `../../references/00-first-principles.md`
2. `../../references/06-storyboard-handoff.md`
3. `../../references/08-camera-and-cinematography.md`
4. `../../references/09-storyboard-methodology.md`
5. `../../references/10a-action-dialogue-scenes.md`
6. `../../references/11a-seedance-prompt-methodology.md`

## 技能说明

分镜交接技能，负责将通过审核的剧本桥接到视频化阶段。提供两种工作流：

1. **标准分镜流（Film Storyboard）**：适用于传统影视分镜需求
   - Beat 拆解 → Beat Board（九宫格）→ Sequence Board（四宫格）→ Motion Prompt
   - 产物：静态分镜图 + 图生视频提示词

2. **Seedance 流（Seedance Storyboard）**：适用于 Seedance 2.0 文生视频
   - 导演讲戏分析 → 服化道设计 → Seedance 2.0 提示词
   - 产物：可直接复制到 Seedance 平台的提示词脚本

## 前置条件

1. 剧本已通过业务审核（`outputs/{剧本名}/review/review-log.md` 中对应集数标记 PASS）
2. 剧本已通过合规审核（`outputs/{剧本名}/review/review-log.md` 中对应集数标记 PASS）
3. 角色与场景命名稳定

## 输入

1. 通过审核的剧本（`outputs/{剧本名}/scripts/ep<N>.md`）
2. 用户指定的工作流类型（film / seedance）
3. 视觉风格（可选，默认：真人风格）

## 输出

### 标准分镜流产物
1. `outputs/{剧本名}/storyboard/ep<N>/beat-breakdown.md` — 节拍拆解表
2. `outputs/{剧本名}/storyboard/ep<N>/beat-board.md` — Beat Board 九宫格提示词
3. `outputs/{剧本名}/storyboard/ep<N>/sequence-board.md` — Sequence Board 四宫格提示词
4. `outputs/{剧本名}/storyboard/ep<N>/motion-prompt.md` — 动态提示词

### Seedance 流产物
1. `outputs/{剧本名}/storyboard/ep<N>/01-director-analysis.md` — 导演分析（讲戏本 + 人物清单 + 场景清单）
2. `outputs/{剧本名}/assets/character-prompts.md` — 人物提示词（跨集累积）
3. `outputs/{剧本名}/assets/scene-prompts.md` — 场景提示词（跨集累积）
4. `outputs/{剧本名}/storyboard/ep<N>/02-seedance-prompts.md` — Seedance 2.0 提示词脚本

## 执行流程

### 前置检查

1. 检查剧本是否存在：`outputs/{剧本名}/scripts/ep<N>.md`
2. 检查审核记录：`outputs/{剧本名}/review/review-log.md`
3. 确认该集已通过业务审核和合规审核
4. 如未通过审核，提示用户先执行 `~review N`

### 工作流选择

询问用户选择工作流类型：
- `film`：标准分镜流（Beat breakdown → Beat Board → Sequence Board → Motion Prompt）
- `seedance`：Seedance 流（Director analysis → Art design → Seedance prompts）

### 标准分镜流（Film Storyboard）

#### 阶段 1：Beat Breakdown（节拍拆解）
1. 调用 `storyboard-artist` 使用 `film-storyboard-skill` 生成节拍拆解表
2. 输出：`outputs/{剧本名}/storyboard/ep<N>/beat-breakdown.md`
3. 调用 `storyboard-director` 使用 `storyboard-review-skill` 审核
4. 如 FAIL，回改并重审，直到 PASS

#### 阶段 2：Beat Board（九宫格）
1. 调用 `storyboard-artist` 使用 `film-storyboard-skill` 生成 Beat Board 九宫格提示词
2. 输出：`outputs/{剧本名}/storyboard/ep<N>/beat-board.md`
3. 调用 `storyboard-director` 使用 `storyboard-review-skill` 审核
4. 如 FAIL，回改并重审，直到 PASS

#### 阶段 3：Sequence Board（四宫格）
1. 调用 `storyboard-artist` 使用 `film-storyboard-skill` 生成 Sequence Board 四宫格提示词
2. 输出：`outputs/{剧本名}/storyboard/ep<N>/sequence-board.md`
3. 调用 `storyboard-director` 使用 `storyboard-review-skill` 审核
4. 如 FAIL，回改并重审，直到 PASS

#### 阶段 4：Motion Prompt（动态提示词）
1. 调用 `animator` 使用 `animator-skill` 生成动态提示词
2. 输出：`outputs/{剧本名}/storyboard/ep<N>/motion-prompt.md`
3. 调用 `storyboard-director` 使用 `storyboard-review-skill` 审核
4. 如 FAIL，回改并重审，直到 PASS

### Seedance 流（Seedance Storyboard）

#### 阶段 1：Director Analysis（导演分析）
1. 调用 `storyboard-director` 使用 `director-skill` 生成导演分析
2. 输出：`outputs/{剧本名}/storyboard/ep<N>/01-director-analysis.md`（包含讲戏本 + 人物清单 + 场景清单）
3. 调用 `storyboard-director` 使用 `script-analysis-review-skill` 自审
4. 如 FAIL，回改并重审，直到 PASS

#### 阶段 2：Art Design（服化道设计）
1. 调用 `art-designer` 使用 `art-design-skill` 生成人物和场景提示词
2. 输出：
   - `outputs/{剧本名}/assets/character-prompts.md`（追加式写入，跨集累积）
   - `outputs/{剧本名}/assets/scene-prompts.md`（追加式写入，跨集累积）
3. 调用 `storyboard-director` 使用 `art-direction-review-skill` 审核
4. 如 FAIL，回改并重审，直到 PASS

#### 阶段 3：Seedance Prompts（Seedance 提示词）
1. 调用 `storyboard-artist` 使用 `seedance-storyboard-skill` 生成 Seedance 2.0 提示词
2. 输出：`outputs/{剧本名}/storyboard/ep<N>/02-seedance-prompts.md`
3. 调用 `storyboard-director` 使用 `seedance-prompt-review-skill` 审核
4. 如 FAIL，回改并重审，直到 PASS

## 审核机制

每个阶段都执行：**生成 → 导演审核 → 回改 → 复审**

审核标准参考：
- `../../references/04-review-gates.md`（业务审核标准）
- `../../references/05-compliance-boundaries.md`（合规审核标准）

审核产物：
- 每次审核生成 `outputs/{剧本名}/storyboard/ep<N>/review-<stage>.md`
- 记录审核结果（PASS/FAIL）、问题清单、修改建议

## 成功标准

1. 前置审核全 PASS（剧本已通过业务 + 合规审核）
2. 每个阶段都通过导演审核
3. 产物完整且符合格式规范
4. 标准流：4 个产物文件齐全
5. Seedance 流：3 个产物文件齐全 + `outputs/{剧本名}/assets/` 下提示词文件更新

## 错误处理

1. 剧本不存在 → 提示用户先执行 `~write N`
2. 剧本未通过审核 → 提示用户先执行 `~review N`
3. 审核 FAIL 超过 3 次 → 暂停流程，提示用户介入
4. 文件写入失败 → 检查目录权限，重试

## 命令示例

```bash
# 标准分镜流
~storyboard-film 1

# Seedance 流
~storyboard-seedance 1

# 查询分镜状态
~storyboard-status
```
