"""
PromptForge - 搜索引擎测试 / Search Engine Tests
==================================================

测试TFIDFSearcher的索引构建、搜索和模糊匹配功能。
Test TFIDFSearcher's index building, search and fuzzy matching.

Author: PromptForge Team
Version: 1.0.0
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptforge.searcher import TFIDFSearcher
from promptforge.models import Prompt


def _make_prompt(title: str, content: str, pid: str = "test-id") -> Prompt:
    """创建测试用Prompt / Create test Prompt"""
    return Prompt(
        id=pid,
        title=title,
        content=content,
        category="test",
        tags=[],
        score=50.0,
        created_at="2024-01-01T00:00:00+00:00",
        updated_at="2024-01-01T00:00:00+00:00",
        version=1,
        usage_count=0,
    )


class TestTFIDFSearcherIndex(unittest.TestCase):
    """搜索索引测试 / Search index tests"""

    def setUp(self):
        self.searcher = TFIDFSearcher()

    def test_empty_index(self):
        """空索引构建 / Empty index building"""
        self.searcher.build_index([])
        stats = self.searcher.get_index_stats()
        self.assertEqual(stats["document_count"], 0)
        self.assertEqual(stats["vocabulary_size"], 0)

    def test_single_document_index(self):
        """单文档索引 / Single document index"""
        prompts = [_make_prompt("Test", "This is a test document.")]
        self.searcher.build_index(prompts)
        stats = self.searcher.get_index_stats()
        self.assertEqual(stats["document_count"], 1)
        self.assertGreater(stats["vocabulary_size"], 0)

    def test_multiple_documents_index(self):
        """多文档索引 / Multiple documents index"""
        prompts = [
            _make_prompt("Python", "Python programming language", "id1"),
            _make_prompt("Java", "Java programming language", "id2"),
            _make_prompt("Data", "Data analysis and visualization", "id3"),
        ]
        self.searcher.build_index(prompts)
        stats = self.searcher.get_index_stats()
        self.assertEqual(stats["document_count"], 3)
        self.assertGreater(stats["vocabulary_size"], 5)

    def test_chinese_tokenization(self):
        """中文分词 / Chinese tokenization"""
        prompts = [_make_prompt("测试", "这是一个中文测试文档")]
        self.searcher.build_index(prompts)
        stats = self.searcher.get_index_stats()
        self.assertGreater(stats["vocabulary_size"], 0)


class TestTFIDFSearcherSearch(unittest.TestCase):
    """搜索功能测试 / Search function tests"""

    def setUp(self):
        self.searcher = TFIDFSearcher()
        self.prompts = [
            _make_prompt(
                "Python编程助手",
                "你是一个Python编程专家，帮助用户编写高质量的Python代码。提供清晰的代码示例和解释。",
                "id1",
            ),
            _make_prompt(
                "翻译工具",
                "你是一个专业翻译工具，支持中英文互译。保持原文语义，确保翻译准确流畅。",
                "id2",
            ),
            _make_prompt(
                "数据分析报告",
                "分析以下数据并生成报告。包含数据摘要、趋势分析和可视化建议。",
                "id3",
            ),
            _make_prompt(
                "Code Review Expert",
                "You are a senior software engineer specializing in code review. "
                "Analyze code for bugs, performance issues, and style violations.",
                "id4",
            ),
        ]
        self.searcher.build_index(self.prompts)

    def test_search_english_keyword(self):
        """英文关键词搜索 / English keyword search"""
        results = self.searcher.search("Python")
        self.assertGreater(len(results), 0)

    def test_search_chinese_keyword(self):
        """中文关键词搜索 / Chinese keyword search"""
        results = self.searcher.search("翻译")
        self.assertGreater(len(results), 0)

    def test_search_data_analysis(self):
        """数据分析搜索 / Data analysis search"""
        results = self.searcher.search("数据分析")
        self.assertGreater(len(results), 0)

    def test_search_code_review(self):
        """代码审查搜索 / Code review search"""
        results = self.searcher.search("code review")
        self.assertGreater(len(results), 0)

    def test_search_no_results(self):
        """无结果搜索 / No results search"""
        results = self.searcher.search("xyznonexistent12345", min_score=0.5)
        self.assertEqual(len(results), 0)

    def test_search_result_ordering(self):
        """搜索结果排序 / Search result ordering"""
        results = self.searcher.search("Python")
        # 结果应该按分数降序 / Results should be in descending score order
        for i in range(len(results) - 1):
            self.assertGreaterEqual(results[i].score, results[i + 1].score)

    def test_search_limit(self):
        """搜索结果数量限制 / Search result count limit"""
        results = self.searcher.search("a", limit=2)
        self.assertLessEqual(len(results), 2)

    def test_search_without_fuzzy(self):
        """禁用模糊匹配 / Disable fuzzy matching"""
        results = self.searcher.search("Python", fuzzy=False)
        self.assertIsInstance(results, list)

    def test_empty_query(self):
        """空查询 / Empty query"""
        results = self.searcher.search("")
        self.assertEqual(len(results), 0)

    def test_none_query(self):
        """None查询 / None query"""
        results = self.searcher.search(None)
        self.assertEqual(len(results), 0)


class TestTFIDFSearcherFieldSearch(unittest.TestCase):
    """字段搜索测试 / Field search tests"""

    def setUp(self):
        self.searcher = TFIDFSearcher()
        self.prompts = [
            _make_prompt("Python Guide", "A comprehensive guide to Python programming.", "id1"),
            _make_prompt("Java Guide", "A comprehensive guide to Java programming.", "id2"),
        ]
        self.searcher.build_index(self.prompts)

    def test_search_all_fields(self):
        """搜索所有字段 / Search all fields"""
        results = self.searcher.search_by_field("Python", field="all")
        self.assertGreater(len(results), 0)

    def test_search_title_field(self):
        """搜索标题字段 / Search title field"""
        results = self.searcher.search_by_field("Python", field="title")
        self.assertGreater(len(results), 0)

    def test_search_content_field(self):
        """搜索内容字段 / Search content field"""
        results = self.searcher.search_by_field("programming", field="content")
        self.assertGreater(len(results), 0)


class TestTFIDFSearcherHighlight(unittest.TestCase):
    """高亮功能测试 / Highlight function tests"""

    def setUp(self):
        self.searcher = TFIDFSearcher()
        self.prompts = [
            _make_prompt(
                "Test Title",
                "This is a test document about Python programming and data analysis.",
                "id1",
            ),
        ]
        self.searcher.build_index(self.prompts)

    def test_search_highlights(self):
        """搜索高亮 / Search highlights"""
        results = self.searcher.search("Python")
        if results and results[0].highlights:
            self.assertIsInstance(results[0].highlights, list)
            self.assertGreater(len(results[0].highlights[0]), 0)


class TestTFIDFSearcherIndexStats(unittest.TestCase):
    """索引统计测试 / Index stats tests"""

    def test_index_stats(self):
        """索引统计 / Index stats"""
        searcher = TFIDFSearcher()
        prompts = [
            _make_prompt("A", "Content A", "id1"),
            _make_prompt("B", "Content B", "id2"),
        ]
        searcher.build_index(prompts)
        stats = searcher.get_index_stats()

        self.assertEqual(stats["document_count"], 2)
        self.assertGreater(stats["vocabulary_size"], 0)
        self.assertGreater(stats["idf_entries"], 0)


if __name__ == "__main__":
    unittest.main()
