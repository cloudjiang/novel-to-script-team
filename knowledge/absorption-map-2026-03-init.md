# Absorption Map — 初始整合记录

> 归档自原 `source-absorption-map.md`，记录 2026-03-07 初始整合结果。
> 归档时间：2026-03-12

---

## 第一性重组结果

### 1. 抽象层（原则）
   - 落地到：`../references/00-first-principles.md`
   - 吸收来源：旧 workflow、v2 门控、短剧法则、Seedance 审核循环

### 2. 结构化层（分析/规划/写作）
   - 落地到：
     - `../references/01-adaptation-system.md`（增强：性别频率、情绪曲线、Buff 系统）
     - `../references/02-episode-architecture.md`（增强：系统化分集框架）
     - `../references/03-script-writing-standard.md`（增强：类型模板、格式标记）
   - 吸收来源：legacy references + new-tutorials 的编剧团队方法

### 3. 门控层（业务+合规）
   - 落地到：
     - `../references/04-review-gates.md`（增强：Aligner 方法论）
     - `../references/05-compliance-boundaries.md`（增强：视觉合规、借鉴边界）
   - 吸收来源：script-aligner、quality-gate、compliance 规则、多个 Aligner 提示词

### 4. 桥接层（分镜/Seedance）
   - 落地到：`../references/06-storyboard-handoff.md`（增强：详细工作流）
   - 吸收来源：Seedance 团队 + AI 分镜师配置

### 5. 分镜与视频化层（新增）
   - 落地到：
     - `../references/08-camera-and-cinematography.md`（镜头技巧、景别、角度、运镜）
     - `../references/09-storyboard-methodology.md`（Beat breakdown、九宫格、四宫格）
     - `../references/10-scene-design-techniques.md`（动作、对话、氛围、悬念、蒙太奇）
     - `../references/11-video-prompt-engineering.md`（Gemini、Seedance、Motion Prompt）
     - `../references/12-genre-specific-techniques.md`（玄幻、末世、网文、短剧）
   - 吸收来源：
     - legacy-novel-to-script/04-镜头与分镜/（11 个文件）
     - AI 分镜师配置文件（方法论、模板）
     - Seedance 2.0 团队（提示词工程）
     - 玄幻/末世/网文短剧教程（类型化技巧）

### 6. 增量治理层（知识收编）
   - 落地到：`../references/07-knowledge-curation.md`
   - 吸收来源：v2 knowledge-curator 与所有外部知识池

### 7. 题材选择哲学层（新增）**2026-03-11**
   - 落地到：`../references/18-theme-selection-philosophy.md`
   - 吸收来源：用户直接提供的核心创作理念
   - 核心内容：
     - 开天眼方法论：剥离分别 → 如实观照 → 颠倒真相
     - 众生好恶原则：从情绪出发，而不是从真理出发
     - 题材价值判断标准：人性本质、被掩盖的真相、普世性、当下性
     - 实操指南：识别"被颠倒的真相"、从"好恶"出发设计冲突、确保普世性和当下性
   - 优先级：S级（核心哲学，所有Agent必须理解和应用）
   - 影响范围：
     - novel-analyzer：识别主流叙事和被掩盖的真相
     - episode-architect：使用"开天眼"方法论设计分集架构
     - script-writer：从"好恶"出发设计冲突
     - review-director：评估题材深度和价值

### 8. 故事心理学层（增强）**2026-03-12**
   - 落地到：`../references/14-story-psychology.md`
   - 吸收来源：
     - `pending-knowledge/split/A-编剧基础-钩子人设套路.md` 章节1（情绪卡点钩子）
     - `pending-knowledge/split/E-剧本方法论-过稿选题公式.md` 章节6（爽感心理学层级）
     - `pending-knowledge/split/E-剧本方法论-过稿选题公式.md` 章节7（共鸣公式）
   - 核心内容：
     - 爽感心理学层级（层级1-3、爽点叠加原则）
     - 共鸣公式（爽点≠共鸣、目标观众定位、性别差异）
     - 情绪卡点钩子方法（三种钩子、设计方法）
   - 优先级：A级（核心执行标准）

## Agent 层整合

### 新增 Agents（4 个）
1. **storyboard-director.md** — 导演分析、镜头设计（director-skill）
2. **storyboard-artist.md** — 分镜绘制、Beat Board（film-storyboard-skill）
3. **art-designer.md** — 服化道设计、Gemini 提示词（art-design-skill）
4. **animator.md** — Motion Prompt 生成（animator-skill）

## Skill 层整合

### 新增 Skills（9 个）
- 分镜工作流：director-skill、film-storyboard-skill、seedance-storyboard-skill
- 服化道与动画：art-design-skill、animator-skill
- 审核：script-analysis-review-skill、art-direction-review-skill、seedance-prompt-review-skill、storyboard-review-skill

## 去冗余策略

1. 同主题保留一份执行标准，其他内容降级为补充来源
2. 运行时仅读 `references/`，避免多版本冲突
3. `sources/` 仅用于后续新增资料吸收，不直接参与生产
4. 重复内容合并：Gemini 提示词→ref/11、分镜方法论→ref/09、合规审核→ref/05、Aligner→ref/04

## 验收结论

1. 运行时知识已内化到 `references/`（12 个）、`agents/`（10 个）、`skills/`（18 个）
2. `agents/` 已按统一协议绑定 skill
3. `sources/` 已完成"知识池"角色，标记为归档
4. 新增分镜与视频化能力：2 条工作流（标准分镜流、Seedance 流）
