# Agent 日志记录规范

## 概述

本文档定义了所有 Agent 的统一日志记录规范，确保执行过程可追溯、可调试、可分析。

## 日志目录结构

```
outputs/{剧本名}/
├── logs/
│   ├── knowledge-curator.log
│   ├── novel-analyzer.log
│   ├── insight-architect.log
│   ├── episode-architect.log
│   ├── emotion-architect.log
│   ├── script-writer.log
│   ├── visual-storyteller.log
│   ├── script-comparator.log
│   ├── review-director.log
│   ├── continuity-recorder.log
│   ├── storyboard-director.log
│   ├── storyboard-artist.log
│   ├── storyboard-coach.log
│   ├── art-designer.log
│   ├── animator.log
│   └── image-generator.log
```

## 日志格式规范

### 基本结构

每个 Agent 的日志文件采用 Markdown 格式，包含以下结构：

```markdown
# {Agent 名称} 执行日志

---

## [{时间戳}] {任务名称}

**任务类型**：{analyze / plan / write / review / storyboard / etc.}
**触发命令**：{~analyze / ~write 1 / etc.}
**输入**：
- 参数1：值1
- 参数2：值2

**执行步骤**：
1. 步骤1描述
2. 步骤2描述
3. ...

**输出文件**：
- `outputs/{剧本名}/path/to/file1.md`
- `outputs/{剧本名}/path/to/file2.md`

**关键决策**：
- 决策1：原因
- 决策2：原因

**结果**：SUCCESS / FAIL
**备注**：补充说明

---
```

### 必需字段

每条日志记录必须包含以下字段：

1. **时间戳**：格式为 `YYYY-MM-DD HH:MM:SS`（如：`2026-03-15 10:30:15`）
2. **任务名称**：简短描述任务内容（如：`写作第1集`、`审核第1集`）
3. **任务类型**：任务的类型标识（如：`analyze`、`plan`、`write`、`review`、`storyboard`）
4. **触发命令**：触发此任务的命令（如：`~analyze`、`~write 1`、`~storyboard-seedance 1`）
5. **输入**：任务的输入参数（列表形式，包含剧本名、集数、依赖文件等）
6. **执行步骤**：任务执行的关键步骤（有序列表，描述清晰）
7. **输出文件**：任务生成的文件列表（完整路径）
8. **关键决策**：任务中的重要决策及其原因（列表形式）
9. **结果**：任务执行结果（`SUCCESS` 或 `FAIL`）
10. **备注**：补充说明（可选，用于记录特殊情况或后续行动）

### 记录时机

Agent 应在以下时机记录日志：

1. **任务开始**：记录时间戳、任务名称、任务类型、触发命令、输入参数
2. **关键步骤**：记录重要的中间步骤（如检索、分析、生成、审核）
3. **任务完成**：记录输出文件、关键决策、结果状态、备注

### 日志追加规则

- **同一集内多次调用**：追加到日志文件（如回改时）
- **跨集调用**：追加到日志文件（按时间顺序记录所有集的执行）
- **任务分隔**：每个任务开始时添加分隔线 `---`，便于区分不同任务

### 时间戳格式

统一使用：`YYYY-MM-DD HH:MM:SS`

示例：
- `2026-03-15 10:30:15`
- `2026-03-15 14:22:03`

便于排序和时间计算，与 ISO 8601 标准兼容。

### 敏感信息处理

日志中不应包含：
- API 密钥（如 nano banana API key）
- 用户个人信息
- 完整的文件内容（仅记录文件路径）

### 错误处理

当 Agent 执行失败时：
- 必须记录 `FAIL` 状态
- 必须记录错误原因和堆栈信息
- 必须记录失败时的输入参数（便于复现）

## 日志示例

### 示例 1：script-writer 日志

```markdown
# script-writer 执行日志

---

## [2026-03-15 10:30:15] 写作第1集

**任务类型**：write
**触发命令**：~write 1
**输入**：
- 剧本名：逼我离开我成了道门天师你哭什么
- 集数：1
- 分集规划：`outputs/逼我离开我成了道门天师你哭什么/planning/分集目录.md`
- 角色档案：`outputs/逼我离开我成了道门天师你哭什么/analysis/角色档案.md`

**执行步骤**：
1. 读取分集规划，提取第1集关键信息（类型：复仇、情绪：愤怒、场景：萧家驱逐）
2. 使用 hit-script-retrieval-skill 检索爆款剧本
   - 查询关键词："重生 复仇 豪门 打脸"
   - 检索结果：5个相关剧本（male 频道）
   - 参考剧本：《重生后我成了豪门继承人》、《复仇千金归来》等
3. 分析参考剧本特征
   - 平均句长：12.3 字符
   - 对话比：73%
   - 视觉标记密度：4.2 个/100字
   - 网文感关键词：冷笑、嗤笑、眼神一冷等
4. 读取洞察报告，理解核心冲突
   - 主流叙事：被抛弃的孩子渴望被爱
   - 隐藏真相：真正的家人一直在等他
   - 核心冲突：虚假的豪门 vs 真实的亲情
5. 创作第1集剧本（3个场景）
   - 场景1：重生闪回（建立悬念）
   - 场景2：萧家驱逐（冲突爆发）
   - 场景3：改名离开（反转钩子）
6. 使用 style-analysis-skill 分析生成剧本
   - 句长：12.1 字符（符合目标）
   - 对话比：75%（符合目标）
   - 视觉标记密度：4.5 个/100字（符合目标）

**输出文件**：
- `outputs/逼我离开我成了道门天师你哭什么/scripts/ep01.md`
- `outputs/逼我离开我成了道门天师你哭什么/review/style-analysis-ep01.md`

**关键决策**：
- 选择 male 频道检索（原因：主角为男性，复仇逆袭题材）
- 保留原著"巴掌"情节（原因：符合人物性格，增强冲突）
- 结尾设置"回头看萧宏"钩子（原因：暗示未来反转）

**结果**：SUCCESS
**备注**：等待 review-director 审核

---
```

### 示例 2：review-director 日志

```markdown
# review-director 执行日志

---

## [2026-03-15 11:00:30] 审核第1集

**任务类型**：review
**触发命令**：~review 1
**输入**：
- 剧本名：逼我离开我成了道门天师你哭什么
- 集数：1
- 剧本文件：`outputs/逼我离开我成了道门天师你哭什么/scripts/ep01.md`
- 风格分析：`outputs/逼我离开我成了道门天师你哭什么/review/style-analysis-ep01.md`

**执行步骤**：
1. 读取洞察报告，理解核心冲突
2. 执行业务审核（使用 script-review-skill）
   - 场景数量：3个（PASS）
   - 冲突+反转+悬念：完整（PASS）
   - 称呼规范：一致（PASS）
   - 台词口语化：短句为主（PASS）
   - 情绪段落：完整（PASS）
   - 信息增量：充足（PASS）
   - 一致性锚点：清晰（PASS）
3. 执行合规审核（使用 compliance-review-skill）
   - 暴力程度：非暴力冲突（PASS）
   - 伦理边界：揭露式而非美化式（PASS）
   - 敏感内容：无��感内容（PASS）
4. 执行对比审核（使用 comparative-review-skill）
   - 句长差异：+0.2 字符（PASS）
   - 对话比差异：+2%（PASS）
   - 视觉标记密度差异：+0.3 个/100字（PASS）
   - 网文感关键词：使用充分（PASS）

**输出文件**：
- `outputs/逼我离开我成了道门天师你哭什么/review/review-log.md`（追加）
- `outputs/逼我离开我成了道门天师你哭什么/review/comparative-review-ep01.md`

**关键决策**：
- 业务审核 PASS（原因：所有检查项符合标准）
- 合规审核 PASS（原因：无违规内容）
- 对比审核 PASS（原因：风格指标接近参考剧本）

**结果**：SUCCESS（第1集复核通过）
**备注**：通知 continuity-recorder 更新项目记忆

---
```

### 示例 3：storyboard-artist 日志

```markdown
# storyboard-artist 执行日志

---

## [2026-03-15 15:20:45] 生成 Seedance 提示词（第1集）

**任务类型**：storyboard
**触发命令**：~storyboard-seedance 1
**输入**：
- 剧本名：逼我离开我成了道门天师你哭什么
- 集数：1
- 剧本文件：`outputs/逼我离开我成了道门天师你哭什么/scripts/ep01.md`
- 导演分析：`outputs/逼我离开我成了道门天师你哭什么/storyboard/ep01/01-director-analysis.md`
- 角色提示词：`outputs/逼我离开我成了道门天师你哭什么/assets/character-prompts.md`
- 场景提示词：`outputs/逼我离开我成了道门天师你哭什么/assets/scene-prompts.md`

**执行步骤**：
1. 读取剧本和导演分析，理解场景结构
2. 读取角色和场景提示词，准备资产引用
3. 使用 seedance-storyboard-skill 生成 Seedance 2.0 提示词
   - 场景1：重生闪回（3条提示词）
   - 场景2：萧家驱逐（5条提示词）
   - 场景3：改名离开（2条提示词）
   - 总计：10条提示词
4. 为每条提示词选择生成模式
   - T2V：6条（纯文本生成）
   - I2V-首帧：3条（需要首帧参考图）
   - 首尾帧：1条（需要首尾帧参考图）
5. 生成帧图需求清单
   - 首帧需求：3个（F01, F03, F07）
   - 尾帧需求：1个（F10）
   - 总计：4个帧图需求

**输出文件**：
- `outputs/逼我离开我成了道门天师你哭什么/storyboard/ep01/02-seedance-prompts.md`
- `outputs/逼我离开我成了道门天师你哭什么/storyboard/ep01/03-frame-requests.md`

**关键决策**：
- 场景1使用 T2V（原因：闪回场景，无需精确控制）
- 场景2使用 I2V-首帧（原因：需要精确控制人物表情和动作）
- 场景3使用首尾帧（原因：需要控制离开的起点和终点）

**结果**：SUCCESS
**备注**：等待 storyboard-director 审核，然后生成帧图

---
```

### 示例 4：image-generator 日志

```markdown
# image-generator 执行日志

---

## [2026-03-15 16:10:22] 生成帧图（第1集）

**任务类型**：image-generation
**触发命令**：~generate-images 1
**输入**：
- 剧本名：逼我离开我成了道门天师你哭什么
- 集数：1
- 帧图需求清单：`outputs/逼我离开我成了道门天师你哭什么/storyboard/ep01/03-frame-requests.md`
- API 配置：nano banana API（已配置）

**执行步骤**：
1. 读取帧图需求清单，提取 4 个帧图需求
2. 使用 image-generation-skill 调用 nano banana API
   - F01：萧凌重生闪回（首帧）
   - F03：萧家客厅冲突（首帧）
   - F07：萧凌愤怒表情（首帧）
   - F10：萧凌离开萧家（尾帧）
3. 生成帧图文件
   - `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F01.png`
   - `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F03.png`
   - `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F07.png`
   - `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F10.png`
4. 更新 Seedance 提示词文件，添加帧图 @引用
   - 提示词 1：@frame-F01.png
   - 提示词 3：@frame-F03.png
   - 提示词 7：@frame-F07.png
   - 提示词 10：@frame-F10.png（首尾帧）

**输出文件**：
- `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F01.png`
- `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F03.png`
- `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F07.png`
- `outputs/逼我离开我成了道门天师你哭什么/images/frames/ep01/frame-F10.png`
- `outputs/逼我离开我成了道门天师你哭什么/storyboard/ep01/02-seedance-prompts.md`（更新）

**关键决策**：
- 使用 nano banana API（原因：已配置 API key，自动化生成）
- 帧图分辨率：1920x1080（原因：符合 Seedance 2.0 要求）
- 帧图风格：写实风格（原因：符合剧本定位）

**结果**：SUCCESS
**备注**：帧图已生成并引用到 Seedance 提示词中

---
```

### 示例 5：失败案例日志

```markdown
# script-writer 执行日志

---

## [2026-03-15 10:30:15] 写作第1集

**任务类型**：write
**触发命令**：~write 1
**输入**：
- 剧本名：逼我离开我成了道门天师你哭什么
- 集数：1
- 分集规划：`outputs/逼我离开我成了道门天师你哭什么/planning/分集目录.md`
- 角色档案：`outputs/逼我离开我成了道门天师你哭什么/analysis/角色档案.md`

**执行步骤**：
1. 读取分集规划，提取第1集关键信息
2. 使用 hit-script-retrieval-skill 检索爆款剧本
   - 查询关键词："重生 复仇 豪门 打脸"
   - 检索结果：0个相关剧本（检索失败）
   - 错误信息：`improved_hybrid_search.py` 未找到索引文件

**输出文件**：
- 无（任务失败）

**关键决策**：
- 无（任务失败）

**结果**：FAIL
**备注**：检索系统故障，需要修复索引文件后重试

---
```

## 与现有日志的关系

### 保留现有日志

- `outputs/{剧本名}/review/review-log.md`：保留，用于审核结果的表格化展示
- `outputs/{剧本名}/final-check-report.md`：保留，用于最终检查报告

### 新日志的定位

- `outputs/{剧本名}/logs/{agent-name}.log`：用于记录 Agent 执行过程的详细信息
- 两者互补，不冲突

## 实施要点

### 日志文件管理

- **日志追加**：同一集内多次调用同一 Agent（如回改）时，追加到日志文件
- **跨集记录**：跨集调用时，追加到日志文件（按时间顺序记录所有集的执行）
- **任务分隔**：每个任务开始时添加分隔线 `---`，便于区分不同任务

### 日志文件大小控制

- 单个日志文件建议不超过 10MB
- 如果日志过大，可以考虑按集分割（如 `script-writer-ep01.log`）
- 或者定期归档旧日志（如移动到 `logs/archive/`）

### 性能考虑

日志记录应该：
- 不阻塞 Agent 执行
- 避免记录过大的数据结构（如完整的剧本内容）
- 仅记录关键信息和文件路径

## 验证清单

执行日志记录时，确保：

- [ ] 日志文件存在于 `outputs/{剧本名}/logs/` 目录
- [ ] 格式符合规范（Markdown + 时间戳 + 结构化内容）
- [ ] 内容完整（输入、步骤、输出、决策、结果）
- [ ] 时间戳格式正确（YYYY-MM-DD HH:MM:SS）
- [ ] 能够通过日志追溯每个 Agent 的执行过程
- [ ] 敏感信息已脱敏（API 密钥、个人信息等）
- [ ] 失败案例记录了错误原因和堆栈信息

## 总结

本规范定义了统一的 Agent 日志记录标准，确保：

1. **可追溯性**：能够追溯每个 Agent 的执行过程
2. **可调试性**：能够定位问题发生的具体步骤
3. **可分析性**：能够分析性能瓶颈和优化空间
4. **一致性**：所有 Agent 使用统一的日志格式
5. **可读性**：日志格式清晰，易于阅读和理解

所有 Agent 必须遵循本规范，确保日志记录的质量和一致性。
