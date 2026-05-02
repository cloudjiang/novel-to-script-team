# Canon Map

## 运行时 Canon

### 核心原则与系统（A 级 - 必读）
1. `../references/00-first-principles.md`
2. `../references/01-adaptation-system.md`
3. `../references/02-episode-architecture.md`
4. `../references/03-script-writing-standard.md`
5. `../references/04-review-gates.md`
6. `../references/05-compliance-boundaries.md`
7. `../references/06-storyboard-handoff.md`
8. `../references/07-knowledge-curation.md`

### 分镜与视频化（B 级 - 按需）
8. `../references/08-camera-and-cinematography.md`
9. `../references/09-storyboard-methodology.md`
10a. `../references/10a-action-dialogue-scenes.md`
10b. `../references/10b-atmosphere-fantasy.md`
10c. `../references/10c-suspense-montage.md`
11a. `../references/11a-seedance-prompt-methodology.md`
11b. `../references/11b-image-motion-prompt.md`
11c. `../references/11c-sora2-rhythm-control.md`
12. `../references/12-genre-specific-techniques.md`

## Skill -> Canon 依赖

### 剧本创作流程（原有）
1. knowledge-curation-skill -> 07 + index
2. adaptation-analysis-skill -> 00 + 01
3. episode-planning-skill -> 00 + 02
4. script-writing-skill -> 00 + 03 + 12
5. script-review-skill -> 00 + 04
6. compliance-review-skill -> 00 + 05
7. continuity-record-skill -> 00 + 04
8. novel-to-script-orchestrator-skill -> index + 00

### 分镜桥接（原有 + 增强）
9. storyboard-handoff-skill -> 00 + 06 + 08 + 09 + 10 + 11

### 标准分镜流（新增）
10. director-skill -> 00 + 06 + 08 + 09 + 10
11. film-storyboard-skill -> 00 + 06 + 08 + 09 + 11
12. animator-skill -> 00 + 06 + 11
13. script-analysis-review-skill -> 00 + 04 + 06 + 08 + 09
14. storyboard-review-skill -> 00 + 06 + 08 + 09 + 11

### Seedance 流（新增）
15. art-design-skill -> 00 + 06 + 10 + 11 + 12
16. seedance-storyboard-skill -> 00 + 06 + 11 + 12
17. art-direction-review-skill -> 00 + 05 + 06 + 11
18. seedance-prompt-review-skill -> 00 + 06 + 11 + 12

## Agent -> Skill 绑定

### 剧本创作 Agents（原有）
- novel-analyzer -> adaptation-analysis-skill
- episode-architect -> episode-planning-skill
- script-writer -> script-writing-skill
- review-director -> script-review-skill, compliance-review-skill
- continuity-recorder -> continuity-record-skill
- knowledge-curator -> knowledge-curation-skill

### 分镜与视频化 Agents（新增）
- storyboard-director -> director-skill, script-analysis-review-skill
- storyboard-artist -> film-storyboard-skill, storyboard-review-skill
- art-designer -> art-design-skill, art-direction-review-skill
- animator -> animator-skill, seedance-storyboard-skill, seedance-prompt-review-skill

## 来源映射原则

- 旧资料映射以”能力域”为单位，不再按原目录平移。
- 映射明细见：`./absorption-map-index.md` 与 `./source-registry.md`。
- 整合完成时间：2026-03-07
