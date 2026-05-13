"""
PromptForge - Prompt质量评分引擎 / Prompt Quality Scoring Engine
==================================================================

对Prompt进行多维度质量评分并提供优化建议。
Evaluate prompt quality across multiple dimensions
and provide optimization suggestions.

评分维度（总分100）/ Scoring Dimensions (Total 100):
- 长度评分 Length Score:        0-15
- 结构评分 Structure Score:     0-25
- 关键词评分 Keyword Score:     0-20
- 清晰度评分 Clarity Score:     0-20
- 完整性评分 Completeness Score: 0-20

Author: PromptForge Team
Version: 1.0.0
"""

import re
import math
from typing import List, Tuple
from .models import ScoreResult
from .utils import word_count, char_count


class PromptScorer:
    """Prompt质量评分引擎 / Prompt quality scoring engine

    从长度、结构、关键词、清晰度、完整性五个维度评估Prompt质量。
    Evaluate prompt quality from five dimensions:
    length, structure, keywords, clarity, completeness.
    """

    # 最佳长度范围（字符数）/ Optimal length range (character count)
    OPTIMAL_LENGTH_MIN = 100
    OPTIMAL_LENGTH_MAX = 2000

    # 行动动词 / Action verbs
    ACTION_VERBS = {
        "en": [
            "analyze", "create", "write", "generate", "summarize",
            "explain", "translate", "compare", "evaluate", "list",
            "describe", "identify", "classify", "recommend", "design",
            "implement", "optimize", "refactor", "debug", "test",
            "extract", "convert", "format", "organize", "review",
            "improve", "suggest", "provide", "calculate", "define",
            "demonstrate", "illustrate", "outline", "rewrite", "edit",
            "compose", "draft", "produce", "develop", "build",
        ],
        "zh": [
            "分析", "创建", "编写", "生成", "总结",
            "解释", "翻译", "比较", "评估", "列出",
            "描述", "识别", "分类", "推荐", "设计",
            "实现", "优化", "重构", "调试", "测试",
            "提取", "转换", "格式化", "组织", "审查",
            "改进", "建议", "提供", "计算", "定义",
            "演示", "说明", "概述", "重写", "编辑",
            "撰写", "起草", "制作", "开发", "构建",
            "请", "帮我", "你需要", "作为", "假设",
        ],
    }

    # 结构关键词 / Structure keywords
    STRUCTURE_KEYWORDS = {
        "role": {
            "en": ["role", "act as", "you are", "as a", "persona", "expert", "specialist"],
            "zh": ["角色", "作为", "你是", "扮演", "身份", "专家", "助手", "顾问"],
        },
        "task": {
            "en": ["task", "objective", "goal", "purpose", "mission", "please", "need to"],
            "zh": ["任务", "目标", "目的", "需要", "要求", "请", "帮我"],
        },
        "output_format": {
            "en": ["format", "output", "response", "result", "structure", "template",
                    "json", "markdown", "table", "list", "bullet"],
            "zh": ["格式", "输出", "结果", "结构", "模板", "列表", "表格", "JSON", "Markdown"],
        },
        "context": {
            "en": ["context", "background", "given", "assume", "scenario", "situation"],
            "zh": ["背景", "上下文", "假设", "场景", "情况", "条件", "前提"],
        },
        "constraint": {
            "en": ["constraint", "limit", "restriction", "must", "should", "only",
                    "don't", "avoid", "never", "ensure", "require"],
            "zh": ["约束", "限制", "必须", "不要", "避免", "确保", "要求", "仅", "只能"],
        },
        "example": {
            "en": ["example", "for instance", "such as", "like", "e.g.", "sample",
                    "demonstration", "illustration"],
            "zh": ["例如", "比如", "示例", "样例", "如", "举例", "参考"],
        },
    }

    # 冗余词 / Redundant words
    REDUNDANT_PATTERNS = [
        r"\b(please note that|it is important to note|it should be noted that)\b",
        r"^(okay|sure|alright|well|so)\b",
        r"\b(very|really|quite|rather|somewhat)\s+(very|really|quite)\b",
    ]

    def __init__(self):
        """初始化评分引擎 / Initialize scoring engine"""
        # 合并所有行动动词 / Merge all action verbs
        self._all_action_verbs = set(self.ACTION_VERBS["en"]) | set(self.ACTION_VERBS["zh"])

    def score(self, content: str) -> ScoreResult:
        """对Prompt进行全面评分 / Perform comprehensive scoring on prompt

        Args:
            content: Prompt内容 / Prompt content

        Returns:
            ScoreResult: 评分结果对象 / Score result object
        """
        result = ScoreResult()

        # 计算各维度分数 / Calculate dimension scores
        result.length_score = self._score_length(content)
        result.structure_score = self._score_structure(content)
        result.keyword_score = self._score_keywords(content)
        result.clarity_score = self._score_clarity(content)
        result.completeness_score = self._score_completeness(content)

        # 计算总分 / Calculate total score
        result.total_score = (
            result.length_score
            + result.structure_score
            + result.keyword_score
            + result.clarity_score
            + result.completeness_score
        )

        # 生成优化建议 / Generate optimization suggestions
        result.suggestions = self._generate_suggestions(content, result)

        return result

    def _score_length(self, content: str) -> float:
        """长度评分（0-15）/ Length score (0-15)

        100-2000字符为最佳范围。
        100-2000 characters is the optimal range.

        Args:
            content: Prompt内容 / Prompt content

        Returns:
            float: 长度评分 / Length score
        """
        length = len(content.strip())

        if length < 20:
            return 1.0  # 极短 / Extremely short
        elif length < 50:
            return 3.0  # 太短 / Too short
        elif length < self.OPTIMAL_LENGTH_MIN:
            # 线性增长到最佳范围 / Linear increase to optimal range
            ratio = (length - 50) / (self.OPTIMAL_LENGTH_MIN - 50)
            return 3.0 + ratio * 7.0
        elif length <= self.OPTIMAL_LENGTH_MAX:
            return 15.0  # 最佳范围 / Optimal range
        elif length <= 5000:
            # 超出最佳范围，缓慢下降 / Beyond optimal, slowly decrease
            ratio = (length - self.OPTIMAL_LENGTH_MAX) / (5000 - self.OPTIMAL_LENGTH_MAX)
            return 15.0 - ratio * 5.0
        else:
            return 8.0  # 过长 / Too long

    def _score_structure(self, content: str) -> float:
        """结构评分（0-25）/ Structure score (0-25)

        检查是否包含角色设定、任务描述、输出格式等结构要素。
        Check for structural elements: role setting, task description,
        output format, etc.

        Args:
            content: str: Prompt内容 / Prompt content

        Returns:
            float: 结构评分 / Structure score
        """
        content_lower = content.lower()
        score = 0.0
        found_elements: List[str] = []

        # 检查各结构要素 / Check each structural element
        for element, keywords in self.STRUCTURE_KEYWORDS.items():
            all_keywords = keywords["en"] + keywords["zh"]
            if any(kw.lower() in content_lower for kw in all_keywords):
                found_elements.append(element)

        # 根据找到的要素数量评分 / Score based on found elements
        element_scores = {
            "role": 6.0,       # 角色设定 / Role setting
            "task": 6.0,       # 任务描述 / Task description
            "output_format": 5.0,  # 输出格式 / Output format
            "context": 4.0,    # 上下文 / Context
            "constraint": 2.0, # 约束条件 / Constraints
            "example": 2.0,    # 示例 / Examples
        }

        for element in found_elements:
            score += element_scores.get(element, 0)

        # 检查分段结构 / Check paragraph structure
        paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
        if len(paragraphs) >= 3:
            score += 2.0  # 有良好的分段 / Good paragraphing
        elif len(paragraphs) >= 2:
            score += 1.0

        # 检查是否有编号或列表 / Check for numbering or lists
        if re.search(r'^\s*[\d\-\*•]\s+', content, re.MULTILINE):
            score += 2.0  # 有列表结构 / Has list structure

        return min(score, 25.0)

    def _score_keywords(self, content: str) -> float:
        """关键词评分（0-20）/ Keyword score (0-20)

        检查是否包含行动动词和具体指令。
        Check for action verbs and specific instructions.

        Args:
            content: Prompt内容 / Prompt content

        Returns:
            float: 关键词评分 / Keyword score
        """
        content_lower = content.lower()

        # 统计行动动词命中数 / Count action verb hits
        action_hits = sum(1 for verb in self._all_action_verbs if verb in content_lower)

        # 行动动词评分（最多10分）/ Action verb score (max 10)
        action_score = min(action_hits * 2.0, 10.0)

        # 检查具体性 / Check specificity
        specificity_score = 0.0

        # 包含数字 / Contains numbers
        if re.search(r'\d+', content):
            specificity_score += 2.0

        # 包含引号（引用）/ Contains quotes (citation)
        if '"' in content or "'" in content or "「" in content or "」" in content:
            specificity_score += 1.5

        # 包含专业术语（简单检测）/ Contains professional terms (simple detection)
        tech_terms = re.findall(
            r'\b(API|JSON|XML|HTML|CSS|SQL|Python|Java|JavaScript|AI|ML|NLP|LLM|GPT|code|data|model|algorithm)\b',
            content,
            re.IGNORECASE,
        )
        if tech_terms:
            specificity_score += min(len(tech_terms) * 1.0, 3.0)

        # 包含具体领域词汇 / Contains domain-specific vocabulary
        domain_indicators = [
            "步骤", "流程", "方法", "标准", "规范",
            "step", "process", "method", "standard", "criteria",
            "first", "then", "finally", "next", "after",
        ]
        domain_hits = sum(1 for d in domain_indicators if d in content_lower)
        specificity_score += min(domain_hits * 1.0, 3.5)

        return min(action_score + specificity_score, 20.0)

    def _score_clarity(self, content: str) -> float:
        """清晰度评分（0-20）/ Clarity score (0-20)

        评估句子长度、冗余程度和表达清晰度。
        Evaluate sentence length, redundancy and expression clarity.

        Args:
            content: Prompt内容 / Prompt content

        Returns:
            float: 清晰度评分 / Clarity score
        """
        score = 10.0  # 基础分 / Base score

        # 1. 句子长度分析 / Sentence length analysis
        sentences = re.split(r'[.!?。！？\n]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if sentences:
            avg_len = sum(len(s) for s in sentences) / len(sentences)

            if avg_len <= 20:
                score += 3.0  # 简洁 / Concise
            elif avg_len <= 50:
                score += 4.0  # 适中 / Moderate
            elif avg_len <= 100:
                score += 2.0  # 稍长 / Slightly long
            elif avg_len <= 200:
                score -= 2.0  # 偏长 / Rather long
            else:
                score -= 4.0  # 过长 / Too long

        # 2. 冗余检测 / Redundancy detection
        redundancy_penalty = 0.0
        for pattern in self.REDUNDANT_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            redundancy_penalty += len(matches) * 1.0

        score -= redundancy_penalty

        # 3. 重复词检测 / Repeated word detection
        words = re.findall(r'\b\w+\b', content.lower())
        if len(words) > 10:
            from collections import Counter
            word_freq = Counter(words)
            # 获取高频词（排除常见停用词）/ Get high-frequency words (exclude stop words)
            stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                          "being", "have", "has", "had", "do", "does", "did", "will",
                          "would", "could", "should", "may", "might", "can", "shall",
                          "to", "of", "in", "for", "on", "with", "at", "by", "from",
                          "as", "into", "through", "during", "before", "after", "and",
                          "but", "or", "nor", "not", "so", "yet", "both", "either",
                          "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
                          "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
                          "你", "会", "着", "没有", "看", "好", "自己", "这"}
            meaningful_words = {w: c for w, c in word_freq.items() if w not in stop_words and len(w) > 1}
            if meaningful_words:
                max_freq = max(meaningful_words.values())
                total_meaningful = sum(meaningful_words.values())
                if total_meaningful > 0:
                    repetition_ratio = max_freq / total_meaningful
                    if repetition_ratio > 0.15:
                        score -= 2.0  # 重复过多 / Too repetitive
                    elif repetition_ratio > 0.10:
                        score -= 1.0

        # 4. 标点使用 / Punctuation usage
        # 有适当的标点分隔 / Has proper punctuation separation
        punctuation_count = len(re.findall(r'[，。！？；：,.!?;:]', content))
        if punctuation_count > 0:
            score += 1.0

        return max(0.0, min(score, 20.0))

    def _score_completeness(self, content: str) -> float:
        """完整性评分（0-20）/ Completeness score (0-20)

        检查约束条件、示例、边界情况等完整性要素。
        Check for completeness elements: constraints, examples,
        edge cases, etc.

        Args:
            content: Prompt内容 / Prompt content

        Returns:
            float: 完整性评分 / Completeness score
        """
        score = 0.0
        content_lower = content.lower()

        # 1. 约束条件（最多6分）/ Constraints (max 6)
        constraint_keywords = [
            "必须", "不要", "避免", "确保", "限制", "仅", "只能", "不超过",
            "must", "should", "don't", "avoid", "ensure", "only", "limit",
            "never", "always", "require", "without", "no more than",
        ]
        constraint_hits = sum(1 for kw in constraint_keywords if kw in content_lower)
        score += min(constraint_hits * 1.5, 6.0)

        # 2. 示例（最多5分）/ Examples (max 5)
        example_indicators = [
            "例如", "比如", "示例", "样例", "如：", "如下",
            "for example", "for instance", "such as", "e.g.", "like:",
            "example:", "sample:", "here is",
        ]
        has_example = any(ind in content_lower for ind in example_indicators)
        if has_example:
            score += 5.0

        # 3. 边界情况处理（最多4分）/ Edge case handling (max 4)
        edge_case_keywords = [
            "如果", "否则", "异常", "错误", "失败", "边界",
            "if", "else", "otherwise", "error", "exception", "fail",
            "edge case", "boundary", "fallback",
        ]
        edge_hits = sum(1 for kw in edge_case_keywords if kw in content_lower)
        score += min(edge_hits * 1.0, 4.0)

        # 4. 明确的输出期望（最多5分）/ Clear output expectations (max 5)
        output_keywords = [
            "输出", "返回", "结果", "格式", "要求",
            "output", "return", "result", "format", "expect",
            "should be", "in the form of", "as follows",
        ]
        output_hits = sum(1 for kw in output_keywords if kw in content_lower)
        score += min(output_hits * 1.25, 5.0)

        return min(score, 20.0)

    def _generate_suggestions(self, content: str, result: ScoreResult) -> List[str]:
        """生成优化建议 / Generate optimization suggestions

        Args:
            content: Prompt内容 / Prompt content
            result: 评分结果 / Score result

        Returns:
            List[str]: 建议列表 / Suggestion list
        """
        suggestions: List[str] = []
        content_lower = content.lower()
        length = len(content.strip())

        # 长度建议 / Length suggestions
        if result.length_score < 5:
            if length < 50:
                suggestions.append(
                    "Prompt太短，建议增加更多细节和上下文信息 "
                    "(Prompt is too short, consider adding more details and context)"
                )
            elif length > 5000:
                suggestions.append(
                    "Prompt过长，建议拆分为多个子任务 "
                    "(Prompt is too long, consider splitting into subtasks)"
                )

        # 结构建议 / Structure suggestions
        if result.structure_score < 10:
            # 检查缺少哪些结构要素 / Check which structural elements are missing
            missing = []
            for element, keywords in self.STRUCTURE_KEYWORDS.items():
                all_keywords = keywords["en"] + keywords["zh"]
                if not any(kw.lower() in content_lower for kw in all_keywords):
                    element_names = {
                        "role": "角色设定 (role setting)",
                        "task": "任务描述 (task description)",
                        "output_format": "输出格式 (output format)",
                        "context": "上下文信息 (context)",
                        "constraint": "约束条件 (constraints)",
                        "example": "示例 (examples)",
                    }
                    missing.append(element_names.get(element, element))

            if missing:
                suggestions.append(
                    f"建议添加以下结构要素: {', '.join(missing[:3])}"
                    f" (Consider adding: {', '.join(missing[:3])})"
                )

        # 关键词建议 / Keyword suggestions
        if result.keyword_score < 8:
            suggestions.append(
                "建议使用更具体的行动动词，如'分析'、'生成'、'比较'等 "
                "(Use more specific action verbs like 'analyze', 'generate', 'compare')"
            )

        # 清晰度建议 / Clarity suggestions
        if result.clarity_score < 10:
            sentences = re.split(r'[.!?。！？\n]+', content)
            sentences = [s.strip() for s in sentences if s.strip()]
            if sentences:
                avg_len = sum(len(s) for s in sentences) / len(sentences)
                if avg_len > 100:
                    suggestions.append(
                        "句子偏长，建议拆分为更短的句子以提高可读性 "
                        "(Sentences are too long, consider splitting for readability)"
                    )

            # 检查冗余 / Check redundancy
            for pattern in self.REDUNDANT_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    suggestions.append(
                        "建议移除冗余表达，使Prompt更简洁 "
                        "(Remove redundant expressions for conciseness)"
                    )
                    break

        # 完整性建议 / Completeness suggestions
        if result.completeness_score < 8:
            suggestions.append(
                "建议添加约束条件和示例，帮助AI更准确地理解需求 "
                "(Add constraints and examples to help AI understand requirements better)"
            )

        # 如果评分很高，给出正面反馈 / If score is high, give positive feedback
        if result.total_score >= 85:
            suggestions.append(
                "Prompt质量优秀！结构清晰、内容完整 "
                "(Excellent prompt quality! Clear structure and complete content)"
            )

        return suggestions
