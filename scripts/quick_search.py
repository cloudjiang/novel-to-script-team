#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速关键词搜索工具"""

from pathlib import Path
import sys

def quick_search(query: str, n_results: int = 5, min_score: int = 2):
    """
    快速关键词搜索

    Args:
        query: 搜索查询（空格分隔关键词）
        n_results: 返回结果数量
        min_score: 最低匹配度
    """
    md_dir = Path('knowledge/hit-scripts-md')
    if not md_dir.exists():
        print(f'未找到本地剧本语料目录: {md_dir}')
        print('开源版默认不包含该目录；请放入你有权使用的 .md 剧本语料后重试。')
        return []

    query_words = query.split()
    results = []

    print(f"搜索关键词: {query_words}")
    print("=" * 80)

    for md_file in md_dir.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        content_lower = content.lower()

        score = sum(1 for word in query_words if word in content_lower)

        if score >= min_score:
            results.append({
                'filename': md_file.name,
                'filepath': str(md_file),
                'score': score,
                'preview': content[:500],
                'content': content  # 完整内容，供后续使用
            })

    results.sort(key=lambda x: x['score'], reverse=True)

    print(f"\n找到 {len(results)} 个相关剧本（匹配度 >= {min_score}）:\n")

    for i, result in enumerate(results[:n_results], 1):
        print(f"{i}. {result['filename']}")
        print(f"   匹配度: {result['score']}/{len(query_words)}")
        print(f"   路径: {result['filepath']}")
        print(f"   预览: {result['preview'][:100]}...")
        print("-" * 80)

    # 输出文件列表（供agent使用）
    print("\n" + "=" * 80)
    print("检索到的文件列表:")
    for i, result in enumerate(results[:n_results], 1):
        print(f"{i}. {result['filename']}")

    return results[:n_results]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 quick_search.py '关键词1 关键词2 关键词3'")
        print("示例: python3 quick_search.py '重生 复仇 豪门'")
        sys.exit(1)

    query = sys.argv[1]
    quick_search(query)
