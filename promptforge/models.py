"""
PromptForge - 数据模型定义 / Data Models
==========================================

定义Prompt、PromptVersion、Tag等核心数据结构。
Define core data structures: Prompt, PromptVersion, Tag.

Author: PromptForge Team
Version: 1.0.0
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
import json


@dataclass
class Prompt:
    """Prompt数据模型 / Prompt data model

    Attributes:
        id: 唯一标识符（UUID）/ Unique identifier (UUID)
        title: 标题 / Title
        content: 内容 / Content
        category: 分类 / Category
        tags: 标签列表 / Tag list
        score: 质量评分（0-100）/ Quality score (0-100)
        created_at: 创建时间（ISO格式）/ Creation time (ISO format)
        updated_at: 更新时间（ISO格式）/ Update time (ISO format)
        version: 当前版本号 / Current version number
        usage_count: 使用次数 / Usage count
    """
    id: str
    title: str
    content: str
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    score: float = 0.0
    created_at: str = ""
    updated_at: str = ""
    version: int = 1
    usage_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """转换为JSON字符串 / Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """从字典创建 / Create from dictionary"""
        # 确保tags是列表 / Ensure tags is a list
        if isinstance(data.get("tags"), str):
            data["tags"] = [t.strip() for t in data["tags"].split(",") if t.strip()]
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "Prompt":
        """从JSON字符串创建 / Create from JSON string"""
        return cls.from_dict(json.loads(json_str))


@dataclass
class PromptVersion:
    """Prompt版本记录 / Prompt version record

    每次编辑prompt时自动保存历史版本。
    Automatically save history version on each edit.

    Attributes:
        id: 版本记录唯一标识符 / Version record unique identifier
        prompt_id: 关联的Prompt ID / Associated Prompt ID
        content: 该版本的内容 / Content of this version
        version: 版本号 / Version number
        created_at: 创建时间（ISO格式）/ Creation time (ISO format)
        change_note: 变更说明 / Change note
    """
    id: str
    prompt_id: str
    content: str
    version: int
    created_at: str
    change_note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """转换为JSON字符串 / Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class Tag:
    """标签数据模型 / Tag data model

    Attributes:
        name: 标签名称 / Tag name
        count: 关联的prompt数量 / Number of associated prompts
    """
    name: str
    count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return asdict(self)


@dataclass
class UsageLog:
    """使用日志记录 / Usage log record

    Attributes:
        id: 日志唯一标识符 / Log unique identifier
        prompt_id: 关联的Prompt ID / Associated Prompt ID
        used_at: 使用时间（ISO格式）/ Usage time (ISO format)
    """
    id: str
    prompt_id: str
    used_at: str

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return asdict(self)


@dataclass
class ScoreResult:
    """评分结果 / Score result

    Attributes:
        total_score: 总分（0-100）/ Total score (0-100)
        length_score: 长度评分（0-15）/ Length score (0-15)
        structure_score: 结构评分（0-25）/ Structure score (0-25)
        keyword_score: 关键词评分（0-20）/ Keyword score (0-20)
        clarity_score: 清晰度评分（0-20）/ Clarity score (0-20)
        completeness_score: 完整性评分（0-20）/ Completeness score (0-20)
        suggestions: 优化建议列表 / Optimization suggestions list
    """
    total_score: float = 0.0
    length_score: float = 0.0
    structure_score: float = 0.0
    keyword_score: float = 0.0
    clarity_score: float = 0.0
    completeness_score: float = 0.0
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return asdict(self)

    def to_display(self) -> str:
        """生成评分展示文本 / Generate score display text"""
        lines = [
            f"{'='*50}",
            f"  Prompt质量评分报告 / Quality Score Report",
            f"{'='*50}",
            f"  总分 Total Score:    {self.total_score:.1f}/100",
            f"{'-'*50}",
            f"  长度 Length:         {self.length_score:.1f}/15",
            f"  结构 Structure:      {self.structure_score:.1f}/25",
            f"  关键词 Keywords:     {self.keyword_score:.1f}/20",
            f"  清晰度 Clarity:      {self.clarity_score:.1f}/20",
            f"  完整性 Completeness: {self.completeness_score:.1f}/20",
            f"{'='*50}",
        ]
        if self.suggestions:
            lines.append("  优化建议 / Suggestions:")
            for i, suggestion in enumerate(self.suggestions, 1):
                lines.append(f"    {i}. {suggestion}")
            lines.append(f"{'='*50}")
        return "\n".join(lines)


@dataclass
class SearchResult:
    """搜索结果 / Search result

    Attributes:
        prompt: 匹配的Prompt对象 / Matched Prompt object
        score: 匹配得分 / Match score
        highlights: 高亮片段列表 / Highlight snippets list
        doc_id: 文档ID（用于从数据库查找prompt）/ Document ID for DB lookup
    """
    prompt: Optional[Prompt] = None
    score: float = 0.0
    highlights: List[str] = field(default_factory=list)
    doc_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return {
            "prompt": self.prompt.to_dict() if self.prompt else None,
            "score": self.score,
            "highlights": self.highlights,
            "doc_id": self.doc_id,
        }
