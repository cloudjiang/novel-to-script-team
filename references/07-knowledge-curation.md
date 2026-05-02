# 知识收编规范

## 输入来源

### 标准来源（~ingest）
1. `../sources/legacy-novel-to-script/`
2. `../sources/legacy-novel-to-script-v2/`
3. `../sources/new-tutorials/`
4. `../sources/new-reference-skills/`
5. `../sources/repo-knowledge/`

### 待处理来源（~ingest-pending）
6. `../pending-knowledge/` — 新增知识的临时存放区

**使用场景**：
- 用户提供的新方法论、新教程
- 外部参考资料、案例示例
- 需要批量收编的知识文件

**处理流程**：
1. 用户将待收编文件放入 `pending-knowledge/`
2. 调用 `~ingest-pending` 指令
3. knowledge-curator 自动分析、路由、集成
4. 完成后移动到 `sources/pending-ingested/[日期]/`

## 收编流程

### 标准收编流程（~ingest）
1. 扫描：注册到 `knowledge/source-registry.md`
2. 去重：同主题只保留一个主版本
3. 路由：映射到对应 skill
4. 吸收：更新 `references/*.md` 执行规则
5. 记录：更新 `knowledge/absorption-map-index.md`（索引）和 `knowledge/absorption-map-YYYY-MM.md`（月度详情）

### 批量收编流程（~ingest-pending）
1. **扫描**：列出 `pending-knowledge/` 所有文件
2. **分析**：逐个提取核心知识点
3. **路由**：判断归属位置（references/skills/sources）
4. **集成**：更新对应文件
5. **记录**：更新 `absorption-map-index.md`（索引）和 `absorption-map-YYYY-MM.md`（月度详情）
6. **移动**：将已处理文件移动到 `sources/pending-ingested/[日期]/`
7. **报告**：输出收编总结

## 取舍原则（第一性）

1. 能执行 > 能解释
2. 能验证 > 能感受
3. 能复用 > 一次性灵感
4. 少而硬 > 多而散

## 收编门槛

### A级（references/）
- 必须是核心执行标准
- 至少2个 agent 会用到
- 在工作流中高频使用
- 可直接指导 agent 行为

### B级（references/ 分镜区）
- 必须是分镜或视频化相关执行标准
- 至少1个分镜/视频化 agent 会用到（storyboard-director、storyboard-artist、art-designer、animator）
- 在 ~storyboard-film 或 ~storyboard-seedance 阶段使用
- 目标文件：ref/08、ref/09、ref/10、ref/11、ref/12

### D级（references/ 进阶区）
- 视觉叙事、心理学、剧作理论等进阶知识
- 至少1个 agent 会用到
- 提供深层方法论支撑（非直接执行规则）
- 目标文件：ref/13、ref/14、ref/15、ref/16、ref/17

### C级（sources/）
- 必须是补充参考资料
- 至少1个 agent 会用到
- 在特定场景下使用
- 提供案例或深度方法论

### 拒绝收编标准
以下情况**必须拒绝收编**：
1. **无法明确使用 agent**：无法指定哪个 agent 会用到这个知识
2. **无法明确使用阶段**：无法指定在哪个工作流阶段会用到
3. **与现有知识重复**：与现有知识库内容重复且无明显增量
4. **与工作流无关**：知识内容与小说改编剧本工作流无关
   - 示例：古代文化常识（我们主要做现代网文改编）
   - 示例：好莱坞编剧原则（我们做的是网文改编短剧）
5. **理论性过强**：缺乏可执行性，无法转化为 agent 行为
6. **一次性灵感**：无法复用的个案经验

### 收编前强制5问
在收编任何知识前，必须明确回答以下5个问题：
- **Q1：哪个 agent 会用到？**（必须指定具体 agent 名称，如 script-writer、storyboard-artist）
- **Q2：在哪个阶段会用到？**（必须指定具体工作流阶段，如 ~write、~storyboard-seedance）
- **Q3：现有知识库是否已覆盖？**（如已覆盖且无明显增量，拒绝收编。必须执行 `grep -rn "关键概念" references/*.md`，记录命中文件:行号:摘要。未执行 grep = 自动拒绝）
- **Q4：目标文件行数是否安全？**（执行 `wc -l <目标文件>`，超 800 行警告，超 1200 行禁止追加）
- **Q5：是否存在多文件命中？**（执行 `grep -l "核心概念" references/*.md`，命中 2+ 文件必须选择主文件并说明理由）

如果无法明确回答任何一个问题，**必须拒绝收编**。

## 文件移动规则

### 成功收编
- 目标目录：`sources/pending-ingested/YYYY-MM-DD/`
- 保留原文件名
- 按日期分组

### 拒绝收编
- 目标目录：`sources/pending-ingested/YYYY-MM-DD/rejected/`
- 保留原文件名
- 在报告中说明拒绝原因
- 便于后续人工复核

### 目录结构示例
```
sources/
├── pending-ingested/
│   ├── 2026-03-10/
│   │   ├── 成功收编的文件1.md
│   │   ├── 成功收编的文件2.txt
│   │   └── rejected/
│   │       ├── 拒绝收编的文件1.md（原因：无法明确使用 agent）
│   │       └── 拒绝收编的文件2.md（原因：与现有知识重复）
│   ├── 2026-03-11/
│   │   └── ...
```

## 参考文件健康标准

### 文件大小限制

| 状态 | 行数范围 | 操作 |
|------|---------|------|
| OK | < 800 行 | 正常追加 |
| WARNING | 800-1199 行 | 警告，评估是否需要拆分 |
| OVERSIZED | >= 1200 行 | 禁止追加，必须先拆分 |

### 拆分策略

1. **按主题拆分**：将大文件按独立主题拆分为多个子文件
2. **命名规则**：`XX-原名a.md`、`XX-原名b.md`、`XX-原名c.md`（如 `11a-video-prompt-seedance.md`）
3. **索引更新**：拆分后必须更新 `references/index.md` 和 `knowledge/absorption-map-index.md`
4. **引用更新**：检查所有 agents/ 和 skills/ 中的引用，更新为新文件名

### 当前需关注文件

- `references/10a-action-dialogue-scenes.md` — 动作与对话场景设计（已从 10 拆分）
- `references/10b-atmosphere-fantasy.md` — 氛围营造与奇幻视觉设计（已从 10 拆分）
- `references/10c-suspense-montage.md` — 悬疑惊悚与蒙太奇设计（已从 10 拆分）
- `references/11a-seedance-prompt-methodology.md` — Seedance 2.0 提示词方法论（已从 11 拆分）
- `references/11b-image-motion-prompt.md` — 图像与动态提示词方法论（已从 11 拆分）
- `references/11c-sora2-rhythm-control.md` — Sora2 方法论与节奏控制（已从 11 拆分）
- `references/14-story-psychology.md` — 故事心理学（多维度内容）

## 内容归属边界

易混淆主题的归属对照表，收编时必须参考：

| 主题 | 归属文件 | 不归属 | 区分标准 |
|------|---------|--------|---------|
| 情绪曲线/观众心理 | ref/14（故事心理学） | ref/16（剧作原理） | 14=心理视角，16=结构视角 |
| 冲突设计/矛盾公式 | ref/16（剧作原理） | ref/14（故事心理学） | 16=结构方法，14=心理机制 |
| 节奏控制 | ref/16（剧作原理） | ref/14（故事心理学） | 16=写作节奏，14=情绪节奏 |
| 动作场景设计 | ref/10（场景设计） | ref/13（Show Don't Tell） | 10=场景层面，13=表达手法 |
| 视觉化表达 | ref/13（Show Don't Tell） | ref/10（场景设计） | 13=Show Don't Tell，10=场景技巧 |
| 镜头构图 | ref/08（镜头摄影） | ref/17（光影叙事） | 08=构图运镜，17=光影叙事 |
| 爽感/共鸣设计 | ref/14（故事心理学） | ref/16（剧作原理） | 14=观众心理，16=结构设计 |
| 人设弧光 | ref/16（剧作原理） | ref/14（故事心理学） | 16=角色结构，14=心理共鸣 |

## 冲突处理原则

### 补充优先
- 新知识补充现有规则 → 直接集成
- 新知识是现有规则的细化 → 补充到对应章节

### 替换慎重
- 新知识与现有规则冲突 → 标注"需人工判断"
- 不要自动替换核心规则
- 提供对比分析，由人工决策

### 新增谨慎
- 新知识是全新主题 → 评估是否必要
- 避免知识膨胀，保持"少而硬"原则
