"""
PromptForge - 轻量级终端AI Prompt智能管理与优化引擎
======================================================
Lightweight Terminal AI Prompt Manager & Optimizer

一个零外部依赖的Python CLI工具，用于管理、评分、搜索和优化AI Prompt。
A zero-dependency Python CLI tool for managing, scoring, searching,
and optimizing AI prompts.

Features / 特性:
- SQLite存储 / SQLite storage
- TF-IDF搜索 / TF-IDF search
- 多维度质量评分 / Multi-dimensional quality scoring
- 多格式导出 / Multi-format export (JSON/YAML/Markdown)
- TUI交互式仪表盘 / TUI interactive dashboard
- 版本管理 / Version management
- 零外部依赖 / Zero external dependencies

Usage / 用法:
    from promptforge import PromptManager

    manager = PromptManager()
    prompt = manager.add_prompt(
        title="翻译助手",
        content="你是一个专业翻译专家...",
        tags=["翻译", "工具"],
    )

Author: PromptForge Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "PromptForge Team"
__license__ = "MIT"

from .models import Prompt, PromptVersion, Tag, ScoreResult, SearchResult
from .engine import PromptManager
from .scorer import PromptScorer
from .searcher import TFIDFSearcher
from .exporter import Exporter

__all__ = [
    "Prompt",
    "PromptVersion",
    "Tag",
    "ScoreResult",
    "SearchResult",
    "PromptManager",
    "PromptScorer",
    "TFIDFSearcher",
    "Exporter",
]
