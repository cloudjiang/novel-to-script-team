---
name: knowledge-curation-skill
description: 知识收编技能。将 sources 中知识去重、路由、吸收进 team 内部 references 与 knowledge。
---

# 知识收编技能

## 必读
1. `../../references/index.md`
2. `../../references/07-knowledge-curation.md`
3. `../../knowledge/canon-map.md`

## 执行模式

### 模式1：标准收编（~ingest）
扫描 `sources/` 目录，执行知识整合。

### 模式2：批量收编待处理知识（~ingest-pending）

**触发条件**：收到 `~ingest-pending` 指令

**执行流程**：

#### Step 1：扫描待处理目录
```bash
ls -la ./pending-knowledge/
```
- 列出所有待处理文件
- 识别文件类型（.txt, .md, 目录等）

#### Step 2：逐个分析文件
对每个文件执行：
1. 读取文件内容
2. 提取核心知识点（3-10个）
3. **收编前强制5问**（必须明确回答，否则拒绝收编）：
   - Q1：哪个 agent 会用到这个知识？（必须指定具体 agent 名称，如 script-writer、storyboard-artist）
   - Q2：在哪个阶段会用到？（必须指定具体工作流阶段，如 ~write、~storyboard-seedance）
   - Q3：现有知识库是否已覆盖？（如已覆盖且无明显增量，拒绝收编）。必须执行 `grep -rn "关键概念1\|关键概念2" references/*.md`，记录命中文件:行号:摘要。未执行 grep = 自动拒绝
   - Q4：目标文件行数是否安全？（执行 `wc -l <目标文件>`，超 800 行 [WARNING]，超 1200 行 [OVERSIZED] 禁止追加）
   - Q5：是否存在多文件命中？（执行 `grep -l "核心概念" references/*.md`，命中 2+ 文件必须选择主文件并说明理由）
4. 判断知识类型：
   - 方法论（归属 references/）
   - 执行规则（归属 skills/）
   - 案例示例（归属 sources/）
   - 拒绝收编（无法明确使用场景）

#### 分级示例参考

**A级（references/ 核心区）**：
- ✅ 「节奏呼吸感四步法」→ ref/16（≥2 agent 用，高频）
- ✅ 「共情四步法」→ ref/14（情绪设计核心）
- ❌ 「70个女频梗库」→ 太具体，应为 C 级

**B级（references/ 分镜区）**：
- ✅ 「Seedance 景别运镜组合」→ ref/11
- ✅ 「Beat Board 九宫格方法」→ ref/09

**C级（sources/）**：
- ✅ 「韩国编剧案例分析」→ sources/screenwriting-methodology/
- ✅ 「标题起名30公式」→ sources/screenwriting-methodology/

**D级（references/ 进阶区）**：
- ✅ 「色彩心理学补充」→ ref/15
- ✅ 「光影叙事新技法」→ ref/17

**拒绝**：
- ❌ AI 写作 prompt（与工作流无关）
- ❌ 行业报告/职业规划（无 agent 使用场景）
- ❌ 纯理论无可执行规则

#### Step 3：知识路由分析
为每个知识点生成路由表：
```markdown
| 知识点 | 归属位置 | 集成方式 | 优先级 | 理由 |
|--------|---------|---------|--------|------|
| ... | references/XX.md | 新增/补充/替换 | A/B/C | ... |
```

#### Step 3.5：批量检查点（每 15 个文件）

每处理 15 个文件后输出中间报告：
```markdown
### 批量检查点 #N

**本批文件**：[文件列表]
**VERIFIED**：X 个
**FAILED**：Y 个
**累计进度**：已处理 M / 总计 T

**暂停条件检查**：
- [ ] FAILED >= 3 → 暂停并报告
- [ ] 目标文件 OVERSIZED → 暂停并报告
- [ ] 主题冲突 → 暂停并报告
```

#### Step 4：执行集成
- 使用 Edit 工具更新对应文件
- 遵循"补充优先、替换慎重"原则
- 保持文档结构一致性
- 每次 Edit 后立即执行 `grep -n "唯一短语" <文件>` 确认写入
- 验证成功输出：[VERIFIED] Edit <文件>
- 验证失败重试一次，仍失败标记 [FAILED] Edit <文件> <原因>

#### Step 5：记录集成信息（分区存储）

**月度详情文件** `knowledge/absorption-map-YYYY-MM.md`：
```markdown
## YYYY-MM-DD：批量收编 pending-knowledge

**来源文件**：
- pending-knowledge/1.txt
- pending-knowledge/2.txt
- ...

**集成位置**：
- references/XX.md：新增YY章节
- skills/ZZ/SKILL.md：补充AA规则
- ...

**集成方式**：补充/新增/替换
**优先级**：A/B/C级
```

**索引文件** `knowledge/absorption-map-index.md`：
- 仅追加一行摘要：`| YYYY-MM-DD | N个文件 | A级×M, B级×N, C级×P | 详见 absorption-map-YYYY-MM.md |`
- 更新统计：总收编数、本月收编数、拒绝数

#### Step 6：移动已处理文件
```bash
# 创建日期目录
mkdir -p ./sources/pending-ingested/YYYY-MM-DD/
mkdir -p ./sources/pending-ingested/YYYY-MM-DD/rejected/

# 移动成功收编的文件
mv ./pending-knowledge/[文件名] ./sources/pending-ingested/YYYY-MM-DD/

# 移动拒绝收编的文件
mv ./pending-knowledge/[文件名] ./sources/pending-ingested/YYYY-MM-DD/rejected/
```

**移动规则**：
- ✅ 成功收编：移动到 `sources/pending-ingested/[日期]/`
- ❌ 拒绝收编：移动到 `sources/pending-ingested/[日期]/rejected/`，并在报告中说明原因
- 📁 子目录：整体移动，保持结构

#### Step 7：输出收编报告
```markdown
## 批量收编报告

### 处理统计
- 总文件数：X
- 成功收编：Y
- 拒绝收编：Z
- 已移动文件：X（成功Y + 拒绝Z）

### 成功收编列表
1. [文件名] → [集成位置] → 已移动到 sources/pending-ingested/YYYY-MM-DD/
   - 使用 agent：[agent名称]
   - 使用阶段：[工作流阶段]
2. ...

### 拒绝收编列表
1. [文件名]：[拒绝原因] → 已移动到 sources/pending-ingested/YYYY-MM-DD/rejected/
   - 原因示例：无法明确使用 agent / 与现有知识重复 / 与工作流无关
2. ...

### 知识集成摘要
- 新增章节：X个
- 补充内容：Y处
- 替换内容：Z处
```

#### Step 8：健康检查

收编报告末尾附加健康报告：

```markdown
### 健康检查报告

| 文件 | 行数 | 状态 | 建议 |
|------|------|------|------|
| references/XX.md | NNN | OK/WARNING/OVERSIZED | — / 评估拆分 / 必须拆分 |

### 重叠检测
- grep -l "核心概念A" references/*.md → [命中文件列表]
- 如命中 2+ 文件，标注需要归属确认
```

## 输出
1. `../../knowledge/source-registry.md`
2. `../../knowledge/absorption-map-index.md`
3. `../../knowledge/canon-map.md`
4. 批量收编报告（输出到终端）

## 成功标准
1. 新增来源已注册
2. 每个来源都有归属 skill
3. 吸收结论可追溯
4. **批量收编模式**：所有文件已移动（成功收编 → `sources/pending-ingested/[日期]/`，拒绝收编 → `sources/pending-ingested/[日期]/rejected/`）
5. **收编前强制5问**：每个文件都明确回答了使用 agent、使用阶段、是否重复、目标文件行数、多文件命中
6. **执行验证**：每个 Edit/mv 操作有 [VERIFIED] 标记
7. **5问完整**：每个文件的5问记录完整，Q3 含 grep 证据
8. **健康检查**：报告末尾包含健康检查报告
9. **零 FAILED**：所有操作 VERIFIED，或 FAILED 已说明原因并标记

## 注意事项

### 冲突处理
- 如果新知识与现有知识冲突，标注为"需人工判断"
- 不要自动替换现有的核心规则
- 优先补充而非替换

### 文件移动安全
- 移动前确认文件已成功集成
- 保留原文件名，便于追溯
- 使用日期目录分组，便于管理

### 质量控制
- 只收编可执行的知识（能执行 > 能解释）
- 只收编可验证的知识（能验证 > 能感受）
- 拒绝一次性灵感，只收编可复用的规则
