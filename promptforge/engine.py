"""
PromptForge - 核心引擎 / Core Engine
======================================

封装所有Prompt管理操作，提供统一的业务逻辑接口。
Encapsulate all prompt management operations,
provide unified business logic interface.

Author: PromptForge Team
Version: 1.0.0
"""

import os
from typing import List, Optional, Dict, Any, Tuple

from .models import Prompt, PromptVersion, Tag, ScoreResult, SearchResult, UsageLog
from .database import Database
from .scorer import PromptScorer
from .searcher import TFIDFSearcher
from .exporter import Exporter
from .utils import (
    generate_uuid, now_iso, format_datetime, time_ago,
    truncate, validate_prompt_content, validate_title,
    simple_diff, colored, Color,
)


class PromptManager:
    """Prompt管理器 / Prompt Manager

    核心业务逻辑层，协调数据库、评分、搜索和导出模块。
    Core business logic layer, coordinating database,
    scoring, search and export modules.

    Attributes:
        db: 数据库管理器 / Database manager
        scorer: 评分引擎 / Scoring engine
        searcher: 搜索引擎 / Search engine
        exporter: 导出器 / Exporter
    """

    def __init__(self, db_path: Optional[str] = None):
        """初始化Prompt管理器 / Initialize Prompt Manager

        Args:
            db_path: 数据库路径 / Database path
        """
        self.db = Database(db_path)
        self.scorer = PromptScorer()
        self.searcher = TFIDFSearcher()
        self.exporter = Exporter()
        self._rebuild_search_index()

    # ============================================================
    # CRUD 操作 / CRUD Operations
    # ============================================================

    def add_prompt(
        self,
        title: str,
        content: str,
        category: str = "general",
        tags: Optional[List[str]] = None,
        auto_score: bool = True,
    ) -> Prompt:
        """添加新prompt / Add new prompt

        Args:
            title: 标题 / Title
            content: 内容 / Content
            category: 分类 / Category
            tags: 标签列表 / Tag list
            auto_score: 是否自动评分 / Auto score

        Returns:
            Prompt: 创建的Prompt对象 / Created Prompt object

        Raises:
            ValueError: 验证失败 / Validation failed
        """
        # 验证输入 / Validate input
        valid, msg = validate_title(title)
        if not valid:
            raise ValueError(msg)

        valid, msg = validate_prompt_content(content)
        if not valid:
            raise ValueError(msg)

        # 处理标签 / Process tags
        processed_tags = [t.strip() for t in (tags or []) if t.strip()]

        # 自动评分 / Auto score
        score = 0.0
        if auto_score:
            result = self.scorer.score(content)
            score = result.total_score

        # 创建Prompt对象 / Create Prompt object
        now = now_iso()
        prompt = Prompt(
            id=generate_uuid(),
            title=title.strip(),
            content=content.strip(),
            category=category.strip() if category else "general",
            tags=processed_tags,
            score=score,
            created_at=now,
            updated_at=now,
            version=1,
            usage_count=0,
        )

        # 保存到数据库 / Save to database
        self.db.add_prompt(prompt)

        # 重建搜索索引 / Rebuild search index
        self._rebuild_search_index()

        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """获取prompt / Get prompt

        支持完整ID和短ID查询。
        Support full ID and short ID query.

        Args:
            prompt_id: Prompt ID（完整或短ID）/ Prompt ID (full or short)

        Returns:
            Optional[Prompt]: Prompt对象或None / Prompt object or None
        """
        prompt = self.db.get_prompt(prompt_id)
        if not prompt:
            prompt = self.db.get_prompt_by_short_id(prompt_id)
        return prompt

    def edit_prompt(
        self,
        prompt_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        change_note: str = "",
        auto_score: bool = True,
    ) -> Prompt:
        """编辑prompt / Edit prompt

        Args:
            prompt_id: Prompt ID / Prompt ID
            title: 新标题 / New title
            content: 新内容 / New content
            category: 新分类 / New category
            tags: 新标签 / New tags
            change_note: 变更说明 / Change note
            auto_score: 是否自动评分 / Auto score

        Returns:
            Prompt: 更新后的Prompt对象 / Updated Prompt object

        Raises:
            ValueError: Prompt不存在或验证失败 / Prompt not found or validation failed
        """
        # 获取现有prompt / Get existing prompt
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_id}")

        # 验证新值 / Validate new values
        if title is not None:
            valid, msg = validate_title(title)
            if not valid:
                raise ValueError(msg)
            prompt.title = title.strip()

        if content is not None:
            valid, msg = validate_prompt_content(content)
            if not valid:
                raise ValueError(msg)
            prompt.content = content.strip()

        if category is not None:
            prompt.category = category.strip() if category.strip() else "general"

        if tags is not None:
            prompt.tags = [t.strip() for t in tags if t.strip()]

        # 自动评分 / Auto score
        if auto_score and content is not None:
            result = self.scorer.score(prompt.content)
            prompt.score = result.total_score

        prompt.updated_at = now_iso()

        # 更新数据库 / Update database
        updated = self.db.update_prompt(prompt, change_note)

        # 重建搜索索引 / Rebuild search index
        self._rebuild_search_index()

        return updated

    def delete_prompt(self, prompt_id: str) -> bool:
        """删除prompt / Delete prompt

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            bool: 是否删除成功 / Whether deletion was successful
        """
        success = self.db.delete_prompt(prompt_id)
        if success:
            self._rebuild_search_index()
        return success

    # ============================================================
    # 列表和过滤 / List and Filter
    # ============================================================

    def list_prompts(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> List[Prompt]:
        """列出prompts / List prompts

        Args:
            category: 按分类过滤 / Filter by category
            tag: 按标签过滤 / Filter by tag
            sort_by: 排序字段 / Sort field
            sort_order: 排序方向 / Sort direction
            limit: 数量限制 / Count limit
            offset: 偏移量 / Offset

        Returns:
            List[Prompt]: Prompt列表 / Prompt list
        """
        return self.db.list_prompts(
            category=category,
            tag=tag,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
        )

    def count_prompts(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> int:
        """统计prompt数量 / Count prompts

        Args:
            category: 按分类过滤 / Filter by category
            tag: 按标签过滤 / Filter by tag

        Returns:
            int: 数量 / Count
        """
        return self.db.count_prompts(category=category, tag=tag)

    # ============================================================
    # 搜索 / Search
    # ============================================================

    def search(
        self,
        query: str,
        limit: int = 10,
        fuzzy: bool = True,
    ) -> List[SearchResult]:
        """搜索prompts / Search prompts

        Args:
            query: 搜索查询 / Search query
            limit: 结果数量限制 / Result count limit
            fuzzy: 是否启用模糊匹配 / Enable fuzzy matching

        Returns:
            List[SearchResult]: 搜索结果列表 / Search result list
        """
        # 使用TF-IDF搜索 / Use TF-IDF search
        raw_results = self.searcher.search(query, limit=limit * 2, fuzzy=fuzzy)

        # 填充prompt对象 / Fill prompt objects
        results: List[SearchResult] = []
        for raw in raw_results:
            # 通过doc_id查找对应的prompt / Find prompt by doc_id
            lookup_id = raw.doc_id or (raw.prompt.prompt_id if raw.prompt else "")
            prompt = self.db.get_prompt(lookup_id)
            if not prompt:
                continue

            results.append(SearchResult(
                prompt=prompt,
                score=raw.score,
                highlights=raw.highlights,
                doc_id=raw.doc_id,
            ))

        # 标签搜索补充 / Tag search supplement
        tag_results = self._search_by_tag(query, limit)
        existing_ids = {r.prompt.id for r in results if r.prompt}
        for tr in tag_results:
            if tr.prompt and tr.prompt.id not in existing_ids:
                results.append(tr)
                existing_ids.add(tr.prompt.id)

        # 排序并限制数量 / Sort and limit
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def _search_by_tag(self, query: str, limit: int) -> List[SearchResult]:
        """按标签搜索 / Search by tag

        Args:
            query: 搜索查询 / Search query
            limit: 结果数量限制 / Result count limit

        Returns:
            List[SearchResult]: 搜索结果 / Search results
        """
        results: List[SearchResult] = []
        query_lower = query.lower()

        # 获取所有prompts / Get all prompts
        prompts = self.db.list_prompts(limit=1000)
        for prompt in prompts:
            for tag in prompt.tags:
                if query_lower in tag.lower():
                    results.append(SearchResult(
                        prompt=prompt,
                        score=0.5,  # 标签匹配基础分 / Tag match base score
                        highlights=[f"Tag: {tag}"],
                    ))
                    break

        return results[:limit]

    # ============================================================
    # 评分 / Scoring
    # ============================================================

    def score_prompt(self, prompt_id: str) -> Optional[ScoreResult]:
        """对prompt进行评分 / Score a prompt

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            Optional[ScoreResult]: 评分结果或None / Score result or None
        """
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return None

        result = self.scorer.score(prompt.content)

        # 更新数据库中的评分 / Update score in database
        prompt.score = result.total_score
        prompt.updated_at = now_iso()
        self.db.update_prompt(prompt, "Auto score update")

        return result

    def rescore_all(self) -> int:
        """重新评分所有prompts / Rescore all prompts

        Returns:
            int: 重新评分的数量 / Number of rescored prompts
        """
        prompts = self.db.list_prompts(limit=10000)
        count = 0
        for prompt in prompts:
            result = self.scorer.score(prompt.content)
            prompt.score = result.total_score
            prompt.updated_at = now_iso()
            self.db.update_prompt(prompt, "Batch rescore")
            count += 1

        return count

    # ============================================================
    # 版本管理 / Version Management
    # ============================================================

    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """获取版本历史 / Get version history

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            List[PromptVersion]: 版本列表 / Version list
        """
        return self.db.get_versions(prompt_id)

    def diff_versions(
        self,
        prompt_id: str,
        version1: int,
        version2: int,
    ) -> str:
        """对比两个版本 / Compare two versions

        Args:
            prompt_id: Prompt ID / Prompt ID
            version1: 版本号1 / Version number 1
            version2: 版本号2 / Version number 2

        Returns:
            str: 差异文本 / Diff text
        """
        versions = self.db.get_versions(prompt_id)

        v1_content = ""
        v2_content = ""

        for v in versions:
            if v.version == version1:
                v1_content = v.content
            if v.version == version2:
                v2_content = v.content

        if not v1_content:
            # 如果版本1不在历史中，尝试用当前版本 / If v1 not in history, try current
            prompt = self.get_prompt(prompt_id)
            if prompt and prompt.version == version1:
                v1_content = prompt.content

        return simple_diff(v1_content, v2_content)

    # ============================================================
    # 标签管理 / Tag Management
    # ============================================================

    def get_all_tags(self) -> List[Tag]:
        """获取所有标签 / Get all tags

        Returns:
            List[Tag]: 标签列表 / Tag list
        """
        return self.db.get_all_tags()

    def get_categories(self) -> List[str]:
        """获取所有分类 / Get all categories

        Returns:
            List[str]: 分类列表 / Category list
        """
        stats = self.db.get_stats()
        return list(stats.get("categories", {}).keys())

    # ============================================================
    # 导出 / Export
    # ============================================================

    def export_prompt(
        self,
        prompt_id: str,
        format_type: str = "json",
        include_versions: bool = False,
        file_path: Optional[str] = None,
    ) -> str:
        """导出prompt / Export prompt

        Args:
            prompt_id: Prompt ID / Prompt ID
            format_type: 导出格式 / Export format
            include_versions: 是否包含版本 / Include versions
            file_path: 文件路径（可选）/ File path (optional)

        Returns:
            str: 导出内容或文件路径 / Export content or file path
        """
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_id}")

        versions = None
        if include_versions:
            versions = self.db.get_versions(prompt_id)

        if file_path:
            return self.exporter.export_to_file(
                prompt, file_path, format_type, include_versions, versions
            )

        return self.exporter.export_prompt(prompt, format_type, include_versions, versions)

    def export_all(
        self,
        format_type: str = "json",
        directory: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> str:
        """批量导出所有prompts / Batch export all prompts

        Args:
            format_type: 导出格式 / Export format
            directory: 目标目录 / Target directory
            category: 按分类过滤 / Filter by category
            tag: 按标签过滤 / Filter by tag

        Returns:
            str: 导出内容或目录路径 / Export content or directory path
        """
        prompts = self.db.list_prompts(
            category=category,
            tag=tag,
            limit=10000,
        )

        if directory:
            exported = self.exporter.export_all_to_directory(prompts, directory, format_type)
            return f"Exported {len(exported)} prompts to: {directory}"

        return self.exporter.export_prompts(prompts, format_type)

    # ============================================================
    # 使用日志 / Usage Logging
    # ============================================================

    def log_usage(self, prompt_id: str) -> None:
        """记录使用 / Log usage

        Args:
            prompt_id: Prompt ID / Prompt ID
        """
        self.db.log_usage(prompt_id)

    # ============================================================
    # 统计信息 / Statistics
    # ============================================================

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息 / Get statistics

        Returns:
            Dict[str, Any]: 统计信息 / Statistics
        """
        return self.db.get_stats()

    def display_stats(self) -> str:
        """生成统计信息展示文本 / Generate statistics display text

        Returns:
            str: 格式化的统计信息 / Formatted statistics
        """
        stats = self.get_stats()

        lines = [
            colored("=" * 55, Color.CYAN),
            colored("  PromptForge 统计信息 / Statistics", Color.CYAN + Color.BOLD),
            colored("=" * 55, Color.CYAN),
            "",
            f"  Prompt总数 / Total:       {colored(str(stats['total_prompts']), Color.BRIGHT_GREEN)}",
            f"  平均评分 / Avg Score:     {colored(str(stats['avg_score']), Color.BRIGHT_YELLOW)}/100",
            f"  标签总数 / Tags:          {colored(str(stats['total_tags']), Color.BRIGHT_CYAN)}",
            f"  总使用次数 / Usage:       {colored(str(stats['total_usage']), Color.BRIGHT_MAGENTA)}",
            "",
        ]

        # 分类统计 / Category statistics
        if stats["categories"]:
            lines.append(colored("  分类分布 / Categories:", Color.BOLD))
            for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
                bar_len = min(count * 2, 20)
                bar = colored("█" * bar_len, Color.BLUE)
                lines.append(f"    {cat:<15} {bar} {count}")
            lines.append("")

        # 评分分布 / Score distribution
        if stats["score_distribution"]:
            lines.append(colored("  评分分布 / Score Distribution:", Color.BOLD))
            labels = {
                "excellent": ("优秀/Excellent", Color.BRIGHT_GREEN),
                "good": ("良好/Good", Color.BRIGHT_YELLOW),
                "average": ("一般/Average", Color.YELLOW),
                "poor": ("较差/Poor", Color.BRIGHT_RED),
            }
            for level, label_color in labels.items():
                count = stats["score_distribution"].get(level, 0)
                label, color = label_color
                bar_len = min(count * 2, 20)
                bar = colored("█" * bar_len, color)
                lines.append(f"    {label:<20} {bar} {count}")
            lines.append("")

        # 最近添加 / Recently added
        if stats["recent_prompts"]:
            lines.append(colored("  最近添加 / Recent:", Color.BOLD))
            for rp in stats["recent_prompts"][:5]:
                lines.append(f"    - {truncate(rp['title'], 40)} ({time_ago(rp['created_at'])})")

        lines.append(colored("=" * 55, Color.CYAN))
        return "\n".join(lines)

    # ============================================================
    # 显示 / Display
    # ============================================================

    def display_prompt(self, prompt_id: str) -> str:
        """生成prompt详情展示文本 / Generate prompt detail display text

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            str: 格式化的prompt详情 / Formatted prompt detail
        """
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            return colored(f"Prompt not found: {prompt_id}", Color.RED)

        lines = [
            colored("=" * 60, Color.CYAN),
            colored(f"  {prompt.title}", Color.BOLD),
            colored("=" * 60, Color.CYAN),
            "",
            f"  ID:        {colored(prompt.id, Color.GRAY)}",
            f"  Category:  {colored(prompt.category, Color.BLUE)}",
            f"  Score:     {colored(f'{prompt.score:.1f}/100', Color.BRIGHT_YELLOW)}",
            f"  Version:   {prompt.version}",
            f"  Usage:     {prompt.usage_count}",
            f"  Created:   {format_datetime(prompt.created_at)} ({time_ago(prompt.created_at)})",
            f"  Updated:   {format_datetime(prompt.updated_at)} ({time_ago(prompt.updated_at)})",
        ]

        if prompt.tags:
            tag_str = " ".join(colored(f"[{t}]", Color.BRIGHT_CYAN) for t in prompt.tags)
            lines.append(f"  Tags:      {tag_str}")

        lines.extend([
            "",
            colored("-" * 60, Color.GRAY),
            "",
        ])

        # 内容 / Content
        for line in prompt.content.split("\n"):
            lines.append(f"  {line}")

        lines.extend([
            "",
            colored("=" * 60, Color.CYAN),
        ])

        return "\n".join(lines)

    def display_prompt_list(
        self,
        prompts: List[Prompt],
        show_index: bool = True,
    ) -> str:
        """生成prompt列表展示文本 / Generate prompt list display text

        Args:
            prompts: Prompt列表 / Prompt list
            show_index: 是否显示序号 / Show index

        Returns:
            str: 格式化的列表 / Formatted list
        """
        if not prompts:
            return colored("  没有找到Prompt / No prompts found", Color.YELLOW)

        rows: List[List[str]] = []
        for i, p in enumerate(prompts, 1):
            idx = str(i) if show_index else ""
            tags_str = ", ".join(p.tags[:3]) + ("..." if len(p.tags) > 3 else "")
            updated = time_ago(p.updated_at)
            rows.append([
                idx,
                truncate(p.title, 25),
                p.category,
                truncate(tags_str, 20),
                f"{p.score:.0f}",
                updated,
            ])

        headers = ["#", "Title", "Cat", "Tags", "Score", "Updated"]
        return format_table(headers, rows, max_col_width=30)

    # ============================================================
    # 内部方法 / Internal Methods
    # ============================================================

    def _rebuild_search_index(self) -> None:
        """重建搜索索引 / Rebuild search index"""
        prompts = self.db.get_all_prompts_for_search()
        self.searcher.build_index(prompts)


def format_table(headers: List[str], rows: List[List[str]], max_col_width: int = 30) -> str:
    """格式化表格（从utils导入的快捷方式）/ Format table (shortcut from utils)

    Args:
        headers: 表头 / Headers
        rows: 数据行 / Data rows
        max_col_width: 列最大宽度 / Column max width

    Returns:
        str: 格式化表格 / Formatted table
    """
    from .utils import format_table as _format_table
    return _format_table(headers, rows, max_col_width=max_col_width)
