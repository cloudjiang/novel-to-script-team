#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的混合搜索系统：
1. 支持索引持久化（避免重复构建）
2. 支持男女频分类过滤
"""

import chromadb
from chromadb.config import Settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
from pathlib import Path
import numpy as np
import pickle
import re
from typing import List, Dict, Tuple, Optional
import sys


class ImprovedHybridSearchEngine:
    """改进的混合搜索引擎：持久化索引 + 男女频分类"""

    def __init__(self, md_dir: str, index_dir: str = ".search_index"):
        """
        初始化搜索引擎

        Args:
            md_dir: MD文件目录路径
            index_dir: 索引存储目录
        """
        self.md_dir = Path(md_dir)
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(exist_ok=True)

        self.documents = []
        self.filenames = []
        self.file_paths = []
        self.genders = []  # 男频/女频标记

        # 检查是否需要重建索引
        if self._should_rebuild_index():
            print("检测到文件变化，重建索引...")
            self._load_documents()
            self._classify_gender()
            self._init_chroma()
            self._init_tfidf()
            self._save_metadata()
        else:
            print("加载已有索引...")
            self._load_metadata()
            self._load_chroma()
            self._load_tfidf()

    def _should_rebuild_index(self) -> bool:
        """检查是否需要重建索引"""
        metadata_file = self.index_dir / "metadata.pkl"
        if not metadata_file.exists():
            return True

        # 检查文件数量是否变化
        try:
            with open(metadata_file, 'rb') as f:
                metadata = pickle.load(f)
            current_files = set(f.name for f in self.md_dir.glob("*.md"))
            saved_files = set(metadata['filenames'])
            return current_files != saved_files
        except:
            return True

    def _load_documents(self):
        """加载所有MD文件"""
        print("正在加载MD文件...")
        for md_file in sorted(self.md_dir.glob("*.md")):
            try:
                content = md_file.read_text(encoding='utf-8')
                self.documents.append(content)
                self.filenames.append(md_file.name)
                self.file_paths.append(str(md_file))
            except Exception as e:
                print(f"警告：无法读取 {md_file.name}: {e}")

        print(f"成功加载 {len(self.documents)} 个文件")

    def _classify_gender(self):
        """分类男女频"""
        print("正在分类男女频...")

        male_keywords = ['男主', '男频', '重生', '异能', '权谋', '锦衣卫', '战神', '兵王', '赘婿']
        female_keywords = ['女主', '女频', '霸总', '豪门', '虐恋', '甜宠', '替身', '闪婚', '追妻']

        for i, (content, filename) in enumerate(zip(self.documents, self.filenames)):
            content_lower = content.lower()
            filename_lower = filename.lower()

            # 统计关键词出现次数
            male_score = sum(1 for kw in male_keywords if kw in content_lower or kw in filename_lower)
            female_score = sum(1 for kw in female_keywords if kw in content_lower or kw in filename_lower)

            # 判定
            if male_score > female_score:
                gender = 'male'
            elif female_score > male_score:
                gender = 'female'
            else:
                # 默认判定：检查文件名中的明确标记
                if '男主' in filename or '男频' in filename:
                    gender = 'male'
                elif '女主' in filename or '女频' in filename:
                    gender = 'female'
                else:
                    gender = 'unknown'

            self.genders.append(gender)

        # 统计
        male_count = self.genders.count('male')
        female_count = self.genders.count('female')
        unknown_count = self.genders.count('unknown')
        print(f"分类完成: 男频 {male_count}, 女频 {female_count}, 未知 {unknown_count}")

    def _init_chroma(self):
        """初始化Chroma语义搜索（持久化）"""
        print("正在初始化Chroma语义搜索...")

        # 使用持久化存储
        chroma_path = str(self.index_dir / "chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)

        # 删除旧collection（如果存在）
        try:
            self.chroma_client.delete_collection("scripts")
        except:
            pass

        # 创建新collection
        self.chroma_collection = self.chroma_client.create_collection("scripts")

        # 添加文档
        for i, (content, filename, gender) in enumerate(zip(self.documents, self.filenames, self.genders)):
            self.chroma_collection.add(
                documents=[content[:5000]],  # 限制长度避免超限
                ids=[f"doc_{i}"],
                metadatas=[{"filename": filename, "index": i, "gender": gender}]
            )

        print("Chroma索引构建完成并保存")

    def _load_chroma(self):
        """加载已有的Chroma索引"""
        chroma_path = str(self.index_dir / "chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.chroma_collection = self.chroma_client.get_collection("scripts")
        print("Chroma索引加载完成")

    def _init_tfidf(self):
        """初始化TF-IDF关键词搜索"""
        print("正在初始化TF-IDF关键词搜索...")

        # 中文分词
        documents_seg = []
        for content in self.documents:
            content_seg = ' '.join(jieba.cut(content))
            documents_seg.append(content_seg)

        # 构建TF-IDF向量
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents_seg)

        # 保存TF-IDF模型
        tfidf_path = self.index_dir / "tfidf_model.pkl"
        with open(tfidf_path, 'wb') as f:
            pickle.dump({
                'vectorizer': self.tfidf_vectorizer,
                'matrix': self.tfidf_matrix
            }, f)

        print("TF-IDF索引构建完成并保存")

    def _load_tfidf(self):
        """加载已有的TF-IDF索引"""
        tfidf_path = self.index_dir / "tfidf_model.pkl"
        with open(tfidf_path, 'rb') as f:
            data = pickle.load(f)
            self.tfidf_vectorizer = data['vectorizer']
            self.tfidf_matrix = data['matrix']
        print("TF-IDF索引加载完成")

    def _save_metadata(self):
        """保存元数据"""
        metadata = {
            'filenames': self.filenames,
            'file_paths': self.file_paths,
            'genders': self.genders,
            'documents': self.documents
        }
        metadata_path = self.index_dir / "metadata.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        print("元数据保存完成")

    def _load_metadata(self):
        """加载元数据"""
        metadata_path = self.index_dir / "metadata.pkl"
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
            self.filenames = metadata['filenames']
            self.file_paths = metadata['file_paths']
            self.genders = metadata['genders']
            self.documents = metadata['documents']
        print("元数据加载完成")

    def semantic_search(self, query: str, n_results: int = 10, gender_filter: Optional[str] = None) -> List[Tuple[int, float]]:
        """
        语义搜索

        Args:
            query: 查询文本
            n_results: 返回结果数量
            gender_filter: 男女频过滤 ('male', 'female', None)

        Returns:
            [(文档索引, 相似度分数), ...]
        """
        # Chroma查询
        where_filter = {"gender": gender_filter} if gender_filter else None
        results = self.chroma_collection.query(
            query_texts=[query],
            n_results=min(n_results * 3, len(self.documents)),  # 多取一些，过滤后可能不够
            where=where_filter
        )

        # 提取结果
        search_results = []
        if results['ids'] and results['ids'][0]:
            for doc_id, distance in zip(results['ids'][0], results['distances'][0]):
                index = int(doc_id.split('_')[1])
                similarity = 1 - distance  # 转换为相似度
                search_results.append((index, similarity))

        return search_results[:n_results]

    def keyword_search(self, query: str, n_results: int = 10, gender_filter: Optional[str] = None) -> List[Tuple[int, float]]:
        """
        关键词搜索

        Args:
            query: 查询文本
            n_results: 返回结果数量
            gender_filter: 男女频过滤 ('male', 'female', None)

        Returns:
            [(文档索引, 相似度分数), ...]
        """
        # 分词
        query_seg = ' '.join(jieba.cut(query))

        # TF-IDF向量化
        query_vec = self.tfidf_vectorizer.transform([query_seg])

        # 计算相似度
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        # 应用男女频过滤
        if gender_filter:
            for i, gender in enumerate(self.genders):
                if gender != gender_filter:
                    similarities[i] = 0

        # 排序
        top_indices = np.argsort(similarities)[::-1][:n_results]
        results = [(idx, similarities[idx]) for idx in top_indices if similarities[idx] > 0]

        return results

    def hybrid_search(self, query: str, n_results: int = 5,
                     semantic_weight: float = 0.6, keyword_weight: float = 0.4,
                     gender_filter: Optional[str] = None) -> List[Dict]:
        """
        混合搜索

        Args:
            query: 查询文本
            n_results: 返回结果数量
            semantic_weight: 语义搜索权重
            keyword_weight: 关键词搜索权重
            gender_filter: 男女频过滤 ('male', 'female', None)

        Returns:
            搜索结果列表
        """
        # 语义搜索
        semantic_results = self.semantic_search(query, n_results * 2, gender_filter)

        # 关键词搜索
        keyword_results = self.keyword_search(query, n_results * 2, gender_filter)

        # 合并结果
        scores = {}
        for idx, score in semantic_results:
            scores[idx] = scores.get(idx, 0) + score * semantic_weight

        for idx, score in keyword_results:
            scores[idx] = scores.get(idx, 0) + score * keyword_weight

        # 排序
        sorted_indices = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # 构建结果
        results = []
        for idx in sorted_indices[:n_results]:
            results.append({
                'filename': self.filenames[idx],
                'filepath': self.file_paths[idx],
                'gender': self.genders[idx],
                'score': scores[idx],
                'semantic_score': dict(semantic_results).get(idx, 0),
                'keyword_score': dict(keyword_results).get(idx, 0),
                'preview': self.documents[idx][:200]
            })

        return results

    def search(self, query: str, n_results: int = 5, gender_filter: Optional[str] = None, **kwargs):
        """
        执行搜索并打印结果

        Args:
            query: 查询文本
            n_results: 返回结果数量
            gender_filter: 男女频过滤 ('male', 'female', None)
            **kwargs: 其他参数（semantic_weight, keyword_weight）
        """
        results = self.hybrid_search(query, n_results=n_results, gender_filter=gender_filter, **kwargs)

        gender_label = {'male': '男频', 'female': '女频', 'unknown': '未知'}.get(gender_filter, '全部')
        print(f"\n搜索查询: {query} (类型: {gender_label})")
        print(f"找到 {len(results)} 个结果\n")
        print("=" * 80)

        for i, result in enumerate(results, 1):
            gender_tag = {'male': '[男频]', 'female': '[女频]', 'unknown': '[未知]'}[result['gender']]
            print(f"\n{i}. {gender_tag} {result['filename']}")
            print(f"   综合得分: {result['score']:.3f} "
                  f"(语义: {result['semantic_score']:.3f}, "
                  f"关键词: {result['keyword_score']:.3f})")
            print(f"   预览: {result['preview'][:100]}...")
            print("-" * 80)

        return results


def main():
    """主函数"""
    import sys

    # 初始化搜索引擎
    md_dir = "knowledge/hit-scripts-md"
    if not Path(md_dir).exists():
        print(f"未找到本地剧本语料目录: {md_dir}")
        print("开源版默认不包含该目录；请放入你有权使用的 .md 剧本语料后重试。")
        sys.exit(0)

    engine = ImprovedHybridSearchEngine(md_dir)

    print("\n" + "=" * 80)
    print("混合搜索系统已就绪！")
    print("=" * 80)

    # 如果有命令行参数，执行单次搜索后退出
    if len(sys.argv) >= 2:
        query = sys.argv[1]
        gender_filter = sys.argv[2] if len(sys.argv) >= 3 else None

        # 验证gender_filter
        if gender_filter == 'all':
            gender_filter = None
        if gender_filter and gender_filter not in ['male', 'female']:
            print(f"错误：gender_filter 必须是 'male'、'female' 或 'all'，当前值: {gender_filter}")
            sys.exit(1)

        print(f"\n命令行查询: {query} (类型: {gender_filter or '全部'})")
        results = engine.search(query, n_results=5, gender_filter=gender_filter)

        # 输出文件名列表（供agent使用）
        print("\n" + "=" * 80)
        print("检索到的文件列表:")
        for i, result in enumerate(results, 1):
            gender_tag = {'male': '[男频]', 'female': '[女频]', 'unknown': '[未知]'}[result['gender']]
            print(f"{i}. {gender_tag} {result['filename']}")
        return

    # 交互式搜索
    while True:
        print("\n请输入搜索查询（输入 'q' 退出）:")
        query = input("> ").strip()

        if query.lower() == 'q':
            print("再见！")
            break

        if not query:
            continue

        print("\n请选择类型（male/female/all，默认all）:")
        gender_input = input("> ").strip().lower()

        gender_filter = None
        if gender_input == 'male':
            gender_filter = 'male'
        elif gender_input == 'female':
            gender_filter = 'female'

        # 执行搜索
        engine.search(query, n_results=5, gender_filter=gender_filter)


if __name__ == "__main__":
    main()
