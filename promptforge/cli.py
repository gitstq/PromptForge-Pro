"""
PromptForge - CLI命令行入口 / CLI Entry Point
================================================

使用argparse实现命令行参数解析，提供所有子命令。
Use argparse for command-line argument parsing,
provide all subcommands.

Author: PromptForge Team
Version: 1.0.0

Usage:
    promptforge add --title "..." --content "..." --tags "tag1,tag2"
    promptforge list [--category ...] [--tag ...] [--sort ...] [--limit ...]
    promptforge search <query>
    promptforge show <id>
    promptforge edit <id>
    promptforge delete <id>
    promptforge score <id>
    promptforge export <id> --format json/yaml/md
    promptforge export-all [--format ...] [--dir ...]
    promptforge tags
    promptforge stats
    promptforge tui
    promptforge version
"""

import argparse
import sys
import os
from typing import Optional

from .engine import PromptManager
from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器 / Create CLI argument parser

    Returns:
        argparse.ArgumentParser: 参数解析器 / Argument parser
    """
    parser = argparse.ArgumentParser(
        prog="promptforge",
        description="PromptForge - 轻量级终端AI Prompt智能管理与优化引擎\n"
                    "Lightweight Terminal AI Prompt Manager & Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  promptforge add --title "翻译助手" --content "你是一个专业翻译..." --tags "翻译,工具"
  promptforge list --category coding --sort score --limit 10
  promptforge search "Python代码"
  promptforge show abc12345
  promptforge score abc12345
  promptforge export abc12345 --format md
  promptforge stats
  promptforge tui
        """,
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"PromptForge v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令 / Subcommand")

    # ============================================================
    # add 命令 / add command
    # ============================================================
    add_parser = subparsers.add_parser(
        "add",
        help="添加新prompt / Add new prompt",
        description="添加一个新的Prompt到数据库 / Add a new prompt to database",
    )
    add_parser.add_argument("--title", "-t", required=True, help="标题 / Title")
    add_parser.add_argument("--content", "-c", required=True, help="内容 / Content")
    add_parser.add_argument(
        "--category", "-cat",
        default="general",
        help="分类 / Category (default: general)",
    )
    add_parser.add_argument(
        "--tags",
        default="",
        help="标签（逗号分隔）/ Tags (comma-separated)",
    )
    add_parser.add_argument(
        "--no-score",
        action="store_true",
        help="跳过自动评分 / Skip auto scoring",
    )

    # ============================================================
    # list 命令 / list command
    # ============================================================
    list_parser = subparsers.add_parser(
        "list",
        help="列出所有prompts / List all prompts",
        aliases=["ls"],
    )
    list_parser.add_argument("--category", "-cat", help="按分类过滤 / Filter by category")
    list_parser.add_argument("--tag", "-t", help="按标签过滤 / Filter by tag")
    list_parser.add_argument(
        "--sort", "-s",
        default="updated_at",
        choices=["updated_at", "score", "title", "created_at", "usage_count"],
        help="排序字段 / Sort field (default: updated_at)",
    )
    list_parser.add_argument(
        "--order", "-o",
        default="desc",
        choices=["asc", "desc"],
        help="排序方向 / Sort order (default: desc)",
    )
    list_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=20,
        help="显示数量 / Limit (default: 20)",
    )
    list_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="偏移量 / Offset (default: 0)",
    )

    # ============================================================
    # search 命令 / search command
    # ============================================================
    search_parser = subparsers.add_parser(
        "search",
        help="搜索prompts / Search prompts",
        aliases=["find"],
    )
    search_parser.add_argument("query", help="搜索关键词 / Search query")
    search_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="结果数量 / Result limit (default: 10)",
    )
    search_parser.add_argument(
        "--no-fuzzy",
        action="store_true",
        help="禁用模糊匹配 / Disable fuzzy matching",
    )

    # ============================================================
    # show 命令 / show command
    # ============================================================
    show_parser = subparsers.add_parser(
        "show",
        help="显示prompt详情 / Show prompt details",
        aliases=["view"],
    )
    show_parser.add_argument("id", help="Prompt ID（支持短ID）/ Prompt ID (short ID supported)")

    # ============================================================
    # edit 命令 / edit command
    # ============================================================
    edit_parser = subparsers.add_parser(
        "edit",
        help="编辑prompt / Edit prompt",
    )
    edit_parser.add_argument("id", help="Prompt ID / Prompt ID")
    edit_parser.add_argument("--title", "-t", help="新标题 / New title")
    edit_parser.add_argument("--content", "-c", help="新内容 / New content")
    edit_parser.add_argument("--category", "-cat", help="新分类 / New category")
    edit_parser.add_argument("--tags", help="新标签（逗号分隔）/ New tags (comma-separated)")
    edit_parser.add_argument("--note", "-n", default="CLI edit", help="变更说明 / Change note")
    edit_parser.add_argument(
        "--no-score",
        action="store_true",
        help="跳过自动评分 / Skip auto scoring",
    )

    # ============================================================
    # delete 命令 / delete command
    # ============================================================
    delete_parser = subparsers.add_parser(
        "delete",
        help="删除prompt / Delete prompt",
        aliases=["rm", "del"],
    )
    delete_parser.add_argument("id", help="Prompt ID / Prompt ID")
    delete_parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="跳过确认 / Skip confirmation",
    )

    # ============================================================
    # score 命令 / score command
    # ============================================================
    score_parser = subparsers.add_parser(
        "score",
        help="评分prompt / Score prompt",
    )
    score_parser.add_argument("id", help="Prompt ID / Prompt ID")

    # ============================================================
    # export 命令 / export command
    # ============================================================
    export_parser = subparsers.add_parser(
        "export",
        help="导出prompt / Export prompt",
    )
    export_parser.add_argument("id", help="Prompt ID / Prompt ID")
    export_parser.add_argument(
        "--format", "-f",
        default="json",
        choices=["json", "yaml", "md", "txt"],
        help="导出格式 / Export format (default: json)",
    )
    export_parser.add_argument(
        "--output", "-o",
        help="输出文件路径 / Output file path",
    )
    export_parser.add_argument(
        "--with-versions",
        action="store_true",
        help="包含版本历史 / Include version history",
    )

    # ============================================================
    # export-all 命令 / export-all command
    # ============================================================
    export_all_parser = subparsers.add_parser(
        "export-all",
        help="批量导出所有prompts / Batch export all prompts",
    )
    export_all_parser.add_argument(
        "--format", "-f",
        default="md",
        choices=["json", "yaml", "md", "txt"],
        help="导出格式 / Export format (default: md)",
    )
    export_all_parser.add_argument(
        "--dir", "-d",
        default="./exports",
        help="导出目录 / Export directory (default: ./exports)",
    )
    export_all_parser.add_argument("--category", "-cat", help="按分类过滤 / Filter by category")
    export_all_parser.add_argument("--tag", "-t", help="按标签过滤 / Filter by tag")

    # ============================================================
    # tags 命令 / tags command
    # ============================================================
    subparsers.add_parser(
        "tags",
        help="列出所有标签 / List all tags",
    )

    # ============================================================
    # stats 命令 / stats command
    # ============================================================
    stats_parser = subparsers.add_parser(
        "stats",
        help="显示统计信息 / Show statistics",
    )
    stats_parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出 / Output in JSON format",
    )

    # ============================================================
    # tui 命令 / tui command
    # ============================================================
    subparsers.add_parser(
        "tui",
        help="启动TUI交互式仪表盘 / Start TUI interactive dashboard",
    )

    # ============================================================
    # version 命令 / version command
    # ============================================================
    subparsers.add_parser(
        "version",
        help="显示版本信息 / Show version info",
    )

    return parser


def main(argv: Optional[list] = None) -> int:
    """CLI主入口函数 / CLI main entry function

    Args:
        argv: 命令行参数列表 / Command-line argument list

    Returns:
        int: 退出码（0=成功）/ Exit code (0=success)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # 无命令时显示帮助 / Show help when no command
    if not args.command:
        parser.print_help()
        return 0

    # 初始化管理器 / Initialize manager
    try:
        manager = PromptManager()
    except Exception as e:
        print(f"Error: Failed to initialize PromptForge: {e}", file=sys.stderr)
        return 1

    # 分发命令 / Dispatch command
    try:
        return _dispatch_command(args, manager)
    except KeyboardInterrupt:
        print("\n操作已取消 / Operation cancelled")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _dispatch_command(args: argparse.Namespace, manager: PromptManager) -> int:
    """分发命令到对应处理函数 / Dispatch command to handler

    Args:
        args: 解析后的参数 / Parsed arguments
        manager: Prompt管理器 / Prompt manager

    Returns:
        int: 退出码 / Exit code
    """
    command = args.command

    # ---- add ----
    if command == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        prompt = manager.add_prompt(
            title=args.title,
            content=args.content,
            category=args.category,
            tags=tags,
            auto_score=not args.no_score,
        )
        print(f"Prompt added successfully!")
        print(f"  ID: {prompt.id}")
        print(f"  Title: {prompt.title}")
        print(f"  Score: {prompt.score:.1f}/100")
        return 0

    # ---- list ----
    elif command in ("list", "ls"):
        prompts = manager.list_prompts(
            category=args.category,
            tag=args.tag,
            sort_by=args.sort,
            sort_order=args.order,
            limit=args.limit,
            offset=args.offset,
        )
        print(manager.display_prompt_list(prompts))
        total = manager.count_prompts(category=args.category, tag=args.tag)
        print(f"\nShowing {len(prompts)}/{total} prompts")
        return 0

    # ---- search ----
    elif command in ("search", "find"):
        results = manager.search(
            query=args.query,
            limit=args.limit,
            fuzzy=not args.no_fuzzy,
        )
        if not results:
            print(f"No results found for: {args.query}")
            return 0

        print(f"Search results for '{args.query}' ({len(results)}):")
        print()
        for i, result in enumerate(results, 1):
            if result.prompt:
                p = result.prompt
                print(f"  {i}. {p.title} (Score: {p.score:.0f}, Match: {result.score:.2f})")
                print(f"     ID: {p.id}")
                if result.highlights:
                    for h in result.highlights[:2]:
                        print(f"     > {h[:80]}")
                print()
        return 0

    # ---- show ----
    elif command in ("show", "view"):
        print(manager.display_prompt(args.id))
        return 0

    # ---- edit ----
    elif command == "edit":
        tags = None
        if args.tags:
            tags = [t.strip() for t in args.tags.split(",") if t.strip()]

        updated = manager.edit_prompt(
            prompt_id=args.id,
            title=args.title,
            content=args.content,
            category=args.category,
            tags=tags,
            change_note=args.note,
            auto_score=not args.no_score,
        )
        print(f"Prompt updated successfully!")
        print(f"  ID: {updated.id}")
        print(f"  Version: {updated.version}")
        print(f"  Score: {updated.score:.1f}/100")
        return 0

    # ---- delete ----
    elif command in ("delete", "rm", "del"):
        if not args.yes:
            confirm = input(f"Confirm delete prompt {args.id}? (y/N): ").strip().lower()
            if confirm != "y":
                print("Cancelled.")
                return 0

        if manager.delete_prompt(args.id):
            print(f"Prompt {args.id} deleted successfully.")
            return 0
        else:
            print(f"Prompt not found: {args.id}", file=sys.stderr)
            return 1

    # ---- score ----
    elif command == "score":
        result = manager.score_prompt(args.id)
        if result:
            print(result.to_display())
            return 0
        else:
            print(f"Prompt not found: {args.id}", file=sys.stderr)
            return 1

    # ---- export ----
    elif command == "export":
        output = manager.export_prompt(
            prompt_id=args.id,
            format_type=args.format,
            include_versions=args.with_versions,
            file_path=args.output,
        )
        if args.output:
            print(f"Exported to: {output}")
        else:
            print(output)
        return 0

    # ---- export-all ----
    elif command == "export-all":
        result = manager.export_all(
            format_type=args.format,
            directory=args.dir,
            category=args.category,
            tag=args.tag,
        )
        print(result)
        return 0

    # ---- tags ----
    elif command == "tags":
        tags = manager.get_all_tags()
        if not tags:
            print("No tags found.")
            return 0

        print(f"Tags ({len(tags)}):")
        for tag in tags:
            print(f"  {tag.name:<20} ({tag.count} prompts)")
        return 0

    # ---- stats ----
    elif command == "stats":
        if args.json:
            import json
            stats = manager.get_stats()
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print(manager.display_stats())
        return 0

    # ---- tui ----
    elif command == "tui":
        from .tui import TUI
        tui = TUI(manager)
        tui.run()
        return 0

    # ---- version ----
    elif command == "version":
        print(f"PromptForge v{__version__}")
        return 0

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 1


# 入口点 / Entry point
if __name__ == "__main__":
    sys.exit(main())
