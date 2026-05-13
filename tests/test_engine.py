"""
PromptForge - 核心引擎测试 / Core Engine Tests
================================================

测试PromptManager的CRUD操作、列表过滤和统计功能。
Test PromptManager CRUD operations, list filtering and statistics.

Author: PromptForge Team
Version: 1.0.0
"""

import unittest
import tempfile
import os
import sys

# 确保可以导入包 / Ensure package can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptforge.engine import PromptManager
from promptforge.models import Prompt


class TestPromptManagerCRUD(unittest.TestCase):
    """PromptManager CRUD操作测试 / PromptManager CRUD operation tests"""

    def setUp(self):
        """测试前准备 / Setup before tests"""
        # 使用临时数据库 / Use temporary database
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.manager = PromptManager(db_path=self.db_path)

    def tearDown(self):
        """测试后清理 / Cleanup after tests"""
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_add_prompt(self):
        """测试添加prompt / Test adding prompt"""
        prompt = self.manager.add_prompt(
            title="Test Prompt",
            content="This is a test prompt for testing purposes.",
            category="testing",
            tags=["test", "unit"],
        )

        self.assertIsNotNone(prompt)
        self.assertEqual(prompt.title, "Test Prompt")
        self.assertEqual(prompt.category, "testing")
        self.assertEqual(prompt.tags, ["test", "unit"])
        self.assertEqual(prompt.version, 1)
        self.assertGreater(prompt.score, 0)

    def test_add_prompt_with_empty_title(self):
        """测试空标题验证 / Test empty title validation"""
        with self.assertRaises(ValueError):
            self.manager.add_prompt(title="", content="Some content")

    def test_add_prompt_with_empty_content(self):
        """测试空内容验证 / Test empty content validation"""
        with self.assertRaises(ValueError):
            self.manager.add_prompt(title="Title", content="")

    def test_get_prompt(self):
        """测试获取prompt / Test getting prompt"""
        created = self.manager.add_prompt(
            title="Get Test",
            content="Content for get test",
        )

        retrieved = self.manager.get_prompt(created.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Get Test")
        self.assertEqual(retrieved.content, "Content for get test")

    def test_get_prompt_by_short_id(self):
        """测试短ID获取 / Test getting by short ID"""
        created = self.manager.add_prompt(
            title="Short ID Test",
            content="Content",
        )

        short_id = created.id[:8]
        retrieved = self.manager.get_prompt(short_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, created.id)

    def test_get_nonexistent_prompt(self):
        """测试获取不存在的prompt / Test getting nonexistent prompt"""
        result = self.manager.get_prompt("nonexistent-id")
        self.assertIsNone(result)

    def test_edit_prompt(self):
        """测试编辑prompt / Test editing prompt"""
        created = self.manager.add_prompt(
            title="Original Title",
            content="Original content",
            tags=["original"],
        )

        updated = self.manager.edit_prompt(
            prompt_id=created.id,
            title="Updated Title",
            content="Updated content",
            tags=["updated"],
            change_note="Test update",
        )

        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.content, "Updated content")
        self.assertEqual(updated.tags, ["updated"])
        self.assertEqual(updated.version, 2)

    def test_edit_prompt_partial(self):
        """测试部分编辑 / Test partial edit"""
        created = self.manager.add_prompt(
            title="Partial Edit Test",
            content="Original content",
            category="original_cat",
        )

        updated = self.manager.edit_prompt(
            prompt_id=created.id,
            title="New Title Only",
        )

        self.assertEqual(updated.title, "New Title Only")
        self.assertEqual(updated.content, "Original content")
        self.assertEqual(updated.category, "original_cat")

    def test_delete_prompt(self):
        """测试删除prompt / Test deleting prompt"""
        created = self.manager.add_prompt(
            title="Delete Test",
            content="To be deleted",
        )

        result = self.manager.delete_prompt(created.id)
        self.assertTrue(result)

        # 验证已删除 / Verify deleted
        retrieved = self.manager.get_prompt(created.id)
        self.assertIsNone(retrieved)

    def test_delete_nonexistent_prompt(self):
        """测试删除不存在的prompt / Test deleting nonexistent prompt"""
        result = self.manager.delete_prompt("nonexistent-id")
        self.assertFalse(result)

    def test_list_prompts(self):
        """测试列出prompts / Test listing prompts"""
        # 添加多个prompts / Add multiple prompts
        self.manager.add_prompt(title="Prompt 1", content="Content 1", category="cat1")
        self.manager.add_prompt(title="Prompt 2", content="Content 2", category="cat2")
        self.manager.add_prompt(title="Prompt 3", content="Content 3", category="cat1")

        prompts = self.manager.list_prompts()
        self.assertEqual(len(prompts), 3)

    def test_list_prompts_with_category_filter(self):
        """测试分类过滤 / Test category filter"""
        self.manager.add_prompt(title="Cat1 A", content="Content", category="cat1")
        self.manager.add_prompt(title="Cat2 A", content="Content", category="cat2")
        self.manager.add_prompt(title="Cat1 B", content="Content", category="cat1")

        prompts = self.manager.list_prompts(category="cat1")
        self.assertEqual(len(prompts), 2)

    def test_list_prompts_with_tag_filter(self):
        """测试标签过滤 / Test tag filter"""
        self.manager.add_prompt(title="Tagged 1", content="Content", tags=["python"])
        self.manager.add_prompt(title="Tagged 2", content="Content", tags=["java"])
        self.manager.add_prompt(title="Tagged 3", content="Content", tags=["python", "tool"])

        prompts = self.manager.list_prompts(tag="python")
        self.assertEqual(len(prompts), 2)

    def test_list_prompts_with_sort(self):
        """测试排序 / Test sorting"""
        self.manager.add_prompt(title="A", content="Content A")
        self.manager.add_prompt(title="B", content="Content B")
        self.manager.add_prompt(title="C", content="Content C")

        # 按标题升序 / Sort by title ascending
        prompts = self.manager.list_prompts(sort_by="title", sort_order="asc")
        titles = [p.title for p in prompts]
        self.assertEqual(titles, ["A", "B", "C"])

    def test_list_prompts_with_limit(self):
        """测试数量限制 / Test limit"""
        for i in range(10):
            self.manager.add_prompt(title=f"Prompt {i}", content="Content")

        prompts = self.manager.list_prompts(limit=5)
        self.assertEqual(len(prompts), 5)

    def test_count_prompts(self):
        """测试统计数量 / Test count"""
        self.manager.add_prompt(title="A", content="Content")
        self.manager.add_prompt(title="B", content="Content")

        count = self.manager.count_prompts()
        self.assertEqual(count, 2)

    def test_version_history(self):
        """测试版本历史 / Test version history"""
        created = self.manager.add_prompt(
            title="Version Test",
            content="Version 1 content",
        )

        # 第一次编辑 / First edit
        self.manager.edit_prompt(
            prompt_id=created.id,
            content="Version 2 content",
            change_note="Update to v2",
        )

        # 第二次编辑 / Second edit
        self.manager.edit_prompt(
            prompt_id=created.id,
            content="Version 3 content",
            change_note="Update to v3",
        )

        versions = self.manager.get_versions(created.id)
        self.assertEqual(len(versions), 2)  # 两个历史版本 / Two history versions

    def test_tags_management(self):
        """测试标签管理 / Test tag management"""
        self.manager.add_prompt(title="T1", content="Content for tag test one", tags=["python", "ai"])
        self.manager.add_prompt(title="T2", content="Content for tag test two", tags=["python", "ml"])
        self.manager.add_prompt(title="T3", content="Content for tag test three", tags=["java"])

        tags = self.manager.get_all_tags()
        tag_names = {t.name for t in tags}

        self.assertIn("python", tag_names)
        self.assertIn("ai", tag_names)
        self.assertIn("ml", tag_names)
        self.assertIn("java", tag_names)

        # python标签应该有2个prompt / python tag should have 2 prompts
        python_tag = next(t for t in tags if t.name == "python")
        self.assertEqual(python_tag.count, 2)

    def test_statistics(self):
        """测试统计信息 / Test statistics"""
        self.manager.add_prompt(title="S1", content="Content", category="cat1")
        self.manager.add_prompt(title="S2", content="Content", category="cat2")

        stats = self.manager.get_stats()
        self.assertEqual(stats["total_prompts"], 2)
        self.assertIn("cat1", stats["categories"])
        self.assertIn("cat2", stats["categories"])

    def test_display_prompt(self):
        """测试显示prompt / Test display prompt"""
        created = self.manager.add_prompt(
            title="Display Test",
            content="Display content",
        )

        display = self.manager.display_prompt(created.id)
        self.assertIn("Display Test", display)
        self.assertIn("Display content", display)

    def test_display_prompt_list(self):
        """测试显示prompt列表 / Test display prompt list"""
        self.manager.add_prompt(title="List Test 1", content="Content")
        self.manager.add_prompt(title="List Test 2", content="Content")

        prompts = self.manager.list_prompts()
        display = self.manager.display_prompt_list(prompts)
        self.assertIn("List Test", display)


class TestPromptManagerSearch(unittest.TestCase):
    """PromptManager搜索测试 / PromptManager search tests"""

    def setUp(self):
        """测试前准备 / Setup before tests"""
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.manager = PromptManager(db_path=self.db_path)

        # 添加测试数据 / Add test data
        self.manager.add_prompt(
            title="Python编程助手",
            content="你是一个Python编程专家，帮助用户编写高质量的Python代码。请提供清晰的代码示例和解释。",
            tags=["python", "coding", "ai"],
        )
        self.manager.add_prompt(
            title="翻译工具",
            content="你是一个专业翻译工具，支持中英文互译。请保持原文语义，确保翻译准确流畅。",
            tags=["translation", "tool"],
        )
        self.manager.add_prompt(
            title="数据分析报告",
            content="分析以下数据并生成报告。请包含数据摘要、趋势分析和可视化建议。",
            tags=["data", "analysis"],
        )

    def tearDown(self):
        """测试后清理 / Cleanup after tests"""
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_search_by_keyword(self):
        """测试关键词搜索 / Test keyword search"""
        results = self.manager.search("Python")
        self.assertGreater(len(results), 0)

        # 第一个结果应该是Python相关的 / First result should be Python related
        found = any("Python" in (r.prompt.title if r.prompt else "") for r in results)
        self.assertTrue(found)

    def test_search_by_chinese(self):
        """测试中文搜索 / Test Chinese search"""
        results = self.manager.search("翻译")
        self.assertGreater(len(results), 0)

    def test_search_no_results(self):
        """测试无结果搜索 / Test search with no results"""
        results = self.manager.search("xyznonexistent12345")
        # 可能返回空列表或低分结果 / May return empty or low-score results
        self.assertIsInstance(results, list)

    def test_search_by_tag(self):
        """测试标签搜索 / Test tag search"""
        results = self.manager.search("python")
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()
