"""
PromptForge - 评分引擎测试 / Scorer Engine Tests
==================================================

测试PromptScorer的各维度评分功能。
Test PromptScorer's multi-dimensional scoring functions.

Author: PromptForge Team
Version: 1.0.0
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptforge.scorer import PromptScorer
from promptforge.models import ScoreResult


class TestPromptScorerLength(unittest.TestCase):
    """长度评分测试 / Length score tests"""

    def setUp(self):
        self.scorer = PromptScorer()

    def test_very_short_content(self):
        """极短内容应得低分 / Very short content should get low score"""
        result = self.scorer.score("Hi")
        self.assertLess(result.length_score, 5)

    def test_short_content(self):
        """短内容应得较低分 / Short content should get low score"""
        result = self.scorer.score("This is a short prompt.")
        self.assertLess(result.length_score, 8)

    def test_optimal_length(self):
        """最佳长度应得满分 / Optimal length should get full score"""
        content = "This is a prompt of optimal length. " * 10
        result = self.scorer.score(content)
        self.assertGreaterEqual(result.length_score, 14)

    def test_very_long_content(self):
        """超长内容应得中等分 / Very long content should get medium score"""
        content = "This is a very long prompt. " * 500
        result = self.scorer.score(content)
        self.assertGreater(result.length_score, 5)
        self.assertLess(result.length_score, 15)


class TestPromptScorerStructure(unittest.TestCase):
    """结构评分测试 / Structure score tests"""

    def setUp(self):
        self.scorer = PromptScorer()

    def test_no_structure(self):
        """无结构应得低分 / No structure should get low score"""
        result = self.scorer.score("just some random text without any structure")
        self.assertLess(result.structure_score, 10)

    def test_with_role(self):
        """有角色设定应加分 / Having role setting should add score"""
        content = "You are a Python expert. Please help me with coding."
        result = self.scorer.score(content)
        self.assertGreater(result.structure_score, 5)

    def test_full_structure(self):
        """完整结构应得高分 / Full structure should get high score"""
        content = """You are a professional data analyst.

Task: Analyze the following sales data and generate a comprehensive report.

Context: The data covers Q1-Q4 2024 sales across all regions.

Requirements:
- Include summary statistics
- Identify top 5 products
- Provide trend analysis

Output format: Markdown table with charts description.

Example: See the attached sample report for reference format."""
        result = self.scorer.score(content)
        self.assertGreater(result.structure_score, 15)

    def test_chinese_structure(self):
        """中文结构检测 / Chinese structure detection"""
        content = """你是一个专业翻译专家。

任务：将以下英文文本翻译为中文。

要求：
- 保持原文语义
- 确保翻译流畅
- 使用专业术语

输出格式：Markdown格式"""
        result = self.scorer.score(content)
        self.assertGreater(result.structure_score, 10)


class TestPromptScorerKeywords(unittest.TestCase):
    """关键词评分测试 / Keyword score tests"""

    def setUp(self):
        self.scorer = PromptScorer()

    def test_no_action_verbs(self):
        """无行动动词应得低分 / No action verbs should get low score"""
        result = self.scorer.score("the sky is blue and the grass is green")
        self.assertLess(result.keyword_score, 5)

    def test_with_action_verbs(self):
        """有行动动词应加分 / Having action verbs should add score"""
        content = "Please analyze the data and generate a summary report."
        result = self.scorer.score(content)
        self.assertGreater(result.keyword_score, 3)

    def test_with_specific_terms(self):
        """有专业术语应加分 / Having specific terms should add score"""
        content = "Write a Python function to analyze JSON data using the pandas API."
        result = self.scorer.score(content)
        self.assertGreater(result.keyword_score, 5)

    def test_chinese_action_verbs(self):
        """中文行动动词检测 / Chinese action verb detection"""
        content = "请分析以下数据，生成报告并优化代码结构。"
        result = self.scorer.score(content)
        self.assertGreater(result.keyword_score, 3)


class TestPromptScorerClarity(unittest.TestCase):
    """清晰度评分测试 / Clarity score tests"""

    def setUp(self):
        self.scorer = PromptScorer()

    def test_clear_sentences(self):
        """清晰句子应得高分 / Clear sentences should get high score"""
        content = "Analyze the data. Generate a report. Identify trends. Provide recommendations."
        result = self.scorer.score(content)
        self.assertGreater(result.clarity_score, 8)

    def test_redundant_text(self):
        """冗余文本应扣分 / Redundant text should lose score"""
        content = "Please note that it is important to note that the data should be analyzed. " * 5
        result = self.scorer.score(content)
        # 冗余应该导致扣分 / Redundancy should cause score deduction
        self.assertLess(result.clarity_score, 15)


class TestPromptScorerCompleteness(unittest.TestCase):
    """完整性评分测试 / Completeness score tests"""

    def setUp(self):
        self.scorer = PromptScorer()

    def test_minimal_content(self):
        """最小内容应得低分 / Minimal content should get low score"""
        result = self.scorer.score("Do something")
        self.assertLess(result.completeness_score, 5)

    def test_with_constraints(self):
        """有约束条件应加分 / Having constraints should add score"""
        content = "Generate a report. Must not exceed 500 words. Avoid technical jargon."
        result = self.scorer.score(content)
        self.assertGreaterEqual(result.completeness_score, 3)

    def test_with_examples(self):
        """有示例应加分 / Having examples should add score"""
        content = "Translate the text. For example, 'hello' should become '你好'."
        result = self.scorer.score(content)
        self.assertGreater(result.completeness_score, 3)

    def test_full_completeness(self):
        """完整内容应得高分 / Full content should get high score"""
        content = """Analyze the sales data.

Constraints:
- Must include all regions
- Do not exclude any quarter
- Ensure accuracy

Example output format:
| Region | Q1 | Q2 | Q3 | Q4 |
|--------|----|----|----|----|

If data is missing, note it as N/A.
Otherwise, calculate the sum."""
        result = self.scorer.score(content)
        self.assertGreater(result.completeness_score, 5)


class TestPromptScorerOverall(unittest.TestCase):
    """综合评分测试 / Overall scoring tests"""

    def setUp(self):
        self.scorer = PromptScorer()

    def test_excellent_prompt(self):
        """优秀prompt应得高分 / Excellent prompt should get high score"""
        content = """You are a senior Python developer with 10 years of experience.

Task: Review the following code and provide optimization suggestions.

Context: This code is part of a web application handling user authentication.

Requirements:
- Identify performance bottlenecks
- Suggest improvements for readability
- Check for security vulnerabilities
- Ensure PEP 8 compliance

Output format:
1. Summary of issues found
2. Detailed suggestions with code examples
3. Priority ranking (High/Medium/Low)

Example:
Before: x = [i for i in range(1000) if i % 2 == 0]
After: x = list(range(0, 1000, 2))

Please analyze step by step."""
        result = self.scorer.score(content)
        self.assertGreater(result.total_score, 70)

    def test_poor_prompt(self):
        """差prompt应得低分 / Poor prompt should get low score"""
        content = "fix code"
        result = self.scorer.score(content)
        self.assertLess(result.total_score, 30)

    def test_score_result_display(self):
        """测试评分结果展示 / Test score result display"""
        content = "Test prompt content"
        result = self.scorer.score(content)
        display = result.to_display()
        self.assertIn("Prompt", display)
        self.assertIn("Score", display)

    def test_suggestions_generated(self):
        """测试建议生成 / Test suggestions generation"""
        content = "do something"
        result = self.scorer.score(content)
        self.assertGreater(len(result.suggestions), 0)


if __name__ == "__main__":
    unittest.main()
