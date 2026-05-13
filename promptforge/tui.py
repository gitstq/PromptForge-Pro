"""
PromptForge - TUI交互式仪表盘 / TUI Interactive Dashboard
============================================================

使用纯文本菜单实现的交互式终端界面，不依赖curses。
Interactive terminal interface using plain text menus, no curses dependency.

Author: PromptForge Team
Version: 1.0.0
"""

import sys
from typing import Optional, List

from .engine import PromptManager
from .utils import (
    colored, Color, safe_input, safe_int_input,
    truncate, remove_ansi,
)


class TUI:
    """TUI交互式仪表盘 / TUI Interactive Dashboard

    提供基于文本菜单的交互式Prompt管理界面。
    Provide text menu based interactive prompt management interface.

    Attributes:
        manager: Prompt管理器 / Prompt manager
        running: 是否运行中 / Whether running
    """

    # 菜单宽度 / Menu width
    MENU_WIDTH = 55

    def __init__(self, manager: PromptManager):
        """初始化TUI / Initialize TUI

        Args:
            manager: Prompt管理器 / Prompt manager
        """
        self.manager = manager
        self.running = True

    def run(self) -> None:
        """启动TUI主循环 / Start TUI main loop"""
        self._clear_screen()
        self._show_banner()

        while self.running:
            self._show_main_menu()
            choice = safe_input(
                colored("  请选择 / Select: ", Color.BRIGHT_CYAN),
                default="0"
            )
            self._handle_main_choice(choice.strip())

    def stop(self) -> None:
        """停止TUI / Stop TUI"""
        self.running = False

    # ============================================================
    # 主菜单 / Main Menu
    # ============================================================

    def _show_banner(self) -> None:
        """显示欢迎横幅 / Show welcome banner"""
        banner = f"""
{colored('╔' + '═' * 53 + '╗', Color.CYAN)}
{colored('║', Color.CYAN)}{colored('  ____                 _                      ', Color.BRIGHT_CYAN + Color.BOLD)}{colored('║', Color.CYAN)}
{colored('║', Color.CYAN)}{colored(' |  _ \\ _ __ _____  _| |__   _____  __      ', Color.BRIGHT_CYAN + Color.BOLD)}{colored('║', Color.CYAN)}
{colored('║', Color.CYAN)}{colored(' | |_) | \'__/ _ \\ \\/ / \'_ \\ \\ / / _ \\/ /      ', Color.BRIGHT_CYAN + Color.BOLD)}{colored('║', Color.CYAN)}
{colored('║', Color.CYAN)}{colored(' |  __/| | | (_) >  <| |_) \\ V /  __/ /       ', Color.BRIGHT_CYAN + Color.BOLD)}{colored('║', Color.CYAN)}
{colored('║', Color.CYAN)}{colored(' |_|   |_|  \\___/_/\\_\\_.__/ \\_/ \\___/_/        ', Color.BRIGHT_CYAN + Color.BOLD)}{colored('║', Color.CYAN)}
{colored('╚' + '═' * 53 + '╝', Color.CYAN)}
{colored('  Prompt智能管理与优化引擎 v1.0.0', Color.GRAY)}
{colored('  Lightweight AI Prompt Manager & Optimizer', Color.GRAY)}
"""
        print(banner)

    def _show_main_menu(self) -> None:
        """显示主菜单 / Show main menu"""
        print()
        print(colored("  ┌─ 主菜单 / Main Menu ──────────────────────────┐", Color.CYAN))
        print(colored("  │", Color.CYAN) + "                                              " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('1', Color.BRIGHT_GREEN)}. 列出Prompts / List Prompts                " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('2', Color.BRIGHT_GREEN)}. 搜索 / Search                             " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('3', Color.BRIGHT_GREEN)}. 添加Prompt / Add Prompt                   " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('4', Color.BRIGHT_GREEN)}. 查看详情 / View Details                   " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('5', Color.BRIGHT_GREEN)}. 评分 / Score Prompt                       " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('6', Color.BRIGHT_GREEN)}. 导出 / Export                             " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('7', Color.BRIGHT_GREEN)}. 标签管理 / Tags                           " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('8', Color.BRIGHT_GREEN)}. 统计信息 / Statistics                     " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + "                                              " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + f"  {colored('0', Color.BRIGHT_RED)}. 退出 / Exit                                " + colored("│", Color.CYAN))
        print(colored("  │", Color.CYAN) + "                                              " + colored("│", Color.CYAN))
        print(colored("  └──────────────────────────────────────────────┘", Color.CYAN))
        print()

    def _handle_main_choice(self, choice: str) -> None:
        """处理主菜单选择 / Handle main menu choice

        Args:
            choice: 用户选择 / User choice
        """
        handlers = {
            "1": self._action_list,
            "2": self._action_search,
            "3": self._action_add,
            "4": self._action_view,
            "5": self._action_score,
            "6": self._action_export,
            "7": self._action_tags,
            "8": self._action_stats,
            "0": self._action_exit,
            "q": self._action_exit,
            "Q": self._action_exit,
        }

        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print(colored("  无效选择，请重试 / Invalid choice, try again", Color.RED))

    # ============================================================
    # 列表操作 / List Action
    # ============================================================

    def _action_list(self) -> None:
        """列出prompts / List prompts"""
        print(colored("\n  ── Prompt列表 / Prompt List ──", Color.CYAN))

        # 获取过滤选项 / Get filter options
        category = safe_input("  分类过滤 (留空跳过) / Category filter (empty to skip): ")
        tag = safe_input("  标签过滤 (留空跳过) / Tag filter (empty to skip): ")
        limit = safe_int_input("  显示数量 (默认20) / Limit (default 20): ", default=20, min_val=1, max_val=100)

        prompts = self.manager.list_prompts(
            category=category if category else None,
            tag=tag if tag else None,
            limit=limit,
        )

        if not prompts:
            print(colored("  没有找到Prompt / No prompts found", Color.YELLOW))
            return

        print()
        print(self.manager.display_prompt_list(prompts))
        print(f"\n  共 {len(prompts)} 个Prompt / {len(prompts)} prompts total")

        # 是否查看详情 / View details?
        choice = safe_input(
            colored("\n  查看详情? 输入序号 (留空返回) / View? Enter # (empty to back): ", Color.YELLOW)
        )
        if choice.strip().isdigit():
            idx = int(choice.strip()) - 1
            if 0 <= idx < len(prompts):
                self._show_prompt_detail(prompts[idx].id)

    # ============================================================
    # 搜索操作 / Search Action
    # ============================================================

    def _action_search(self) -> None:
        """搜索prompts / Search prompts"""
        query = safe_input(colored("\n  输入搜索关键词 / Enter search query: ", Color.BRIGHT_CYAN))
        if not query:
            print(colored("  搜索词不能为空 / Query cannot be empty", Color.RED))
            return

        results = self.manager.search(query, limit=10)

        if not results:
            print(colored(f"  没有找到匹配 '{query}' 的结果 / No results for '{query}'", Color.YELLOW))
            return

        print(colored(f"\n  搜索结果 / Search Results ({len(results)}):", Color.CYAN))
        print()

        for i, result in enumerate(results, 1):
            if result.prompt:
                p = result.prompt
                print(f"  {colored(f'{i}.', Color.BRIGHT_GREEN)} {colored(truncate(p.title, 40), Color.BOLD)}")
                print(f"     ID: {p.id[:16]}... | Score: {p.score:.0f} | Match: {result.score:.2f}")
                if result.highlights:
                    for h in result.highlights[:2]:
                        print(f"     {colored(truncate(h, 60), Color.GRAY)}")
                print()

        # 查看详情 / View details
        choice = safe_input(
            colored("  查看详情? 输入序号 (留空返回) / View? Enter # (empty to back): ", Color.YELLOW)
        )
        if choice.strip().isdigit():
            idx = int(choice.strip()) - 1
            if 0 <= idx < len(results) and results[idx].prompt:
                self._show_prompt_detail(results[idx].prompt.id)

    # ============================================================
    # 添加操作 / Add Action
    # ============================================================

    def _action_add(self) -> None:
        """添加新prompt / Add new prompt"""
        print(colored("\n  ── 添加新Prompt / Add New Prompt ──", Color.CYAN))
        print(colored("  (输入空行结束内容编辑 / Empty line to finish)", Color.GRAY))
        print()

        title = safe_input(colored("  标题 / Title: ", Color.BRIGHT_CYAN))
        if not title:
            print(colored("  标题不能为空 / Title cannot be empty", Color.RED))
            return

        category = safe_input("  分类 / Category (默认general): ", default="general")

        tags_str = safe_input("  标签 / Tags (逗号分隔, e.g., coding,ai): ")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

        print()
        print(colored("  输入Prompt内容 (输入单独的 END 结束):", Color.BRIGHT_YELLOW))
        print(colored("  Enter prompt content (type END on a new line to finish):", Color.GRAY))
        print()

        content_lines: List[str] = []
        while True:
            try:
                line = input("  > ")
                if line.strip() == "END":
                    break
                content_lines.append(line)
            except (EOFError, KeyboardInterrupt):
                print()
                break

        content = "\n".join(content_lines).strip()
        if not content:
            print(colored("  内容不能为空 / Content cannot be empty", Color.RED))
            return

        try:
            prompt = self.manager.add_prompt(
                title=title,
                content=content,
                category=category,
                tags=tags,
            )
            print()
            print(colored(f"  Prompt添加成功! / Prompt added successfully!", Color.BRIGHT_GREEN))
            print(f"  ID: {prompt.id}")
            print(f"  Score: {prompt.score:.1f}/100")
        except ValueError as e:
            print(colored(f"  添加失败: {e}", Color.RED))

    # ============================================================
    # 查看详情 / View Details
    # ============================================================

    def _action_view(self) -> None:
        """查看prompt详情 / View prompt details"""
        prompt_id = safe_input(colored("\n  输入Prompt ID (支持短ID): ", Color.BRIGHT_CYAN))
        if not prompt_id:
            return

        self._show_prompt_detail(prompt_id)

    def _show_prompt_detail(self, prompt_id: str) -> None:
        """显示prompt详情 / Show prompt detail

        Args:
            prompt_id: Prompt ID / Prompt ID
        """
        print()
        print(self.manager.display_prompt(prompt_id))

        # 子菜单 / Sub menu
        prompt = self.manager.get_prompt(prompt_id)
        if not prompt:
            return

        print(colored("  操作 / Actions:", Color.BOLD))
        print(f"    {colored('c', Color.BRIGHT_GREEN)}. 复制内容 / Copy content")
        print(f"    {colored('e', Color.BRIGHT_GREEN)}. 编辑 / Edit")
        print(f"    {colored('d', Color.BRIGHT_GREEN)}. 删除 / Delete")
        print(f"    {colored('v', Color.BRIGHT_GREEN)}. 版本历史 / Version history")
        print(f"    {colored('s', Color.BRIGHT_GREEN)}. 评分 / Score")
        print(f"    {colored('b', Color.BRIGHT_RED)}. 返回 / Back")

        choice = safe_input(colored("  选择 / Select: ", Color.YELLOW), default="b")

        if choice == "c":
            self._copy_to_clipboard(prompt.content)
        elif choice == "e":
            self._edit_prompt_inline(prompt)
        elif choice == "d":
            self._delete_prompt_confirm(prompt.id)
        elif choice == "v":
            self._show_versions(prompt.id)
        elif choice == "s":
            self._show_score(prompt.id)

    def _copy_to_clipboard(self, text: str) -> None:
        """复制到剪贴板 / Copy to clipboard

        Args:
            text: 要复制的文本 / Text to copy
        """
        try:
            # 尝试使用xclip（Linux）/ Try xclip (Linux)
            import subprocess
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"],
                stdin=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            process.communicate(text.encode("utf-8"))
            print(colored("  已复制到剪贴板 / Copied to clipboard", Color.BRIGHT_GREEN))
        except (FileNotFoundError, OSError):
            # 回退：直接输出 / Fallback: direct output
            print(colored("\n  内容如下（请手动复制）/ Content below (copy manually):", Color.YELLOW))
            print(colored("  " + "-" * 50, Color.GRAY))
            for line in text.split("\n"):
                print(f"  {line}")
            print(colored("  " + "-" * 50, Color.GRAY))

    def _edit_prompt_inline(self, prompt) -> None:
        """内联编辑prompt / Inline edit prompt

        Args:
            prompt: Prompt对象 / Prompt object
        """
        print(colored(f"\n  编辑Prompt: {prompt.title}", Color.CYAN))
        print(colored("  (留空保持原值 / Empty to keep original)", Color.GRAY))
        print()

        new_title = safe_input(f"  标题 / Title [{prompt.title}]: ", default=prompt.title)
        new_category = safe_input(f"  分类 / Category [{prompt.category}]: ", default=prompt.category)

        tags_str = safe_input(
            f"  标签 / Tags [{', '.join(prompt.tags)}]: ",
            default=", ".join(prompt.tags)
        )
        new_tags = [t.strip() for t in tags_str.split(",") if t.strip()]

        print(colored("  输入新内容 (留空保持原值, 输入END结束):", Color.BRIGHT_YELLOW))
        content_lines: List[str] = []
        while True:
            try:
                line = input("  > ")
                if line.strip() == "END":
                    break
                content_lines.append(line)
            except (EOFError, KeyboardInterrupt):
                print()
                break

        new_content = "\n".join(content_lines).strip() if content_lines else None

        try:
            updated = self.manager.edit_prompt(
                prompt_id=prompt.id,
                title=new_title if new_title != prompt.title else None,
                content=new_content,
                category=new_category if new_category != prompt.category else None,
                tags=new_tags if new_tags != prompt.tags else None,
                change_note="TUI edit",
            )
            print(colored(f"\n  Prompt更新成功! Version: {updated.version}", Color.BRIGHT_GREEN))
        except ValueError as e:
            print(colored(f"  更新失败: {e}", Color.RED))

    def _delete_prompt_confirm(self, prompt_id: str) -> None:
        """确认删除prompt / Confirm delete prompt

        Args:
            prompt_id: Prompt ID / Prompt ID
        """
        confirm = safe_input(
            colored(f"  确认删除? (y/N) / Confirm delete? (y/N): ", Color.BRIGHT_RED),
            default="n"
        )
        if confirm.lower() == "y":
            if self.manager.delete_prompt(prompt_id):
                print(colored("  Prompt已删除 / Prompt deleted", Color.BRIGHT_GREEN))
            else:
                print(colored("  删除失败 / Delete failed", Color.RED))

    def _show_versions(self, prompt_id: str) -> None:
        """显示版本历史 / Show version history

        Args:
            prompt_id: Prompt ID / Prompt ID
        """
        versions = self.manager.get_versions(prompt_id)
        if not versions:
            print(colored("  没有版本历史 / No version history", Color.YELLOW))
            return

        print(colored(f"\n  版本历史 / Version History ({len(versions)}):", Color.CYAN))
        for v in versions:
            note = f" - {v.change_note}" if v.change_note else ""
            print(f"    v{v.version} | {v.created_at[:19]}{note}")
            print(f"    {truncate(v.content, 60)}")
            print()

    def _show_score(self, prompt_id: str) -> None:
        """显示评分结果 / Show score result

        Args:
            prompt_id: Prompt ID / Prompt ID
        """
        result = self.manager.score_prompt(prompt_id)
        if result:
            print()
            print(result.to_display())
        else:
            print(colored("  Prompt not found", Color.RED))

    # ============================================================
    # 评分操作 / Score Action
    # ============================================================

    def _action_score(self) -> None:
        """评分prompt / Score prompt"""
        prompt_id = safe_input(colored("\n  输入Prompt ID: ", Color.BRIGHT_CYAN))
        if not prompt_id:
            return

        self._show_score(prompt_id)

    # ============================================================
    # 导出操作 / Export Action
    # ============================================================

    def _action_export(self) -> None:
        """导出prompt / Export prompt"""
        print(colored("\n  ── 导出 / Export ──", Color.CYAN))
        print(f"    {colored('1', Color.BRIGHT_GREEN)}. 导出单个 / Export single")
        print(f"    {colored('2', Color.BRIGHT_GREEN)}. 批量导出 / Batch export")

        choice = safe_input(colored("  选择 / Select: ", Color.YELLOW), default="1")

        if choice == "1":
            prompt_id = safe_input("  Prompt ID: ")
            if not prompt_id:
                return

            print("  格式 / Format: json, yaml, md")
            fmt = safe_input("  选择格式 / Select format: ", default="md")

            try:
                content = self.manager.export_prompt(prompt_id, fmt, include_versions=True)
                print()
                print(colored("  导出结果 / Export Result:", Color.CYAN))
                print(colored("  " + "-" * 50, Color.GRAY))
                print(content)
                print(colored("  " + "-" * 50, Color.GRAY))
            except ValueError as e:
                print(colored(f"  导出失败: {e}", Color.RED))

        elif choice == "2":
            directory = safe_input("  导出目录 / Export directory (默认./exports): ", default="./exports")
            fmt = safe_input("  格式 / Format: ", default="md")

            try:
                result = self.manager.export_all(format_type=fmt, directory=directory)
                print(colored(f"\n  {result}", Color.BRIGHT_GREEN))
            except Exception as e:
                print(colored(f"  导出失败: {e}", Color.RED))

    # ============================================================
    # 标签管理 / Tag Management
    # ============================================================

    def _action_tags(self) -> None:
        """标签管理 / Tag management"""
        tags = self.manager.get_all_tags()

        if not tags:
            print(colored("\n  没有标签 / No tags found", Color.YELLOW))
            return

        print(colored(f"\n  标签列表 / Tags ({len(tags)}):", Color.CYAN))
        print()

        # 表格显示 / Table display
        for i, tag in enumerate(tags, 1):
            bar_len = min(tag.count * 2, 20)
            bar = colored("█" * bar_len, Color.BLUE)
            print(f"  {colored(f'{i:>3}.', Color.GRAY)} {colored(tag.name, Color.BRIGHT_CYAN):<20} {bar} {tag.count}")

        print(f"\n  共 {len(tags)} 个标签 / {len(tags)} tags total")

    # ============================================================
    # 统计信息 / Statistics
    # ============================================================

    def _action_stats(self) -> None:
        """显示统计信息 / Show statistics"""
        print()
        print(self.manager.display_stats())

    # ============================================================
    # 退出 / Exit
    # ============================================================

    def _action_exit(self) -> None:
        """退出TUI / Exit TUI"""
        print()
        print(colored("  感谢使用 PromptForge! / Thank you for using PromptForge!", Color.BRIGHT_CYAN))
        print()
        self.running = False

    # ============================================================
    # 辅助方法 / Helper Methods
    # ============================================================

    @staticmethod
    def _clear_screen() -> None:
        """清屏 / Clear screen"""
        # ANSI escape code for clearing screen
        print("\033[2J\033[H", end="")
