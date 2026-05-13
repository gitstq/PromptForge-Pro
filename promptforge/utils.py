"""
PromptForge - 工具函数 / Utility Functions
============================================

提供UUID生成、时间格式化、ANSI颜色、文本处理、表格格式化等通用工具。
Provide UUID generation, time formatting, ANSI colors, text processing,
table formatting and other utilities.

Author: PromptForge Team
Version: 1.0.0
"""

import uuid
import os
import re
import math
import textwrap
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Any


# ============================================================
# UUID 生成 / UUID Generation
# ============================================================

def generate_uuid() -> str:
    """生成UUID字符串 / Generate UUID string

    Returns:
        str: UUID v4格式字符串 / UUID v4 format string
    """
    return str(uuid.uuid4())


def generate_short_id() -> str:
    """生成短ID（前8位UUID）/ Generate short ID (first 8 chars of UUID)

    Returns:
        str: 8字符短ID / 8-character short ID
    """
    return str(uuid.uuid4())[:8]


# ============================================================
# 时间格式化 / Time Formatting
# ============================================================

def now_iso() -> str:
    """获取当前时间的ISO格式字符串 / Get current time in ISO format

    Returns:
        str: ISO 8601格式时间字符串 / ISO 8601 format time string
    """
    return datetime.now(timezone.utc).isoformat()


def format_datetime(dt_str: str) -> str:
    """格式化ISO时间为可读字符串 / Format ISO time to readable string

    Args:
        dt_str: ISO格式时间字符串 / ISO format time string

    Returns:
        str: 可读时间字符串 / Readable time string
    """
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return dt_str


def time_ago(dt_str: str) -> str:
    """计算相对时间 / Calculate relative time

    Args:
        dt_str: ISO格式时间字符串 / ISO format time string

    Returns:
        str: 相对时间描述 / Relative time description
    """
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt
        seconds = int(diff.total_seconds())

        if seconds < 60:
            return "刚刚 / just now"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}分钟前 / {minutes}m ago"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}小时前 / {hours}h ago"
        elif seconds < 2592000:
            days = seconds // 86400
            return f"{days}天前 / {days}d ago"
        else:
            months = seconds // 2592000
            return f"{months}个月前 / {months}mo ago"
    except (ValueError, AttributeError):
        return dt_str


# ============================================================
# ANSI 颜色代码 / ANSI Color Codes
# ============================================================

class Color:
    """ANSI颜色代码类 / ANSI color code class

    提供终端彩色输出支持。
    Provide terminal color output support.
    """
    # 基础颜色 / Basic colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # 前景色 / Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    # 亮色 / Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    # 背景色 / Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


def colored(text: str, color: str) -> str:
    """为文本添加颜色 / Add color to text

    Args:
        text: 原始文本 / Original text
        color: ANSI颜色代码 / ANSI color code

    Returns:
        str: 带颜色的文本 / Colored text
    """
    # 检测是否在支持颜色的终端中运行
    # Check if running in a terminal that supports colors
    if not os.environ.get("NO_COLOR") and os.environ.get("TERM") not in ("dumb", ""):
        return f"{color}{text}{Color.RESET}"
    return text


def color_score(score: float) -> str:
    """根据分数返回带颜色的分数文本 / Return colored score text based on score

    Args:
        score: 评分值（0-100）/ Score value (0-100)

    Returns:
        str: 带颜色的分数文本 / Colored score text
    """
    score_str = f"{score:.1f}"
    if score >= 80:
        return colored(score_str, Color.BRIGHT_GREEN)
    elif score >= 60:
        return colored(score_str, Color.BRIGHT_YELLOW)
    elif score >= 40:
        return colored(score_str, Color.YELLOW)
    else:
        return colored(score_str, Color.BRIGHT_RED)


# ============================================================
# 文本处理 / Text Processing
# ============================================================

def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """截断文本 / Truncate text

    Args:
        text: 原始文本 / Original text
        max_length: 最大长度 / Maximum length
        suffix: 截断后缀 / Truncation suffix

    Returns:
        str: 截断后的文本 / Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def word_count(text: str) -> int:
    """统计词数（支持中英文）/ Count words (support Chinese and English)

    Args:
        text: 输入文本 / Input text

    Returns:
        int: 词数 / Word count
    """
    # 中文字符数 / Chinese character count
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词数 / English word count
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return chinese_chars + english_words


def char_count(text: str) -> int:
    """统计字符数（不含空白）/ Count characters (excluding whitespace)

    Args:
        text: 输入文本 / Input text

    Returns:
        int: 字符数 / Character count
    """
    return len(text.replace(" ", "").replace("\n", "").replace("\t", ""))


def remove_ansi(text: str) -> str:
    """移除ANSI转义码 / Remove ANSI escape codes

    Args:
        text: 包含ANSI码的文本 / Text with ANSI codes

    Returns:
        str: 纯文本 / Plain text
    """
    return re.sub(r'\033\[[0-9;]*m', '', text)


def highlight_text(text: str, keywords: List[str], color: str = Color.BRIGHT_YELLOW) -> str:
    """高亮文本中的关键词 / Highlight keywords in text

    Args:
        text: 原始文本 / Original text
        keywords: 关键词列表 / Keyword list
        color: 高亮颜色 / Highlight color

    Returns:
        str: 高亮后的文本 / Highlighted text
    """
    result = text
    for keyword in keywords:
        if keyword:
            # 不区分大小写替换 / Case-insensitive replacement
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            result = pattern.sub(
                lambda m: colored(m.group(), color),
                result
            )
    return result


# ============================================================
# 表格格式化 / Table Formatting
# ============================================================

def format_table(
    headers: List[str],
    rows: List[List[str]],
    max_col_width: int = 30,
    padding: int = 2,
) -> str:
    """格式化文本表格 / Format text table

    Args:
        headers: 表头列表 / Header list
        rows: 数据行列表 / Data row list
        max_col_width: 列最大宽度 / Column max width
        padding: 单元格内边距 / Cell padding

    Returns:
        str: 格式化后的表格字符串 / Formatted table string
    """
    if not rows and not headers:
        return ""

    # 计算每列宽度 / Calculate column widths
    col_count = len(headers)
    col_widths = [0] * col_count

    # 考虑表头宽度 / Consider header widths
    for i, header in enumerate(headers):
        col_widths[i] = max(col_widths[i], len(remove_ansi(header)))

    # 考虑数据行宽度 / Consider data row widths
    for row in rows:
        for i, cell in enumerate(row):
            if i < col_count:
                col_widths[i] = max(col_widths[i], len(remove_ansi(str(cell))))

    # 限制最大宽度 / Limit max width
    col_widths = [min(w, max_col_width) for w in col_widths]

    # 构建分隔线 / Build separator
    sep = "+" + "+".join("-" * (w + padding * 2) for w in col_widths) + "+"

    # 构建表头 / Build header
    header_line = "|"
    for i, header in enumerate(headers):
        cell_text = remove_ansi(header)
        if len(cell_text) > col_widths[i]:
            cell_text = cell_text[: col_widths[i] - 1] + "..."
        header_line += " " * padding + cell_text.ljust(col_widths[i]) + " " * padding + "|"

    # 构建数据行 / Build data rows
    data_lines = []
    for row in rows:
        line = "|"
        for i, cell in enumerate(row):
            if i < col_count:
                cell_text = remove_ansi(str(cell))
                if len(cell_text) > col_widths[i]:
                    cell_text = cell_text[: col_widths[i] - 1] + "..."
                line += " " * padding + cell_text.ljust(col_widths[i]) + " " * padding + "|"
            else:
                line += " " * padding + " " * col_widths[0] + " " * padding + "|"
        data_lines.append(line)

    # 组合表格 / Assemble table
    lines = [sep, header_line, sep]
    for data_line in data_lines:
        lines.append(data_line)
    lines.append(sep)

    return "\n".join(lines)


def format_prompt_table(prompts_data: List[List[str]]) -> str:
    """格式化Prompt列表表格 / Format prompt list table

    Args:
        prompts_data: Prompt数据行列表 / Prompt data row list
            每行格式: [ID, 标题, 分类, 标签, 评分, 更新时间]
            Each row format: [ID, Title, Category, Tags, Score, Updated]

    Returns:
        str: 格式化后的表格 / Formatted table
    """
    headers = [
        colored("ID", Color.CYAN),
        colored("标题/Title", Color.CYAN),
        colored("分类/Cat", Color.CYAN),
        colored("标签/Tags", Color.CYAN),
        colored("评分/Score", Color.CYAN),
        colored("更新/Updated", Color.CYAN),
    ]
    return format_table(headers, prompts_data, max_col_width=35)


# ============================================================
# 输入验证 / Input Validation
# ============================================================

def validate_prompt_content(content: str) -> Tuple[bool, str]:
    """验证prompt内容 / Validate prompt content

    Args:
        content: prompt内容 / Prompt content

    Returns:
        Tuple[bool, str]: (是否有效, 错误消息) / (is valid, error message)
    """
    if not content or not content.strip():
        return False, "内容不能为空 / Content cannot be empty"

    stripped = content.strip()
    if len(stripped) < 3:
        return False, "内容太短，至少需要3个字符 / Content too short, need at least 3 chars"

    if len(stripped) > 100000:
        return False, "内容太长，最大支持100000字符 / Content too long, max 100000 chars"

    return True, ""


def validate_title(title: str) -> Tuple[bool, str]:
    """验证标题 / Validate title

    Args:
        title: 标题文本 / Title text

    Returns:
        bool: 是否有效 / Is valid
        str: 错误消息 / Error message
    """
    if not title or not title.strip():
        return False, "标题不能为空 / Title cannot be empty"

    if len(title.strip()) > 200:
        return False, "标题太长，最大200字符 / Title too long, max 200 chars"

    return True, ""


# ============================================================
# 编辑距离 / Edit Distance
# ============================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """计算Levenshtein编辑距离 / Calculate Levenshtein edit distance

    用于模糊搜索匹配。
    Used for fuzzy search matching.

    Args:
        s1: 字符串1 / String 1
        s2: 字符串2 / String 2

    Returns:
        int: 编辑距离 / Edit distance
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # 计算插入、删除、替换的代价
            # Calculate cost of insert, delete, replace
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def similarity(s1: str, s2: str) -> float:
    """计算字符串相似度（0-1）/ Calculate string similarity (0-1)

    Args:
        s1: 字符串1 / String 1
        s2: 字符串2 / String 2

    Returns:
        float: 相似度（0到1之间）/ Similarity (between 0 and 1)
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    max_len = max(len(s1), len(s2))
    dist = levenshtein_distance(s1.lower(), s2.lower())
    return 1.0 - (dist / max_len)


# ============================================================
# 文本Diff / Text Diff
# ============================================================

def simple_diff(old_text: str, new_text: str, context_lines: int = 2) -> str:
    """简单的文本差异比较 / Simple text diff comparison

    Args:
        old_text: 旧文本 / Old text
        new_text: 新文本 / New text
        context_lines: 上下文行数 / Context lines

    Returns:
        str: 差异结果文本 / Diff result text
    """
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    # 使用简单的行级比较 / Use simple line-level comparison
    diff_lines = []
    max_lines = max(len(old_lines), len(new_lines))

    for i in range(max_lines):
        old_line = old_lines[i] if i < len(old_lines) else None
        new_line = new_lines[i] if i < len(new_lines) else None

        if old_line == new_line:
            diff_lines.append(f"  {old_line}")
        elif old_line is None:
            diff_lines.append(f"{colored('+', Color.GREEN)} {new_line}")
        elif new_line is None:
            diff_lines.append(f"{colored('-', Color.RED)} {old_line}")
        else:
            diff_lines.append(f"{colored('-', Color.RED)} {old_line}")
            diff_lines.append(f"{colored('+', Color.GREEN)} {new_line}")

    return "\n".join(diff_lines)


# ============================================================
# 进度条 / Progress Bar
# ============================================================

def progress_bar(
    current: int,
    total: int,
    width: int = 30,
    prefix: str = "",
    suffix: str = "",
) -> str:
    """生成文本进度条 / Generate text progress bar

    Args:
        current: 当前进度 / Current progress
        total: 总数 / Total
        width: 进度条宽度 / Progress bar width
        prefix: 前缀文本 / Prefix text
        suffix: 后缀文本 / Suffix text

    Returns:
        str: 进度条字符串 / Progress bar string
    """
    if total == 0:
        percent = 100.0
    else:
        percent = (current / total) * 100

    filled = int(width * current / total) if total > 0 else width
    bar = "█" * filled + "░" * (width - filled)

    return f"{prefix} |{bar}| {percent:.1f}% {suffix}"


# ============================================================
# 安全处理 / Safe Handling
# ============================================================

def safe_input(prompt: str, default: str = "") -> str:
    """安全的输入处理 / Safe input handling

    Args:
        prompt: 提示文本 / Prompt text
        default: 默认值 / Default value

    Returns:
        str: 用户输入或默认值 / User input or default value
    """
    try:
        value = input(prompt).strip()
        return value if value else default
    except (EOFError, KeyboardInterrupt):
        print()  # 换行 / Newline
        return default


def safe_int_input(prompt: str, default: int = 0, min_val: int = 0, max_val: int = 999999) -> int:
    """安全的整数输入 / Safe integer input

    Args:
        prompt: 提示文本 / Prompt text
        default: 默认值 / Default value
        min_val: 最小值 / Minimum value
        max_val: 最大值 / Maximum value

    Returns:
        int: 用户输入的整数 / User input integer
    """
    try:
        value = input(prompt).strip()
        if not value:
            return default
        result = int(value)
        return max(min_val, min(max_val, result))
    except (ValueError, EOFError, KeyboardInterrupt):
        print()
        return default
