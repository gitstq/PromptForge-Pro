"""
PromptForge - 多格式导出器 / Multi-format Exporter
====================================================

支持将Prompt导出为JSON、YAML、Markdown等多种格式。
Support exporting prompts to JSON, YAML, Markdown and other formats.

Author: PromptForge Team
Version: 1.0.0
"""

import json
import os
import re
from datetime import datetime
from typing import List, Optional, Dict, Any

from .models import Prompt, PromptVersion


class Exporter:
    """多格式导出器 / Multi-format exporter

    将Prompt数据导出为不同格式的文件。
    Export prompt data to files in different formats.
    """

    # 支持的导出格式 / Supported export formats
    SUPPORTED_FORMATS = {"json", "yaml", "md", "markdown", "txt"}

    def export_prompt(
        self,
        prompt: Prompt,
        format_type: str = "json",
        include_versions: bool = False,
        versions: Optional[List[PromptVersion]] = None,
    ) -> str:
        """导出单个prompt / Export a single prompt

        Args:
            prompt: Prompt对象 / Prompt object
            format_type: 导出格式（json/yaml/md）/ Export format
            include_versions: 是否包含版本历史 / Include version history
            versions: 版本列表 / Version list

        Returns:
            str: 导出的文本内容 / Exported text content

        Raises:
            ValueError: 不支持的格式 / Unsupported format
        """
        format_type = format_type.lower()

        if format_type in ("md", "markdown"):
            return self._export_markdown(prompt, include_versions, versions)
        elif format_type == "yaml":
            return self._export_yaml(prompt, include_versions, versions)
        elif format_type == "json":
            return self._export_json(prompt, include_versions, versions)
        elif format_type == "txt":
            return self._export_txt(prompt, include_versions, versions)
        else:
            raise ValueError(
                f"不支持的导出格式: {format_type} "
                f"(Unsupported format: {format_type}). "
                f"支持: {', '.join(sorted(self.SUPPORTED_FORMATS))}"
            )

    def export_prompts(
        self,
        prompts: List[Prompt],
        format_type: str = "json",
    ) -> str:
        """批量导出prompts / Batch export prompts

        Args:
            prompts: Prompt列表 / Prompt list
            format_type: 导出格式 / Export format

        Returns:
            str: 导出的文本内容 / Exported text content
        """
        format_type = format_type.lower()

        if format_type in ("md", "markdown"):
            return self._export_batch_markdown(prompts)
        elif format_type == "yaml":
            return self._export_batch_yaml(prompts)
        elif format_type == "json":
            return self._export_batch_json(prompts)
        elif format_type == "txt":
            return self._export_batch_txt(prompts)
        else:
            raise ValueError(f"不支持的导出格式: {format_type}")

    def export_to_file(
        self,
        prompt: Prompt,
        file_path: str,
        format_type: Optional[str] = None,
        include_versions: bool = False,
        versions: Optional[List[PromptVersion]] = None,
    ) -> str:
        """导出prompt到文件 / Export prompt to file

        Args:
            prompt: Prompt对象 / Prompt object
            file_path: 文件路径 / File path
            format_type: 导出格式（自动从扩展名推断）/ Export format
            include_versions: 是否包含版本历史 / Include version history
            versions: 版本列表 / Version list

        Returns:
            str: 导出文件的完整路径 / Full path of exported file
        """
        # 从文件扩展名推断格式 / Infer format from file extension
        if format_type is None:
            ext = os.path.splitext(file_path)[1].lower().lstrip(".")
            format_type = ext if ext in self.SUPPORTED_FORMATS else "json"

        content = self.export_prompt(prompt, format_type, include_versions, versions)

        # 确保目录存在 / Ensure directory exists
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return os.path.abspath(file_path)

    def export_all_to_directory(
        self,
        prompts: List[Prompt],
        directory: str,
        format_type: str = "md",
    ) -> List[str]:
        """批量导出所有prompts到目录 / Batch export all prompts to directory

        Args:
            prompts: Prompt列表 / Prompt list
            directory: 目标目录 / Target directory
            format_type: 导出格式 / Export format

        Returns:
            List[str]: 导出文件路径列表 / List of exported file paths
        """
        os.makedirs(directory, exist_ok=True)
        exported_files: List[str] = []

        for prompt in prompts:
            # 生成安全的文件名 / Generate safe filename
            safe_title = self._safe_filename(prompt.title)
            ext = self._format_extension(format_type)
            file_path = os.path.join(directory, f"{safe_title}_{prompt.id[:8]}{ext}")

            content = self.export_prompt(prompt, format_type)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            exported_files.append(os.path.abspath(file_path))

        return exported_files

    # ============================================================
    # JSON 导出 / JSON Export
    # ============================================================

    def _export_json(
        self,
        prompt: Prompt,
        include_versions: bool = False,
        versions: Optional[List[PromptVersion]] = None,
    ) -> str:
        """导出为JSON格式 / Export as JSON format

        Args:
            prompt: Prompt对象 / Prompt object
            include_versions: 是否包含版本 / Include versions
            versions: 版本列表 / Version list

        Returns:
            str: JSON字符串 / JSON string
        """
        data = prompt.to_dict()

        if include_versions and versions:
            data["versions"] = [v.to_dict() for v in versions]

        return json.dumps(data, ensure_ascii=False, indent=2)

    def _export_batch_json(self, prompts: List[Prompt]) -> str:
        """批量导出为JSON格式 / Batch export as JSON format

        Args:
            prompts: Prompt列表 / Prompt list

        Returns:
            str: JSON字符串 / JSON string
        """
        data = {
            "exported_at": datetime.now().isoformat(),
            "total_count": len(prompts),
            "prompts": [p.to_dict() for p in prompts],
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    # ============================================================
    # YAML 导出 / YAML Export
    # ============================================================

    def _export_yaml(
        self,
        prompt: Prompt,
        include_versions: bool = False,
        versions: Optional[List[PromptVersion]] = None,
    ) -> str:
        """导出为YAML格式（纯Python实现）/ Export as YAML format (pure Python)

        不依赖PyYAML，使用简单的文本格式化。
        No PyYAML dependency, use simple text formatting.

        Args:
            prompt: Prompt对象 / Prompt object
            include_versions: 是否包含版本 / Include versions
            versions: 版本列表 / Version list

        Returns:
            str: YAML格式字符串 / YAML format string
        """
        lines = [
            f"# Prompt: {prompt.title}",
            f"# Exported by PromptForge",
            f"# ID: {prompt.id}",
            "",
            f"id: \"{prompt.id}\"",
            f"title: \"{self._escape_yaml(prompt.title)}\"",
            f"category: \"{prompt.category}\"",
            f"score: {prompt.score}",
            f"version: {prompt.version}",
            f"usage_count: {prompt.usage_count}",
            f"created_at: \"{prompt.created_at}\"",
            f"updated_at: \"{prompt.updated_at}\"",
        ]

        # 标签 / Tags
        if prompt.tags:
            lines.append("tags:")
            for tag in prompt.tags:
                lines.append(f"  - \"{tag}\"")
        else:
            lines.append("tags: []")

        # 内容（多行）/ Content (multiline)
        lines.append("content: |")
        for content_line in prompt.content.split("\n"):
            lines.append(f"  {content_line}")

        # 版本历史 / Version history
        if include_versions and versions:
            lines.append("")
            lines.append("versions:")
            for v in versions:
                lines.append(f"  - version: {v.version}")
                lines.append(f"    created_at: \"{v.created_at}\"")
                if v.change_note:
                    lines.append(f"    change_note: \"{self._escape_yaml(v.change_note)}\"")
                lines.append("    content: |")
                for content_line in v.content.split("\n"):
                    lines.append(f"      {content_line}")

        return "\n".join(lines) + "\n"

    def _export_batch_yaml(self, prompts: List[Prompt]) -> str:
        """批量导出为YAML格式 / Batch export as YAML format

        Args:
            prompts: Prompt列表 / Prompt list

        Returns:
            str: YAML格式字符串 / YAML format string
        """
        lines = [
            f"# PromptForge Export",
            f"# Exported at: {datetime.now().isoformat()}",
            f"# Total: {len(prompts)} prompts",
            "",
            "prompts:",
        ]

        for prompt in prompts:
            lines.append(f"  - id: \"{prompt.id}\"")
            lines.append(f"    title: \"{self._escape_yaml(prompt.title)}\"")
            lines.append(f"    category: \"{prompt.category}\"")
            lines.append(f"    score: {prompt.score}")
            if prompt.tags:
                lines.append("    tags:")
                for tag in prompt.tags:
                    lines.append(f"      - \"{tag}\"")
            lines.append("    content: |")
            for content_line in prompt.content.split("\n"):
                lines.append(f"      {content_line}")
            lines.append("")

        return "\n".join(lines)

    # ============================================================
    # Markdown 导出 / Markdown Export
    # ============================================================

    def _export_markdown(
        self,
        prompt: Prompt,
        include_versions: bool = False,
        versions: Optional[List[PromptVersion]] = None,
    ) -> str:
        """导出为Markdown格式 / Export as Markdown format

        Args:
            prompt: Prompt对象 / Prompt object
            include_versions: 是否包含版本 / Include versions
            versions: 版本列表 / Version list

        Returns:
            str: Markdown格式字符串 / Markdown format string
        """
        lines = [
            f"# {prompt.title}",
            "",
            f"> **ID**: `{prompt.id}`",
            f"> **Category**: {prompt.category}",
            f"> **Score**: {prompt.score}/100",
            f"> **Version**: {prompt.version}",
            f"> **Created**: {prompt.created_at}",
            f"> **Updated**: {prompt.updated_at}",
        ]

        # 标签 / Tags
        if prompt.tags:
            tag_str = " ".join(f"`{tag}`" for tag in prompt.tags)
            lines.append(f"> **Tags**: {tag_str}")

        lines.extend([
            "",
            "---",
            "",
            "## Content",
            "",
        ])

        # 内容 / Content
        lines.append(prompt.content)

        # 版本历史 / Version history
        if include_versions and versions:
            lines.extend([
                "",
                "---",
                "",
                "## Version History",
                "",
            ])
            for v in versions:
                lines.append(f"### Version {v.version}")
                lines.append(f"- **Date**: {v.created_at}")
                if v.change_note:
                    lines.append(f"- **Note**: {v.change_note}")
                lines.extend([
                    "",
                    "```",
                    v.content,
                    "```",
                    "",
                ])

        lines.extend([
            "",
            "---",
            f"*Exported by PromptForge*",
        ])

        return "\n".join(lines)

    def _export_batch_markdown(self, prompts: List[Prompt]) -> str:
        """批量导出为Markdown格式 / Batch export as Markdown format

        Args:
            prompts: Prompt列表 / Prompt list

        Returns:
            str: Markdown格式字符串 / Markdown format string
        """
        lines = [
            "# PromptForge Export",
            "",
            f"> Exported at: {datetime.now().isoformat()}",
            f"> Total: {len(prompts)} prompts",
            "",
            "---",
            "",
        ]

        for i, prompt in enumerate(prompts, 1):
            lines.append(f"## {i}. {prompt.title}")
            lines.append("")
            lines.append(f"- **ID**: `{prompt.id}`")
            lines.append(f"- **Category**: {prompt.category}")
            lines.append(f"- **Score**: {prompt.score}/100")

            if prompt.tags:
                tag_str = " ".join(f"`{tag}`" for tag in prompt.tags)
                lines.append(f"- **Tags**: {tag_str}")

            lines.extend([
                "",
                prompt.content,
                "",
                "---",
                "",
            ])

        return "\n".join(lines)

    # ============================================================
    # 纯文本导出 / Plain Text Export
    # ============================================================

    def _export_txt(
        self,
        prompt: Prompt,
        include_versions: bool = False,
        versions: Optional[List[PromptVersion]] = None,
    ) -> str:
        """导出为纯文本格式 / Export as plain text format

        Args:
            prompt: Prompt对象 / Prompt object
            include_versions: 是否包含版本 / Include versions
            versions: 版本列表 / Version list

        Returns:
            str: 纯文本字符串 / Plain text string
        """
        separator = "=" * 60
        lines = [
            separator,
            f"  Title: {prompt.title}",
            f"  ID: {prompt.id}",
            f"  Category: {prompt.category}",
            f"  Score: {prompt.score}/100",
            f"  Version: {prompt.version}",
            f"  Tags: {', '.join(prompt.tags) if prompt.tags else 'None'}",
            f"  Created: {prompt.created_at}",
            f"  Updated: {prompt.updated_at}",
            separator,
            "",
            prompt.content,
            "",
        ]

        if include_versions and versions:
            lines.append(separator)
            lines.append("  Version History")
            lines.append(separator)
            for v in versions:
                lines.append(f"  Version {v.version} - {v.created_at}")
                if v.change_note:
                    lines.append(f"  Note: {v.change_note}")
                lines.extend(["", v.content, ""])

        return "\n".join(lines)

    def _export_batch_txt(self, prompts: List[Prompt]) -> str:
        """批量导出为纯文本格式 / Batch export as plain text format

        Args:
            prompts: Prompt列表 / Prompt list

        Returns:
            str: 纯文本字符串 / Plain text string
        """
        lines = [
            "=" * 60,
            "  PromptForge Export",
            f"  Exported at: {datetime.now().isoformat()}",
            f"  Total: {len(prompts)} prompts",
            "=" * 60,
            "",
        ]

        for i, prompt in enumerate(prompts, 1):
            lines.extend([
                "-" * 60,
                f"  [{i}] {prompt.title}",
                f"  ID: {prompt.id} | Category: {prompt.category} | Score: {prompt.score}",
                "-" * 60,
                "",
                prompt.content,
                "",
            ])

        return "\n".join(lines)

    # ============================================================
    # 辅助方法 / Helper Methods
    # ============================================================

    @staticmethod
    def _safe_filename(title: str) -> str:
        """生成安全的文件名 / Generate safe filename

        Args:
            title: 原始标题 / Original title

        Returns:
            str: 安全文件名 / Safe filename
        """
        # 移除/替换不安全字符 / Remove/replace unsafe characters
        safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', title)
        safe = re.sub(r'_+', '_', safe).strip('_')
        # 限制长度 / Limit length
        return safe[:100] if safe else "untitled"

    @staticmethod
    def _format_extension(format_type: str) -> str:
        """获取格式对应的文件扩展名 / Get file extension for format

        Args:
            format_type: 格式类型 / Format type

        Returns:
            str: 文件扩展名 / File extension
        """
        ext_map = {
            "json": ".json",
            "yaml": ".yaml",
            "yml": ".yml",
            "md": ".md",
            "markdown": ".md",
            "txt": ".txt",
        }
        return ext_map.get(format_type.lower(), ".txt")

    @staticmethod
    def _escape_yaml(text: str) -> str:
        """转义YAML特殊字符 / Escape YAML special characters

        Args:
            text: 原始文本 / Original text

        Returns:
            str: 转义后的文本 / Escaped text
        """
        return text.replace("\\", "\\\\").replace('"', '\\"')
