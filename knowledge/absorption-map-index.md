# Absorption Map Index

轻量索引文件，替代原 `source-absorption-map.md`（已拆分归档）。

## 总体统计

- 总批次：5（初始整合 + 2026-03-10 + 2026-03-11 + 2026-03-12 + 2026-03-14）
- 总文件数：~346（初始 152 + 03-10 补充 + 03-11 批量 38 + 03-12 批量 155 + 03-14 补充 1）
- References 产出：19 个（新增 8 个，增强 6 个）
- Agents 产出：15 个（新增 5 个）
- Skills 产出：27 个（新增 9 个）

## 月度归档索引

| 月份 | 归档文件 | 批次数 | 处理数 | 接受 | 拒绝 |
|------|---------|--------|--------|------|------|
| 2026-03（初始） | `absorption-map-2026-03-init.md` | 1 | 152 | 152 | 0 |
| 2026-03（日常） | `absorption-map-2026-03.md` | 4 | ~199 | ~114 | ~85 |

## References 健康状态

> 收编时由 knowledge-curator 更新此表

| 文件 | 主题边界 | 状态 |
|------|---------|------|
| 00-first-principles.md | 第一性原则、目标函数 | — |
| 01-adaptation-system.md | 改编分析、性别频率、Buff系统 | — |
| 02-episode-architecture.md | 分集框架、情绪曲线 | — |
| 03-script-writing-standard.md | 写作标准、台词技巧、格式 | — |
| 04-review-gates.md | 业务审核、Aligner、评分表 | — |
| 05-compliance-boundaries.md | 合规红线、风险分级 | — |
| 06-storyboard-handoff.md | 分镜桥接、工作流 | — |
| 07-knowledge-curation.md | 知识收编规范 | — |
| 08-camera-and-cinematography.md | 镜头、景别、运镜 | — |
| 09-storyboard-methodology.md | 分镜方法论、Beat系统 | — |
| 10a-action-dialogue-scenes.md | 动作场景、对话场景 | OK |
| 10b-atmosphere-fantasy.md | 氛围营造、奇幻视觉 | OK |
| 10c-suspense-montage.md | 悬疑惊悚、蒙太奇 | OK |
| 11a-seedance-prompt-methodology.md | Seedance 2.0 提示词 | WARNING |
| 11b-image-motion-prompt.md | Gemini图像、动态提示词 | OK |
| 11c-sora2-rhythm-control.md | Sora2、节奏控制 | OK |
| 12-genre-specific-techniques.md | 类型化技巧 | — |
| 13-show-dont-tell-methodology.md | Show Don't Tell、画面语言 | — |
| 14-story-psychology.md | 故事心理学、情绪共鸣 | — |
| 15-color-psychology.md | 色彩心理学 | — |
| 16-dramatic-principles.md | 剧作原理、冲突设计 | — |
| 17-lighting-narrative.md | 光影叙事 | — |
| 18-theme-selection-philosophy.md | 题材选择、开天眼 | — |
| 19-micro-drama-storyboard-system.md | 微短剧分镜系统 | — |

## 内容归属地图

详见 `../references/index.md`「内容归属地图」章节和 `../references/07-knowledge-curation.md`「内容归属边界」章节。

## 使用说明

- 本文件仅作索引，详细记录请查阅对应月度归档文件
- 每次收编后：更新统计数字 + 追加一行到月度归档索引 + 更新健康状态表
- 健康状态由 `wc -l` 检测：OK < 800 行 / WARNING 800-1199 行 / OVERSIZED >= 1200 行
