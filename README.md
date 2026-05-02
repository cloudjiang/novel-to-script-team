# Novel-to-Script-Team

[中文](#中文) | [English](#english)

---

## 中文

Novel-to-Script-Team 是一套多 Agent、多 Skill 的小说改编影视流水线，用于把长篇小说或故事素材逐步转成短剧/漫剧剧本、审核报告、分镜方案和视频/图片提示词。

### 核心能力

- 小说改编分析：提取题材、主线、人物关系、冲突和可拍性问题。
- 洞察与分集规划：生成情绪曲线、分集目录、节奏设计和钩子策略。
- 剧本写作与复审：按集生成剧本，并经过业务审核、合规审核、风格分析和对比审查。
- 分镜与视频化：支持标准分镜流和 Seedance 提示词流。
- 图像与视频辅助脚本：可选调用图片生成、图片反推、SkyReels 批处理等工具。

### 开源版说明

本仓库开源分发的是 Agent/Skill 工作流、参考方法论和工具脚本。以下内容默认不会进入 Git：

- `outputs/`：本地生成的剧本、分镜、图片、视频和报告。
- `docs/`：内部审计、整合报告和临时设计文档。
- `sources/`、`pending-knowledge/`：历史原始资料池和待收编资料。
- `knowledge/hit-scripts-md/`：第三方或项目内剧本语料，需你自行准备可授权版本。
- `.search_index/`、`.agent-state.json`、`.env`：本地索引、运行状态和密钥。

> 如果你需要使用爆款剧本检索，请自行创建 `knowledge/hit-scripts-md/` 并放入有权使用的 `.md` 剧本语料。

### 运行环境

- Python 3.10+（建议 3.11 或 3.12）
- Git
- 可选：Claude Code、Codex 或其他支持 Agent/Skill 的本地代理环境

安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

配置 API Key（仅图片/视频相关脚本需要）：

```bash
cp .env.example .env
# 编辑 .env，填入需要的 key
```

| 变量 | 用途 | 是否必需 |
|------|------|----------|
| `NANO_BANANA_API_KEY` | `scripts/generate_image.py`、`scripts/reverse_prompt.py` | 仅图片生成/反推需要 |
| `SKYREELS_API_KEY` | `scripts/ava_skyreels_batch.py` | 仅 SkyReels 视频批处理需要 |

### 快速开始

查看 Agent 工作流配置：

```bash
cat AGENTS.md
```

`CLAUDE.md` 仅作为 Claude Code 的兼容入口，实际规则以 `AGENTS.md` 为准。

常用工作流：

```bash
# 小说 -> 剧本
~ingest          # 可选：知识收编
~analyze         # 改编分析
~plan            # 分集规划
~write 1         # 写第 1 集
~review 1        # 审核第 1 集

# 剧本 -> 分镜（二选一）
~storyboard-film 1
~storyboard-seedance 1

# 可选：图片生成
~generate-images 1

# 完成检查
~final-check
```

脚本校验：

```bash
python3 -m py_compile scripts/*.py
python3 scripts/quick_search.py "重生 复仇 豪门"
```

开源版默认没有本地语料时，检索脚本会提示你放入自己的语料，不会直接报错退出。

### 架构

主要目录：

```text
novel-to-script-team/
├── AGENTS.md                    # 通用 Agent 工作流指南
├── CLAUDE.md                    # Claude Code 兼容入口
├── SKILL.md                     # 项目入口说明
├── AGENT-STATE-GUIDE.md         # Resumable Subagents 指南
├── agents/                      # Agent 角色定义
├── skills/                      # Skill 执行规则
├── references/                  # 核心参考方法论
├── knowledge/                   # 知识管理索引与吸收记录
├── scripts/                     # 工具脚本
└── outputs/                     # 本地产出目录，被 .gitignore 忽略
```

核心流程：

1. `knowledge-curator`：可选知识收编。
2. `novel-analyzer` + `insight-architect`：改编分析与洞察提炼。
3. `episode-architect` + `emotion-architect`：分集规划与情绪设计。
4. `script-writer` + `visual-storyteller`：剧本生成与视觉化改写。
5. `review-director` + `script-comparator`：业务、合规、风格和对比审核。
6. `storyboard-director` + `storyboard-artist` + `art-designer` + `animator`：分镜、服化道、视频提示词。

### 质量保障

- 每个关键阶段执行业务审核和合规审核。
- 每集产物写入 `outputs/{剧本名}/`。
- Agent 状态记录在 `outputs/{剧本名}/.agent-state.json`，便于断点续跑。
- 工作流完成后可执行乱码检查、称呼一致性检查和文件完整性检查。

### 许可证

本项目采用 MIT License，详见 [`LICENSE`](LICENSE)。

---

## English

Novel-to-Script-Team is a multi-agent, multi-skill pipeline for adapting novels or story material into short-drama/webtoon scripts, review reports, storyboard plans, and image/video prompts.

### Core Features

- Novel adaptation analysis: extracts genre, plot, character relationships, conflicts, and filmability risks.
- Insight and episode planning: builds emotional arcs, episode outlines, pacing, and hook strategies.
- Script writing and review: generates episode scripts with business review, compliance review, style analysis, and comparison review.
- Storyboard and video handoff: supports both a standard storyboard workflow and a Seedance prompt workflow.
- Optional media scripts: includes utilities for image generation, image-to-prompt analysis, and SkyReels batch processing.

### Open-Source Distribution Notes

This repository ships the Agent/Skill workflow, reference methodology, and utility scripts. The following local or proprietary materials are intentionally excluded from Git:

- `outputs/`: generated scripts, storyboards, images, videos, and reports.
- `docs/`: internal audits, integration reports, and temporary design documents.
- `sources/`, `pending-knowledge/`: raw source corpus and pending ingestion material.
- `knowledge/hit-scripts-md/`: third-party or project-specific script corpus; provide your own licensed `.md` files if needed.
- `.search_index/`, `.agent-state.json`, `.env`: local indexes, runtime state, and secrets.

> To use hit-script retrieval, create `knowledge/hit-scripts-md/` locally and add `.md` script files that you are licensed to use.

### Requirements

- Python 3.10+ (3.11 or 3.12 recommended)
- Git
- Optional: Claude Code, Codex, or another local agent environment that supports Agent/Skill workflows

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure API keys (only needed for image/video scripts):

```bash
cp .env.example .env
# Edit .env and fill in the keys you need.
```

| Variable | Used by | Required |
|----------|---------|----------|
| `NANO_BANANA_API_KEY` | `scripts/generate_image.py`, `scripts/reverse_prompt.py` | Only for image generation / reverse prompting |
| `SKYREELS_API_KEY` | `scripts/ava_skyreels_batch.py` | Only for SkyReels batch video jobs |

### Quick Start

Inspect the agent workflow configuration:

```bash
cat AGENTS.md
```

`CLAUDE.md` is kept only as a Claude Code compatibility adapter; `AGENTS.md` is the canonical guide.

Typical workflow:

```bash
# Novel -> script
~ingest          # Optional: ingest local knowledge
~analyze         # Adaptation analysis
~plan            # Episode planning
~write 1         # Write episode 1
~review 1        # Review episode 1

# Script -> storyboard (choose one)
~storyboard-film 1
~storyboard-seedance 1

# Optional: image generation
~generate-images 1

# Final workflow check
~final-check
```

Validate scripts:

```bash
python3 -m py_compile scripts/*.py
python3 scripts/quick_search.py "rebirth revenge wealthy-family"
```

If the local script corpus is missing, retrieval scripts will print a friendly setup message instead of crashing.

### Architecture

Main directories:

```text
novel-to-script-team/
├── AGENTS.md                    # General agent workflow guide
├── CLAUDE.md                    # Claude Code compatibility adapter
├── SKILL.md                     # Project entry point
├── AGENT-STATE-GUIDE.md         # Resumable Subagents guide
├── agents/                      # Agent role definitions
├── skills/                      # Skill execution rules
├── references/                  # Core reference methodology
├── knowledge/                   # Knowledge indexes and ingestion records
├── scripts/                     # Utility scripts
└── outputs/                     # Local generated outputs, ignored by .gitignore
```

Core flow:

1. `knowledge-curator`: optional local knowledge ingestion.
2. `novel-analyzer` + `insight-architect`: adaptation analysis and insight extraction.
3. `episode-architect` + `emotion-architect`: episode planning and emotional design.
4. `script-writer` + `visual-storyteller`: script generation and visual rewrite.
5. `review-director` + `script-comparator`: business, compliance, style, and comparison review.
6. `storyboard-director` + `storyboard-artist` + `art-designer` + `animator`: storyboard, art direction, and video prompts.

### Quality Controls

- Business review and compliance review are required at key stages.
- Episode outputs are written under `outputs/{script_name}/`.
- Agent state is stored in `outputs/{script_name}/.agent-state.json` for resumable execution.
- Final checks can validate encoding, naming consistency, and file completeness.

### License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
