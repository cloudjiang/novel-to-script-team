# Novel-to-Script-Team

> 多 Agent、多 Skill 的小说改编影视流水线：把长篇小说、故事梗概或短剧素材，系统化转成改编分析、分集规划、剧本、审核报告、分镜方案、图片/视频提示词。

[English README](README_en.md) | [Agent 工作流指南](AGENTS.md) | [MIT License](LICENSE)

## 这是什么

Novel-to-Script-Team 不是单个提示词，而是一套可复用的创作生产线。它把“小说改编”拆成多个专业角色和可检查阶段：先分析题材与可拍性，再抽取核心洞察和情绪曲线，随后按集写作、审核、复核，最后进入分镜和视频提示词交付。

适合场景：

- 小说改短剧、漫剧、短视频连续剧
- 原创故事做分集大纲和样集
- 已有剧本做风格、节奏、合规、视觉化复审
- 剧本文字转分镜、Seedance/Sora/图生视频提示词
- 团队内部沉淀一套可审计、可复跑的 Agent 工作流

## 核心能力

- **结构化改编，而不是一次性提示词**：把小说改编拆成改编分析、洞察提炼、分集规划、情绪设计、剧本写作、审核、连续性维护和分镜视频化，每个阶段都有明确输入、产物、责任 Agent 和回改路径。
- **从原文到视频前置资产**：同一套流程可以产出改编分析、分集大纲、单集剧本、审核报告、人物/场景/道具提示词、分镜方案、帧图需求和视频提示词。
- **改编分析**：提取题材、主线、人物关系、世界规则、核心冲突、可拍性问题，先判断故事适合怎么影视化。
- **洞察与情绪设计**：用“开天眼”方式拆出显性叙事、隐藏真相、爽点/虐点、观众预期，并设计情绪曲线、悬念链路和认知负荷。
- **分集规划与剧本写作**：生成分集目录、单集钩子、推进节奏和短剧/漫剧剧本；写作阶段可检索本地授权爆款剧本，参考节奏、钩子、爽点和表达方式。
- **视觉化改写**：专门检查 Show Don't Tell，把抽象心理描写改成能被镜头拍到的动作、表情、道具、场面和镜头语言。
- **多层审核闭环**：业务审核、合规审核、风格分析、逐一对比、综合复核贯穿流程；未达标时回到对应阶段修改，而不是只在最后给建议。
- **连续性维护**：记录称呼、人设、道具、时间线、伏笔、设定变化，降低长项目跨集漂移。
- **两条分镜视频化路线**：支持标准影视分镜流，也支持面向 Seedance/Sora/图生视频的提示词流。
- **可替换媒体 Provider**：图片生成、图片反推、SkyReels 批处理等脚本均通过 `.env` 或环境变量配置 API Key、Base URL、模型和端点。
- **可恢复的多 Agent 工作台**：通过 `outputs/{剧本名}/.agent-state.json` 保存项目上下文，支持长项目分阶段继续。

## 开源版说明

本仓库提供 Agent/Skill 工作流、核心方法论和工具脚本，可以直接用于小说改编、剧本审核、分镜规划和视频提示词生成。运行产物会写入本地 `outputs/{剧本名}/`，图片/视频脚本需要你在 `.env` 或环境变量中配置对应 API Key、Base URL 和可选模型。

### 爆款剧本检索怎么用

剧本写作阶段可以使用 `hit-script-retrieval-skill` 从你自己的授权剧本库里检索参考样本，用于学习节奏、钩子、爽点和表达方式。仓库不自带剧本语料；你需要把自己有权使用的 `.md` 文件放到下面这个目录：

```bash
mkdir -p knowledge/hit-scripts-md
```

推荐文件组织方式：

```text
knowledge/hit-scripts-md/
├── 女频-重生复仇-001.md
├── 女频-豪门甜宠-001.md
├── 男频-战神归来-001.md
└── 悬疑-灵异反转-001.md
```

每个 `.md` 文件建议包含：

```markdown
# 剧名或案例名

## 标签
女频 / 重生 / 复仇 / 豪门 / 甜宠

## 结构摘要
- 开场钩子：...
- 核心冲突：...
- 反转节点：...

## 正文或片段
...
```

放好语料后可以手动测试检索：

```bash
python3 scripts/quick_search.py "重生 复仇 豪门"
python3 scripts/improved_hybrid_search.py "重生 复仇 豪门" female
```

参数说明：

- `quick_search.py`：轻量关键词检索，不需要向量索引，适合快速验证语料是否放对位置。
- `improved_hybrid_search.py`：混合检索，会使用关键词、语义特征和男女频分类；第二个参数可用 `male`、`female`、`all`。
- 首次混合检索会在本地生成 `.search_index/` 索引；后续会复用本地索引。

在 Agent 工作流中，`~write N` 会优先尝试检索 Top 5 参考剧本；如果没有语料，会跳过参考检索并继续基础写作流程。

## 快速开始

### 1. 环境要求

- Python 3.10+（建议 3.11 或 3.12）
- Git
- 可选：Claude Code、Codex、Cursor 或其他能读取 `AGENTS.md` 的 Agent 环境

安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

配置 API（仅图片/视频相关脚本需要）：

```bash
cp .env.example .env
# 编辑 .env，填入需要的 key、base url 和可选模型
```

| 变量 | 用途 | 是否必需 |
|------|------|----------|
| `NANO_BANANA_API_KEY` | 图片生成、图片反推鉴权 | 仅 `scripts/generate_image.py`、`scripts/reverse_prompt.py` 需要 |
| `NANO_BANANA_BASE_URL` | OpenAI-compatible Base URL，例如 `https://your-provider.example/v1` | 图片生成/反推必需；仓库不默认写死供应商地址 |
| `NANO_BANANA_IMAGE_MODEL` | 图片生成模型 | 可选，默认 `gemini-3.1-flash-image-preview` |
| `NANO_BANANA_REVERSE_MODEL` | 图片反推模型 | 可选，默认 `gemini-3.1-pro-preview` |
| `SKYREELS_API_KEY` | SkyReels 图片转视频鉴权 | 仅 `scripts/ava_skyreels_batch.py` 需要 |
| `SKYREELS_BASE_URL` | SkyReels API Base URL | 可选；默认官方 gateway，可被环境变量覆盖 |
| `SKYREELS_SUBMIT_URL` / `SKYREELS_TASK_URL` | SkyReels 提交/查询端点 | 可选；对接非标准网关时使用 |
| `TMPFILES_UPLOAD_URL` / `CATBOX_UPLOAD_URL` | 视频批处理前的图片上传服务端点 | 可选；可替换为自己的上传服务 |

### 2. 阅读 Agent 指南

```bash
cat AGENTS.md
```

`AGENTS.md` 是通用 Agent 入口；`CLAUDE.md` 只保留为 Claude Code 兼容入口。

### 3. 常用命令流

```bash
# 小说 -> 剧本
~ingest          # 可选：知识收编，本地有 sources/ 或 pending-knowledge/ 时使用
~analyze         # 改编分析
~plan            # 分集规划
~write 1         # 写第 1 集
~review 1        # 复核第 1 集

# 剧本 -> 分镜（二选一）
~storyboard-film 1      # 标准分镜流
~storyboard-seedance 1  # Seedance 提示词流

# 可选：图片生成
~generate-images 1

# 完成检查
~final-check
```

### 4. 本地脚本校验

```bash
python3 -m py_compile scripts/*.py
python3 scripts/quick_search.py "重生 复仇 豪门"
```

## Agent / Skill / Reference 如何协作

```mermaid
flowchart LR
  User["创作者 / Agent 使用者"] --> Command["命令<br/>~analyze / ~plan / ~write N / ~storyboard-*"]
  Command --> Agent["Agent<br/>专业角色与阶段负责人"]
  Agent --> Skill["Skill<br/>执行步骤 / 检查表 / 产物格式"]
  Agent --> Reference["Reference<br/>方法论 / 标准 / 合规边界"]
  Reference --> Skill
  Skill --> Script["Scripts<br/>检索 / 生图 / 反推 / 视频批处理"]
  Agent --> Output["outputs/{剧本名}<br/>阶段产物 / 审核报告 / 状态"]
  Output --> Agent
```

协作关系可以理解为：**Agent 决定谁来负责，Skill 决定怎么执行，Reference 决定判断标准，Scripts 处理可自动化的工具动作，Outputs 保存项目记忆和交付物。**

## 工作流总览

```mermaid
flowchart TD
  A["阶段0 可选<br/>知识收编<br/>~ingest / ~ingest-pending"] --> B["阶段1<br/>改编分析<br/>novel-analyzer + insight-architect"]
  B --> C["阶段2<br/>分集规划<br/>episode-architect + emotion-architect"]
  C --> D["阶段3<br/>单集写作<br/>script-writer + visual-storyteller"]
  D --> E{"审核通过?"}
  E -- "否" --> D
  E -- "是" --> F["连续性记录<br/>continuity-recorder"]
  F --> G["阶段4<br/>总复核 / 对比审核<br/>script-comparator + review-director"]
  G --> H{"进入分镜?"}
  H -- "标准分镜" --> I["阶段5A<br/>Film Storyboard<br/>Beat / Board / Motion"]
  H -- "Seedance" --> J["阶段5B<br/>Seedance Flow<br/>导演分析 / 服化道 / 帧图需求 / 提示词"]
  I --> K["阶段6<br/>完成检查<br/>乱码 / 称呼 / 文件完整性"]
  J --> K
  K --> L["final-check-report.md"]
```

## 两条分镜路线

### 标准分镜流：`~storyboard-film N`

适合传统影视分镜、图生视频、分镜板交付。

1. `storyboard-artist` 生成 Beat Breakdown（节拍拆解）。
2. `storyboard-artist` 生成 Beat Board（九宫格）。
3. `storyboard-artist` 生成 Sequence Board（四宫格）。
4. `animator` 生成 Motion Prompt（动态提示词）。
5. `storyboard-director` 在每一步执行分镜审核。

### Seedance 流：`~storyboard-seedance N`

适合需要直接复制到 Seedance 平台的提示词脚本。

1. `storyboard-director` 生成导演分析：讲戏本、人物清单、场景清单。
2. `art-designer` 生成服化道提示词：人物、场景、道具。
3. `image-generator` 可选生成资产图。
4. `storyboard-artist` 生成 Seedance 2.0 提示词和帧图需求清单。
5. `image-generator` 按需生成首帧/尾帧/参考帧。
6. `storyboard-director` 审核模式选型、帧图完整性、提示词质量。

## Agent 架构

| Agent | 职责 | 主要依赖 |
|-------|------|----------|
| `knowledge-curator` | 本地资料收编、更新知识索引 | `knowledge-curation-skill` |
| `novel-analyzer` | 小说/原文改编分析 | `adaptation-analysis-skill` |
| `insight-architect` | 提炼隐藏真相、核心冲突、观众预期 | `references/18-theme-selection-philosophy.md` |
| `episode-architect` | 分集目录、进度、钩子和节奏规划 | `episode-planning-skill` |
| `emotion-architect` | 情绪曲线、悬念策略、心理预期管理 | `references/14-story-psychology.md` |
| `script-writer` | 单集剧本生成、风格分析、回改 | `script-writing-skill`、`hit-script-retrieval-skill`、`style-analysis-skill` |
| `visual-storyteller` | 检查视觉化程度，推动 Show Don't Tell | `show-dont-tell-skill` |
| `script-comparator` | 与参考剧本逐一对比，找节奏和爽点差距 | `one-by-one-comparison-skill` |
| `review-director` | 业务审核、合规审核、综合复核 | `script-review-skill`、`compliance-review-skill`、`comparative-review-skill` |
| `continuity-recorder` | 人设、称呼、道具、时间线、伏笔记录 | `continuity-record-skill` |
| `storyboard-director` | 分镜导演、导演分析、分镜审核 | `director-skill`、分镜审核类 skills |
| `storyboard-artist` | 标准分镜和 Seedance 提示词生成 | `film-storyboard-skill`、`seedance-storyboard-skill` |
| `storyboard-coach` | 对分镜策略提供教练式指导 | `storyboard-coaching-skill` |
| `art-designer` | 服化道、色彩、光影、资产提示词 | `art-design-skill` |
| `animator` | 动态镜头、运动、转场提示词 | `animator-skill` |
| `image-generator` | 批量生成角色图、场景图、帧图 | `image-generation-skill` |
| `image-to-prompt` | 图片反推视觉描述和文生图提示词 | `image-to-prompt-skill` |

## Skill 分组

### 核心流程

- `knowledge-curation-skill`：知识收编，把本地资料沉淀进稳定结构。
- `adaptation-analysis-skill`：改编分析，拆原文、人物、冲突和可拍性。
- `episode-planning-skill`：分集规划，设计节奏、钩子和集间推进。
- `script-writing-skill`：剧本写作，按集输出可拍文本。

### 剧本质量与审核

- `script-review-skill`：业务审核，检查叙事质量、结构完整性、留存点。
- `compliance-review-skill`：合规审核，检查内容风险、平台边界和版权风险。
- `style-analysis-skill`：语言风格分析，检查句长、对话比、网文感、视觉标记。
- `comparative-review-skill`：快速对比审核，判断生成剧本和参考样本差距。
- `one-by-one-comparison-skill`：逐一对比参考剧本，用于最终复核。
- `continuity-record-skill`：连续性记录，维护角色、称呼、道具、时间线。
- `show-dont-tell-skill`：视觉化检查，把抽象情绪转成可拍动作。

### 分镜与视频化

- `storyboard-handoff-skill`：剧本到分镜的交接规则。
- `director-skill`：导演分析，输出讲戏本、人物清单、场景清单。
- `film-storyboard-skill`：标准分镜，支持 Beat/Sequence/Motion 结构。
- `seedance-storyboard-skill`：Seedance 提示词脚本和帧图需求。
- `animator-skill`：镜头运动、动作节奏、转场和动态提示词。
- `art-design-skill`：人物、场景、道具、色彩、光影资产设计。

### 分镜审核

- `script-analysis-review-skill`：导演分析审核。
- `art-direction-review-skill`：服化道审核。
- `seedance-prompt-review-skill`：Seedance 提示词审核。
- `storyboard-review-skill`：分镜结构审核。
- `storyboard-coaching-skill`：分镜教练。

### 检索与媒体工具

- `hit-script-retrieval-skill`：基于本地授权语料的爆款剧本检索。
- `image-generation-skill`：文生图和帧图生成。
- `image-to-prompt-skill`：图片反推提示词。

## References 方法论

`references/` 是运行时优先阅读的稳定知识层：

- **A 级核心标准**：`00-06`、`18`，覆盖第一性原则、改编系统、分集架构、剧本标准、审核门控、合规边界、题材选择。
- **B 级分镜与视频化**：`08-12`、`19`、`20`，覆盖镜头摄影、分镜方法论、场景设计、视频提示词、类型化技巧、帧图描述元素。
- **C 级知识管理**：`07`，说明如何收编本地资料并沉淀为公开可复用结论。
- **D 级视觉叙事与心理学**：`13-17`，覆盖 Show Don't Tell、故事心理学、色彩心理学、剧作原理、光影叙事。
- **执行规范**：`21-agent-logging-standard.md`，定义日志记录格式和交付物索引方式。

## 关键协作关系

1. **`insight-architect` -> `episode-architect` / `script-writer` / `emotion-architect`**
   - 洞察报告提供主流叙事、隐藏真相、核心冲突和观众预期。
2. **`emotion-architect` -> `script-writer`**
   - 情绪策略提供单集情绪目标、悬念链路和认知负荷建议。
3. **`visual-storyteller` -> `script-writer`**
   - 视觉化审核把抽象心理描写改成动作、道具、场面和镜头。
4. **`script-comparator` -> `review-director`**
   - 逐一对比参考剧本，帮助最终审核判断节奏、爽点、钩子是否达标。
5. **`continuity-recorder` -> 全部 Agents**
   - 项目记忆保证跨集人设、称呼、道具、伏笔和时间线一致。
6. **`storyboard-director` -> `storyboard-artist` / `art-designer` / `animator`**
   - 导演视角统一分镜、服化道、动态提示词和视频平台约束。

## 核心机制

### Resumable Subagents

每个项目可以有独立的 Agent 状态：

- 剧本级配置：`outputs/{剧本名}/.agent-state.json`
- 同一集内：尽量 resume 同一 agent，保持上下文连续。
- 跨集时：重置 agent id，避免上下文窗口溢出和旧信息污染。
- 多项目并行：不同剧本目录互不干扰。

详见：`AGENT-STATE-GUIDE.md`。

### 双重审核

每个关键阶段都执行：

1. 业务审核：叙事质量、结构完整性、钩子、留存、爽点/虐点。
2. 合规审核：内容边界、平台风险、版权风险、低俗/血腥/未成年人等风险。

审核循环：

```text
生成 -> 审核 -> 回改 -> 复审 -> PASS
```

### 完成检查

完整工作流结束时执行：

1. UTF-8 乱码检查。
2. 称呼一致性检查。
3. 文件完整性检查。
4. 输出 `outputs/{剧本名}/final-check-report.md`。

## 目录结构

```text
novel-to-script-team/
├── AGENTS.md                    # 通用 Agent 工作流指南
├── CLAUDE.md                    # Claude Code 兼容入口
├── SKILL.md                     # 项目 Skill 元信息
├── README.md                    # 中文说明
├── README_en.md                 # 英文说明
├── AGENT-STATE-GUIDE.md         # Resumable Subagents 指南
├── agents/                      # Agent 角色定义
├── skills/                      # Skill 执行规则
├── references/                  # 核心方法论
├── knowledge/                   # 知识索引、自有授权语料与吸收记录
├── scripts/                     # 工具脚本
└── outputs/                     # 本地产出目录
```

本地生成目录示例：

```text
outputs/{剧本名}/
├── .agent-state.json
├── analysis/
├── planning/
├── emotion-design/
├── scripts/
├── review/
├── storyboard/
├── assets/
├── images/
└── final-check-report.md
```

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `scripts/quick_search.py` | 无外部依赖的简易关键词检索 |
| `scripts/improved_hybrid_search.py` | 语义 + 关键词 + 男女频分类的混合检索 |
| `scripts/test_retrieval.py` | 检索系统自测 |
| `scripts/generate_image.py` | 批量文生图/帧图生成 |
| `scripts/reverse_prompt.py` | 图片反推提示词 |
| `scripts/ava_skyreels_batch.py` | SkyReels 图片转视频批处理 |
| `scripts/ave_still_batch.py` | 批量静帧生成辅助 |
| `scripts/ave_composite_batch.py` | 批量合成辅助 |
| `scripts/refresh_knowledge_registry.sh` | 刷新知识索引 |

## 许可证

本项目采用 MIT License，详见 [`LICENSE`](LICENSE)。
