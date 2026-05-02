#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_FILE="${PROJECT_DIR}/knowledge/source-registry.md"
SOURCES_DIR="${PROJECT_DIR}/sources"
mkdir -p "${PROJECT_DIR}/knowledge"

classify_skill() {
  local rel="$1"

  # 新增：分镜与视频化相关
  if [[ "$rel" == *"director-skill"* ]] || [[ "$rel" == *"导演"* ]] || [[ "$rel" == *"讲戏"* ]]; then
    echo "director-skill|A"; return
  fi
  if [[ "$rel" == *"film-storyboard"* ]] || [[ "$rel" == *"beat-board"* ]] || [[ "$rel" == *"sequence-board"* ]]; then
    echo "film-storyboard-skill|A"; return
  fi
  if [[ "$rel" == *"seedance-storyboard"* ]] || [[ "$rel" == *"Seedance"* ]] && [[ "$rel" == *"prompt"* ]]; then
    echo "seedance-storyboard-skill|A"; return
  fi
  if [[ "$rel" == *"art-design"* ]] || [[ "$rel" == *"服化道"* ]] || [[ "$rel" == *"character-prompt"* ]] || [[ "$rel" == *"scene-prompt"* ]]; then
    echo "art-design-skill|A"; return
  fi
  if [[ "$rel" == *"animator"* ]] || [[ "$rel" == *"motion-prompt"* ]] || [[ "$rel" == *"动态提示词"* ]]; then
    echo "animator-skill|A"; return
  fi

  # 新增：审核技能
  if [[ "$rel" == *"script-analysis-review"* ]] || [[ "$rel" == *"导演分析审核"* ]]; then
    echo "script-analysis-review-skill|A"; return
  fi
  if [[ "$rel" == *"art-direction-review"* ]] || [[ "$rel" == *"服化道审核"* ]]; then
    echo "art-direction-review-skill|A"; return
  fi
  if [[ "$rel" == *"seedance-prompt-review"* ]] || [[ "$rel" == *"Seedance提示词审核"* ]]; then
    echo "seedance-prompt-review-skill|A"; return
  fi
  if [[ "$rel" == *"storyboard-review"* ]] || [[ "$rel" == *"分镜审核"* ]]; then
    echo "storyboard-review-skill|A"; return
  fi

  # 原有：分镜桥接
  if [[ "$rel" == *"storyboard-handoff"* ]] || [[ "$rel" == *"分镜桥接"* ]] || [[ "$rel" == *"CLAUDE.md"* ]]; then
    echo "storyboard-handoff-skill|A"; return
  fi

  # 原有：合规与审核
  if [[ "$rel" == *"compliance"* ]] || [[ "$rel" == *"self-check"* ]] || [[ "$rel" == *"aligner"* ]] || [[ "$rel" == *"review"* ]]; then
    echo "script-review-skill|A"; return
  fi

  # 原有：分集规划
  if [[ "$rel" == *"episode"* ]] || [[ "$rel" == *"情绪"* ]] || [[ "$rel" == *"节奏"* ]]; then
    echo "episode-planning-skill|A"; return
  fi

  # 原有：改编分析
  if [[ "$rel" == *"analysis"* ]] || [[ "$rel" == *"adapt"* ]] || [[ "$rel" == *"方法论"* ]] || [[ "$rel" == *"gender"* ]]; then
    echo "adaptation-analysis-skill|B"; return
  fi

  # 原有：剧本写作
  if [[ "$rel" == *"剧本"* ]] || [[ "$rel" == *"template"* ]] || [[ "$rel" == *"output-style"* ]]; then
    echo "script-writing-skill|B"; return
  fi

  # 默认：知识收编
  echo "knowledge-curation-skill|C"
}

{
  echo "# 知识源注册表"
  echo
  echo "- 生成时间：$(date '+%Y-%m-%d %H:%M:%S')"
  echo "- 生成脚本：\`./scripts/refresh_knowledge_registry.sh\`"
  echo "- 状态：sources/ 已归档（2026-03-07），内容已整合到主结构"
  echo
  echo "## 整合后运行时结构"
  echo
  echo "- **References**: 12 个（00-12，含新增 08-12）"
  echo "- **Agents**: 10 个（含新增 storyboard-director, storyboard-artist, art-designer, animator）"
  echo "- **Skills**: 18 个（含新增 9 个分镜与审核技能）"
  echo
  echo "## 历史来源映射（仅供参考）"
  echo
  echo "| 来源文件 | 建议归属Skill | 优先级 |"
  echo "|---|---|---|"

  while IFS= read -r -d '' f; do
    rel="${f#"${PROJECT_DIR}/"}"
    m="$(classify_skill "$rel")"
    echo "| \`${rel}\` | \`${m%%|*}\` | \`${m##*|}\` |"
  done < <(find "${SOURCES_DIR}" -type f \( -name "*.md" -o -name "*.txt" \) -print0 | sort -z)
} > "${OUT_FILE}"

echo "OK: ${OUT_FILE}"
