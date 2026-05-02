# 知识源注册表

- 生成时间：2026-03-07 15:30:00
- 生成脚本：`./scripts/refresh_knowledge_registry.sh`
- 状态：sources/ 已归档，本注册表记录整合后的运行时结构

## 整合后运行时结构

### References（参考文档）- 12 个
- **核心原则与系统（A 级）**：00-07
  - 00-first-principles.md
  - 01-adaptation-system.md（增强：性别频率、情绪曲线、Buff 系统）
  - 02-episode-architecture.md（增强：系统化分集框架）
  - 03-script-writing-standard.md（增强：类型模板、格式标记）
  - 04-review-gates.md（增强：Aligner 方法论）
  - 05-compliance-boundaries.md（增强：视觉合规、借鉴边界）
  - 06-storyboard-handoff.md（增强：详细工作流）
  - 07-knowledge-curation.md

- **分镜与视频化（B 级）**：08-12（新增，整合自 sources/）
  - 08-camera-and-cinematography.md（镜头技巧、景别、角度、运镜）
  - 09-storyboard-methodology.md（Beat breakdown、九宫格、四宫格）
  - 10a-action-dialogue-scenes.md（动作、对话场景）
  - 10b-atmosphere-fantasy.md（氛围、奇幻视觉）
  - 10c-suspense-montage.md（悬疑、蒙太奇）
  - 11a-seedance-prompt-methodology.md（Seedance 2.0 提示词）
  - 11b-image-motion-prompt.md（Gemini、Motion Prompt）
  - 11c-sora2-rhythm-control.md（Sora2、节奏控制）
  - 12-genre-specific-techniques.md（玄幻、末世、网文、短剧）

### Agents（Agent 配置）- 10 个
- **原有 6 个**：
  - continuity-recorder.md
  - episode-architect.md
  - knowledge-curator.md
  - novel-analyzer.md
  - review-director.md
  - script-writer.md

- **新增 4 个**（整合自 sources/）：
  - storyboard-director.md（分镜导演）
  - storyboard-artist.md（分镜师）
  - art-designer.md（服化道）
  - animator.md（动画师）

### Skills（技能包）- 18 个
- **原有 9 个**：
  - adaptation-analysis-skill
  - compliance-review-skill
  - continuity-record-skill
  - episode-planning-skill
  - knowledge-curation-skill
  - novel-to-script-orchestrator-skill
  - script-review-skill
  - script-writing-skill
  - storyboard-handoff-skill

- **新增 9 个**（整合自 sources/）：
  - director-skill（导演分析）
  - film-storyboard-skill（影视分镜）
  - seedance-storyboard-skill（Seedance 分镜）
  - art-design-skill（服化道设计）
  - animator-skill（动画师）
  - script-analysis-review-skill（导演分析审核）
  - art-direction-review-skill（服化道审核）
  - seedance-prompt-review-skill（Seedance 提示词审核）
  - storyboard-review-skill（分镜审核）

## 去重内容记录

以下内容在 sources/ 中重复出现，已合并为单一信息源：

1. **Gemini 提示词指南**（重复率 100%）→ references/11b-image-motion-prompt.md
2. **分镜方法论**（重复率 95%）→ references/09-storyboard-methodology.md
3. **动态提示词方法论**（重复率 100%）→ references/11b-image-motion-prompt.md
4. **合规审核规则**（重复率 80%）→ references/05-compliance-boundaries.md
5. **Aligner 方法论**（重复率 70%）→ references/04-review-gates.md

## 历史来源映射（已归档）

以下为 sources/ 目录中原始文件的分类记录，仅供历史参考：

| 来源文件 | 建议归属Skill | 优先级 |
|---|---|---|
| `sources/legacy-novel-to-script-v2/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/references/integration-rules.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/references/source-registry.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/subskills/episode-architect/SKILL.md` | `episode-planning-skill` | `A` |
| `sources/legacy-novel-to-script-v2/subskills/knowledge-curator/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/subskills/novel-analyzer/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/subskills/quality-gate/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/subskills/script-writer/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script-v2/subskills/storyboard-bridge/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/audio-friendliness.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/character-reference-prompt.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/compliance.md` | `script-review-skill` | `A` |
| `sources/legacy-novel-to-script/references/01-格式与规范/consistency-check.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/export-guide.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/script-format-basic.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/script-format-donghua.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/01-格式与规范/self-check.md` | `script-review-skill` | `A` |
| `sources/legacy-novel-to-script/references/01-格式与规范/storyboard-script-format.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/02-创作方法论/adaptation-strategy.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/analysis-method.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/emotion-curve.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/gender-frequency.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/handbook-bridge.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/parsing-playbook.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/pitfalls-guide.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/three-layer-buff.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/xiaohongshu-complete.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/02-创作方法论/xiaohongshu-techniques.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/03-案例与模板/approved-script-example-1.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/03-案例与模板/approved-script-example-2.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/03-案例与模板/case-benchmark.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references/03-案例与模板/character-ensemble-templates.md` | `script-writing-skill` | `B` |
| `sources/legacy-novel-to-script/references/03-案例与模板/episode-planning.md` | `episode-planning-skill` | `A` |
| `sources/legacy-novel-to-script/references/03-案例与模板/male-frequency-plot-templates.md` | `script-writing-skill` | `B` |
| `sources/legacy-novel-to-script/references/03-案例与模板/plot-reversal-templates.md` | `script-writing-skill` | `B` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/action-scene-design.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/ai-video-generation-tips.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/atmosphere-design.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/camera-basics.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/camera-movement.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/dialogue-scene-design.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/montage-transition-design.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/shot-definitions-complete.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/storyboard-rules-advanced.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/storyboard-rules.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/04-镜头与分镜/suspense-thriller-design.md` | `storyboard-handoff-skill` | `A` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/character-development-system.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/dialogue-creation-system.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/episode-design-system.md` | `episode-planning-skill` | `A` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/gender-tuning-system.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/novel-adaptation-methodology.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/plot-inspiration-library.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/plot-structure-system.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/satisfaction-engine.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/theme-positioning.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/05-系统级方法论/worldbuilding-system.md` | `adaptation-analysis-skill` | `B` |
| `sources/legacy-novel-to-script/references/README.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/references触发升级方案.md` | `knowledge-curation-skill` | `C` |
| `sources/legacy-novel-to-script/升级指南.md` | `knowledge-curation-skill` | `C` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/animator-skill/SKILL.md.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/animator-skill/motion-prompt-methodology.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/animator-skill/templates/motion-prompt-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/animator.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/director.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/film-storyboard-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/film-storyboard-skill/gemini-image-prompt-guide.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/film-storyboard-skill/storyboard-methodology-playbook.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/film-storyboard-skill/templates/beat-board-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/film-storyboard-skill/templates/beat-breakdown-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/film-storyboard-skill/templates/sequence-board-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/storyboard-artist.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/storyboard-review-skill/motion-prompt-methodology.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/storyboard-review-skill/review-checklist.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/storyboard-review-skill/storyboard-methodology-playbook.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/AI 分镜师 配置文件/AI 分镜师 配置文件/storyboard-review-skill/storyboard-review-skill-SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/agents/art-designer.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/agents/director.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/agents/storyboard-artist.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/art-design-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/art-design-skill/examples/character-prompt-examples.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/art-design-skill/examples/scene-prompt-examples.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/art-design-skill/gemini-image-prompt-guide.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/art-design-skill/templates/art-design-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/art-direction-review-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/compliance-review-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/director-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/director-skill/templates/director-analysis-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/script-analysis-review-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/seedance-prompt-review-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/seedance-storyboard-skill/SKILL.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/seedance-storyboard-skill/examples/seedance-prompt-examples.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/seedance-storyboard-skill/seedance-prompt-methodology.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/skills/seedance-storyboard-skill/templates/seedance-prompts-template.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-reference-skills/Seedance 2.0 AI 分镜师团队/（飞薯）.txt` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/7efc9a1353d36da972654b22520e39c2.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/SKILL.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/examples/catalog-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/examples/chapter-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/examples/character-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/examples/outline-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/outline-method.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/output-style.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/templates/chapter-index-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/templates/chapter-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/templates/character-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/doomsday-skill/templates/outline-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/末世重生类 Aligner Subagent System Prompt/描述.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/末世重生类漫剧剧本创作 SKill/末世重生类 Aligner Subagent System Prompt/提示词.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/SKILL.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/examples/catalog-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/examples/chapter-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/examples/character-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/examples/outline-example.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/outline-method.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/output-style.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/templates/chapter-index-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/templates/chapter-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/templates/character-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/xuanhuan-skill/templates/outline-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/玄幻题材类 Aligner Subagent System Prompt/描述.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/玄幻类漫剧剧本创作 Claude Skill/玄幻题材类 Aligner Subagent System Prompt/提示词.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/breakdown-aligner.md` | `script-review-skill` | `A` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-aligner.md` | `script-review-skill` | `A` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/SKILL.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/adapt-method.md` | `adaptation-analysis-skill` | `B` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/examples/plot-breakdown-example.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/examples/script-example.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/output-style.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/templates/plot-breakdown-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI漫剧/网文改编漫剧 Claude Agent +Skill/网文改编资料包/webtoon-skill/templates/script-template.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI短剧/Claude Code 搭建短剧编剧团队/CLAUDE.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/AI短剧/Claude Code 搭建短剧编剧团队/Output Style.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/AI短剧/Claude Code 搭建短剧编剧团队/script-aligner.md` | `script-review-skill` | `A` |
| `sources/new-tutorials/AI短剧/Claude Code 搭建短剧编剧团队/script-recorder.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/AI短剧/Nano Banana 分镜图生成Prompt Framework.md` | `storyboard-handoff-skill` | `A` |
| `sources/new-tutorials/AI短剧/剧本 _ 爽文短剧提示词框架.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI短剧/剧本 _ 网文改编短剧提示词框架.md` | `script-writing-skill` | `B` |
| `sources/new-tutorials/AI短剧/影视 _ 影视编剧助理提示词框架.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/ai剧制作流程.md` | `knowledge-curation-skill` | `C` |
| `sources/new-tutorials/d458217dee57f91c288019e2f2ace0aa.md` | `knowledge-curation-skill` | `C` |
