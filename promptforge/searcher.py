"""
PromptForge - 语义搜索引擎 / Semantic Search Engine
=====================================================

基于TF-IDF的关键词搜索引擎，支持模糊匹配和搜索结果高亮。
TF-IDF based keyword search engine with fuzzy matching
and search result highlighting.

Author: PromptForge Team
Version: 1.0.0
"""

import math
import re
from typing import List, Dict, Optional, Tuple, Set
from collections import Counter

from .models import Prompt, SearchResult
from .utils import similarity, highlight_text, truncate


class TFIDFSearcher:
    """TF-IDF搜索引擎 / TF-IDF search engine

    基于词频-逆文档频率（TF-IDF）算法实现关键词搜索。
    Implement keyword search based on Term Frequency-Inverse Document Frequency.

    Attributes:
        documents: 文档索引 / Document index
        idf: 逆文档频率 / Inverse document frequency
        vocabulary: 词汇表 / Vocabulary
    """

    # 停用词 / Stop words
    STOP_WORDS: Set[str] = {
        # 英文停用词 / English stop words
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "and", "but", "or",
        "nor", "not", "so", "yet", "both", "either", "neither", "each",
        "every", "all", "any", "few", "more", "most", "other", "some",
        "such", "no", "only", "own", "same", "than", "too", "very",
        "just", "because", "if", "when", "where", "how", "what", "which",
        "who", "whom", "this", "that", "these", "those", "i", "me", "my",
        "we", "our", "you", "your", "he", "him", "his", "she", "her",
        "it", "its", "they", "them", "their",
        # 中文停用词 / Chinese stop words
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
        "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
        "你", "会", "着", "没有", "看", "好", "自己", "这", "他", "她",
        "它", "们", "那", "些", "什么", "怎么", "如何", "为什么", "可以",
        "能", "把", "被", "让", "给", "从", "向", "对", "与", "而",
        "但", "却", "又", "还", "已", "已经", "吗", "呢", "吧", "啊",
        "哦", "嗯", "呀", "啦", "哈", "嘛", "呗", "么",
    }

    def __init__(self):
        """初始化搜索引擎 / Initialize search engine"""
        self.documents: Dict[str, Dict[str, float]] = {}  # doc_id -> {term: tf}
        self.idf: Dict[str, float] = {}  # term -> idf value
        self.vocabulary: Set[str] = set()
        self._doc_texts: Dict[str, str] = {}  # doc_id -> raw text
        self._doc_count: int = 0

    def build_index(self, prompts: List[Prompt]) -> None:
        """构建搜索索引 / Build search index

        Args:
            prompts: Prompt列表 / Prompt list
        """
        # 清空现有索引 / Clear existing index
        self.documents.clear()
        self.idf.clear()
        self.vocabulary.clear()
        self._doc_texts.clear()
        self._doc_count = len(prompts)

        if not prompts:
            return

        # 第一步：计算TF / Step 1: Calculate TF
        doc_freq: Counter = Counter()  # 文档频率 / Document frequency

        for prompt in prompts:
            # 合并标题和内容用于索引 / Combine title and content for indexing
            text = f"{prompt.title} {prompt.content}"
            self._doc_texts[prompt.id] = text

            # 分词 / Tokenize
            terms = self._tokenize(text)

            # 计算TF / Calculate TF
            term_freq = Counter(terms)
            total_terms = len(terms) if terms else 1

            tf_dict: Dict[str, float] = {}
            for term, count in term_freq.items():
                tf_dict[term] = count / total_terms
                self.vocabulary.add(term)

            self.documents[prompt.id] = tf_dict

            # 统计文档频率 / Count document frequency
            unique_terms = set(terms)
            for term in unique_terms:
                doc_freq[term] += 1

        # 第二步：计算IDF / Step 2: Calculate IDF
        for term, freq in doc_freq.items():
            self.idf[term] = math.log((self._doc_count + 1) / (freq + 1)) + 1

    def search(
        self,
        query: str,
        limit: int = 10,
        min_score: float = 0.0,
        fuzzy: bool = True,
    ) -> List[SearchResult]:
        """搜索prompts / Search prompts

        Args:
            query: 搜索查询 / Search query
            limit: 返回结果数量限制 / Result count limit
            min_score: 最低匹配分数 / Minimum match score
            fuzzy: 是否启用模糊匹配 / Enable fuzzy matching

        Returns:
            List[SearchResult]: 搜索结果列表 / Search result list
        """
        if not query or not self.documents:
            return []

        # 分词查询 / Tokenize query
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        # 计算查询向量 / Calculate query vector
        query_tf = Counter(query_terms)
        query_total = len(query_terms) if query_terms else 1
        query_vector: Dict[str, float] = {}
        for term, count in query_tf.items():
            query_vector[term] = (count / query_total) * self.idf.get(term, 1.0)

        # 计算每个文档的相似度 / Calculate similarity for each document
        results: List[SearchResult] = []
        query_norm = self._vector_norm(query_vector)

        for doc_id, doc_tf in self.documents.items():
            # 计算余弦相似度 / Calculate cosine similarity
            doc_vector = {term: tf * self.idf.get(term, 1.0) for term, tf in doc_tf.items()}
            doc_norm = self._vector_norm(doc_vector)

            if query_norm == 0 or doc_norm == 0:
                continue

            # 点积 / Dot product
            dot_product = sum(
                query_vector.get(term, 0) * doc_vector.get(term, 0)
                for term in set(query_vector) & set(doc_vector)
            )

            cosine_sim = dot_product / (query_norm * doc_norm)

            # 模糊匹配加分 / Fuzzy matching bonus
            fuzzy_bonus = 0.0
            if fuzzy:
                fuzzy_bonus = self._fuzzy_match_bonus(query, self._doc_texts.get(doc_id, ""))

            total_score = cosine_sim + fuzzy_bonus

            if total_score >= min_score:
                # 生成高亮片段 / Generate highlight snippets
                highlights = self._generate_highlights(query_terms, self._doc_texts.get(doc_id, ""))

                results.append(SearchResult(
                    prompt=None,  # 将在engine层填充 / Will be filled in engine layer
                    score=round(total_score, 4),
                    highlights=highlights,
                    doc_id=doc_id,
                ))

        # 按分数排序 / Sort by score
        results.sort(key=lambda r: r.score, reverse=True)

        return results[:limit]

    def search_by_field(
        self,
        query: str,
        field: str = "all",
        limit: int = 10,
    ) -> List[SearchResult]:
        """按字段搜索 / Search by field

        Args:
            query: 搜索查询 / Search query
            field: 搜索字段（title/content/tags/all）/ Search field
            limit: 返回结果数量 / Result count limit

        Returns:
            List[SearchResult]: 搜索结果列表 / Search result list
        """
        if field == "all":
            return self.search(query, limit=limit)

        results: List[SearchResult] = []
        query_lower = query.lower()
        query_terms = self._tokenize(query)

        for doc_id, doc_text in self._doc_texts.items():
            match_score = 0.0

            if field == "title":
                # 仅搜索标题 / Search title only
                # 从文本中提取标题（第一行或前50字符）/ Extract title from text
                title_part = doc_text.split("\n")[0][:100].lower()
                if query_lower in title_part:
                    match_score = 1.0
                else:
                    match_score = similarity(query_lower, title_part)
            elif field == "content":
                # 仅搜索内容 / Search content only
                content_part = doc_text.lower()
                if query_lower in content_part:
                    match_score = 0.8
                else:
                    match_score = similarity(query_lower, content_part) * 0.5
            elif field == "tags":
                # 搜索标签 / Search tags
                match_score = 0.0  # 标签搜索在engine层处理 / Tag search handled in engine layer

            if match_score > 0.1:
                highlights = self._generate_highlights(query_terms, doc_text)
                results.append(SearchResult(
                    prompt=None,
                    score=round(match_score, 4),
                    highlights=highlights,
                    doc_id=doc_id,
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def _tokenize(self, text: str) -> List[str]:
        """分词处理 / Tokenize text

        支持中英文混合分词。
        Support mixed Chinese-English tokenization.

        Args:
            text: 输入文本 / Input text

        Returns:
            List[str]: 词项列表 / Term list
        """
        text = text.lower()

        # 提取英文单词 / Extract English words
        english_words = re.findall(r'[a-z]+', text)

        # 提取中文字符（单字和双字组合）/ Extract Chinese characters (single and bigrams)
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        chinese_bigrams = [
            chinese_chars[i] + chinese_chars[i + 1]
            for i in range(len(chinese_chars) - 1)
        ]

        # 合并所有词项 / Combine all terms
        all_terms = english_words + chinese_chars + chinese_bigrams

        # 过滤停用词和短词 / Filter stop words and short terms
        filtered = [
            term for term in all_terms
            if term not in self.STOP_WORDS and len(term) >= 1
        ]

        return filtered

    def _vector_norm(self, vector: Dict[str, float]) -> float:
        """计算向量范数 / Calculate vector norm

        Args:
            vector: 词项向量 / Term vector

        Returns:
            float: 向量范数 / Vector norm
        """
        return math.sqrt(sum(v ** 2 for v in vector.values()))

    def _fuzzy_match_bonus(self, query: str, text: str) -> float:
        """计算模糊匹配加分 / Calculate fuzzy match bonus

        Args:
            query: 搜索查询 / Search query
            text: 文档文本 / Document text

        Returns:
            float: 模糊匹配加分 / Fuzzy match bonus
        """
        bonus = 0.0
        query_lower = query.lower()
        text_lower = text.lower()

        # 直接包含加分 / Direct inclusion bonus
        if query_lower in text_lower:
            bonus += 0.3

        # 查询词的模糊匹配 / Fuzzy matching of query terms
        query_words = query_lower.split()
        for word in query_words:
            if len(word) < 3:
                continue
            # 在文本中查找相似片段 / Find similar segments in text
            text_words = text_lower.split()
            for text_word in text_words:
                if len(text_word) < 3:
                    continue
                sim = similarity(word, text_word)
                if sim > 0.7:
                    bonus += sim * 0.1

        return min(bonus, 0.5)  # 最大模糊加分 / Max fuzzy bonus

    def _generate_highlights(
        self,
        query_terms: List[str],
        text: str,
        snippet_length: int = 100,
        max_snippets: int = 3,
    ) -> List[str]:
        """生成搜索高亮片段 / Generate search highlight snippets

        Args:
            query_terms: 查询词项列表 / Query term list
            text: 文档文本 / Document text
            snippet_length: 片段长度 / Snippet length
            max_snippets: 最大片段数 / Max snippets count

        Returns:
            List[str]: 高亮片段列表 / Highlight snippet list
        """
        if not query_terms or not text:
            return []

        highlights: List[str] = []
        text_lower = text.lower()
        found_positions: List[int] = []

        # 查找每个查询词的位置 / Find position of each query term
        for term in query_terms:
            if len(term) < 2:
                continue
            pos = text_lower.find(term)
            if pos != -1:
                found_positions.append(pos)

        if not found_positions:
            return []

        # 去重并排序 / Deduplicate and sort
        found_positions = sorted(set(found_positions))

        # 生成片段 / Generate snippets
        for pos in found_positions[:max_snippets]:
            start = max(0, pos - snippet_length // 4)
            end = min(len(text), pos + snippet_length)

            snippet = text[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."

            highlights.append(snippet)

        return highlights

    def get_index_stats(self) -> Dict[str, int]:
        """获取索引统计信息 / Get index statistics

        Returns:
            Dict[str, int]: 统计信息 / Statistics
        """
        return {
            "document_count": self._doc_count,
            "vocabulary_size": len(self.vocabulary),
            "idf_entries": len(self.idf),
        }
