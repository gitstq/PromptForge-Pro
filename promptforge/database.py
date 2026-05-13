"""
PromptForge - SQLite数据库管理 / SQLite Database Manager
==========================================================

管理SQLite数据库的初始化、CRUD操作、版本管理和使用日志。
Manage SQLite database initialization, CRUD operations,
version management and usage logging.

Author: PromptForge Team
Version: 1.0.0
"""

import sqlite3
import json
import os
from typing import List, Optional, Dict, Any, Tuple
from contextlib import contextmanager

from .models import Prompt, PromptVersion, Tag, UsageLog
from .utils import generate_uuid, now_iso


class Database:
    """SQLite数据库管理类 / SQLite database manager class

    提供数据库初始化、连接管理和所有数据持久化操作。
    Provide database initialization, connection management
    and all data persistence operations.

    Attributes:
        db_path: 数据库文件路径 / Database file path
    """

    # 数据库Schema版本 / Database schema version
    SCHEMA_VERSION = 1

    def __init__(self, db_path: Optional[str] = None):
        """初始化数据库连接 / Initialize database connection

        Args:
            db_path: 数据库文件路径，默认为 ~/.promptforge/data.db
                     Database file path, default ~/.promptforge/data.db
        """
        if db_path is None:
            # 默认数据库路径 / Default database path
            home = os.path.expanduser("~")
            db_dir = os.path.join(home, ".promptforge")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "data.db")

        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接（上下文管理器）/ Get database connection (context manager)

        Yields:
            sqlite3.Connection: 数据库连接对象 / Database connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # 启用外键约束 / Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        """初始化数据库表结构 / Initialize database table structure

        创建prompts、versions、tags、usage_log等表。
        Create prompts, versions, tags, usage_log tables.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 创建prompts表 / Create prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    tags TEXT DEFAULT '[]',
                    score REAL DEFAULT 0.0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    usage_count INTEGER DEFAULT 0
                )
            """)

            # 创建versions表（版本历史）/ Create versions table (version history)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS versions (
                    id TEXT PRIMARY KEY,
                    prompt_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    change_note TEXT DEFAULT '',
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
                )
            """)

            # 创建tags表 / Create tags table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    name TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            """)

            # 创建usage_log表（使用日志）/ Create usage_log table (usage log)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage_log (
                    id TEXT PRIMARY KEY,
                    prompt_id TEXT NOT NULL,
                    used_at TEXT NOT NULL,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
                )
            """)

            # 创建索引 / Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_category
                ON prompts(category)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_score
                ON prompts(score DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompts_updated
                ON prompts(updated_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_versions_prompt_id
                ON versions(prompt_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_usage_log_prompt_id
                ON usage_log(prompt_id)
            """)

    # ============================================================
    # Prompt CRUD 操作 / Prompt CRUD Operations
    # ============================================================

    def add_prompt(self, prompt: Prompt) -> Prompt:
        """添加新prompt / Add new prompt

        Args:
            prompt: Prompt对象 / Prompt object

        Returns:
            Prompt: 添加后的Prompt（含数据库生成的字段）/ Added Prompt
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prompts (id, title, content, category, tags, score,
                                     created_at, updated_at, version, usage_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prompt.id, prompt.title, prompt.content, prompt.category,
                json.dumps(prompt.tags, ensure_ascii=False), prompt.score,
                prompt.created_at, prompt.updated_at, prompt.version,
                prompt.usage_count,
            ))

            # 更新标签计数 / Update tag counts
            self._update_tags(conn, prompt.tags, [])

        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """根据ID获取prompt / Get prompt by ID

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            Optional[Prompt]: Prompt对象或None / Prompt object or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_prompt(row)
        return None

    def get_prompt_by_short_id(self, short_id: str) -> Optional[Prompt]:
        """根据短ID获取prompt / Get prompt by short ID

        Args:
            short_id: 短ID（前8位）/ Short ID (first 8 chars)

        Returns:
            Optional[Prompt]: Prompt对象或None / Prompt object or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM prompts WHERE id LIKE ?",
                (short_id + "%",)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_prompt(row)
        return None

    def update_prompt(self, prompt: Prompt, change_note: str = "") -> Prompt:
        """更新prompt / Update prompt

        同时保存版本记录。
        Also save version record.

        Args:
            prompt: 更新后的Prompt对象 / Updated Prompt object
            change_note: 变更说明 / Change note

        Returns:
            Prompt: 更新后的Prompt / Updated Prompt
        """
        with self.get_connection() as conn:
            # 获取旧prompt数据 / Get old prompt data
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prompts WHERE id = ?", (prompt.id,))
            old_row = cursor.fetchone()
            if not old_row:
                raise ValueError(f"Prompt not found: {prompt.id}")

            old_prompt = self._row_to_prompt(old_row)

            # 保存版本记录 / Save version record
            version = PromptVersion(
                id=generate_uuid(),
                prompt_id=prompt.id,
                content=old_prompt.content,
                version=old_prompt.version,
                created_at=now_iso(),
                change_note=change_note,
            )
            cursor.execute("""
                INSERT INTO versions (id, prompt_id, content, version, created_at, change_note)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                version.id, version.prompt_id, version.content,
                version.version, version.created_at, version.change_note,
            ))

            # 更新prompt / Update prompt
            new_version = old_prompt.version + 1
            cursor.execute("""
                UPDATE prompts
                SET title = ?, content = ?, category = ?, tags = ?,
                    score = ?, updated_at = ?, version = ?
                WHERE id = ?
            """, (
                prompt.title, prompt.content, prompt.category,
                json.dumps(prompt.tags, ensure_ascii=False), prompt.score,
                prompt.updated_at, new_version, prompt.id,
            ))

            # 更新标签计数 / Update tag counts
            old_tags = old_prompt.tags
            new_tags = prompt.tags
            self._update_tags(conn, new_tags, old_tags)

            # 返回更新后的prompt / Return updated prompt
            prompt.version = new_version
            return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """删除prompt / Delete prompt

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            bool: 是否删除成功 / Whether deletion was successful
        """
        with self.get_connection() as conn:
            # 获取prompt的标签 / Get prompt's tags
            cursor = conn.cursor()
            cursor.execute("SELECT tags FROM prompts WHERE id = ?", (prompt_id,))
            row = cursor.fetchone()

            if not row:
                return False

            tags = json.loads(row["tags"])

            # 删除prompt（级联删除versions和usage_log）/ Delete prompt (cascade delete)
            cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))

            # 更新标签计数 / Update tag counts
            self._update_tags(conn, [], tags)

            return True

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
            sort_by: 排序字段（updated_at, score, title, created_at）
                     Sort field (updated_at, score, title, created_at)
            sort_order: 排序方向（asc, desc）/ Sort direction (asc, desc)
            limit: 返回数量限制 / Return count limit
            offset: 偏移量 / Offset

        Returns:
            List[Prompt]: Prompt列表 / Prompt list
        """
        # 验证排序参数 / Validate sort parameters
        valid_sort_fields = {"updated_at", "score", "title", "created_at", "usage_count"}
        if sort_by not in valid_sort_fields:
            sort_by = "updated_at"
        if sort_order.lower() not in ("asc", "desc"):
            sort_order = "desc"

        conditions = []
        params: List[Any] = []

        if category:
            conditions.append("category = ?")
            params.append(category)

        if tag:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag}"%')

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT * FROM prompts
            {where_clause}
            ORDER BY {sort_by} {sort_order.upper()}
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_prompt(row) for row in rows]

    def count_prompts(self, category: Optional[str] = None, tag: Optional[str] = None) -> int:
        """统计prompt数量 / Count prompts

        Args:
            category: 按分类过滤 / Filter by category
            tag: 按标签过滤 / Filter by tag

        Returns:
            int: prompt数量 / Prompt count
        """
        conditions = []
        params: List[Any] = []

        if category:
            conditions.append("category = ?")
            params.append(category)

        if tag:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag}"%')

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) as cnt FROM prompts {where_clause}", params)
            row = cursor.fetchone()
            return row["cnt"] if row else 0

    # ============================================================
    # 版本管理 / Version Management
    # ============================================================

    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """获取prompt的版本历史 / Get prompt version history

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            List[PromptVersion]: 版本列表（按版本号降序）/ Version list (descending)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM versions
                WHERE prompt_id = ?
                ORDER BY version DESC
            """, (prompt_id,))
            rows = cursor.fetchall()
            return [
                PromptVersion(
                    id=row["id"],
                    prompt_id=row["prompt_id"],
                    content=row["content"],
                    version=row["version"],
                    created_at=row["created_at"],
                    change_note=row["change_note"],
                )
                for row in rows
            ]

    def get_version(self, version_id: str) -> Optional[PromptVersion]:
        """获取特定版本 / Get specific version

        Args:
            version_id: 版本记录ID / Version record ID

        Returns:
            Optional[PromptVersion]: 版本对象或None / Version object or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM versions WHERE id = ?", (version_id,))
            row = cursor.fetchone()
            if row:
                return PromptVersion(
                    id=row["id"],
                    prompt_id=row["prompt_id"],
                    content=row["content"],
                    version=row["version"],
                    created_at=row["created_at"],
                    change_note=row["change_note"],
                )
        return None

    # ============================================================
    # 标签管理 / Tag Management
    # ============================================================

    def get_all_tags(self) -> List[Tag]:
        """获取所有标签 / Get all tags

        Returns:
            List[Tag]: 标签列表 / Tag list
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags ORDER BY count DESC")
            rows = cursor.fetchall()
            return [Tag(name=row["name"], count=row["count"]) for row in rows]

    def get_tag(self, name: str) -> Optional[Tag]:
        """获取特定标签 / Get specific tag

        Args:
            name: 标签名称 / Tag name

        Returns:
            Optional[Tag]: 标签对象或None / Tag object or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return Tag(name=row["name"], count=row["count"])
        return None

    def _update_tags(
        self,
        conn: sqlite3.Connection,
        new_tags: List[str],
        old_tags: List[str],
    ) -> None:
        """更新标签计数 / Update tag counts

        Args:
            conn: 数据库连接 / Database connection
            new_tags: 新标签列表 / New tag list
            old_tags: 旧标签列表 / Old tag list
        """
        cursor = conn.cursor()

        # 减少旧标签计数 / Decrease old tag counts
        for tag in set(old_tags):
            if tag not in new_tags:
                cursor.execute(
                    "UPDATE tags SET count = MAX(0, count - 1) WHERE name = ?",
                    (tag,)
                )
                # 删除计数为0的标签 / Delete tags with zero count
                cursor.execute("DELETE FROM tags WHERE name = ? AND count <= 0", (tag,))

        # 增加新标签计数 / Increase new tag counts
        for tag in set(new_tags):
            if tag not in old_tags:
                cursor.execute("""
                    INSERT INTO tags (name, count) VALUES (?, 1)
                    ON CONFLICT(name) DO UPDATE SET count = count + 1
                """, (tag,))

    # ============================================================
    # 使用日志 / Usage Logging
    # ============================================================

    def log_usage(self, prompt_id: str) -> None:
        """记录prompt使用 / Log prompt usage

        Args:
            prompt_id: Prompt ID / Prompt ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 添加使用日志 / Add usage log
            cursor.execute("""
                INSERT INTO usage_log (id, prompt_id, used_at)
                VALUES (?, ?, ?)
            """, (generate_uuid(), prompt_id, now_iso()))

            # 更新使用计数 / Update usage count
            cursor.execute("""
                UPDATE prompts SET usage_count = usage_count + 1
                WHERE id = ?
            """, (prompt_id,))

    def get_usage_count(self, prompt_id: str) -> int:
        """获取prompt使用次数 / Get prompt usage count

        Args:
            prompt_id: Prompt ID / Prompt ID

        Returns:
            int: 使用次数 / Usage count
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT usage_count FROM prompts WHERE id = ?",
                (prompt_id,)
            )
            row = cursor.fetchone()
            return row["usage_count"] if row else 0

    # ============================================================
    # 统计信息 / Statistics
    # ============================================================

    def get_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息 / Get database statistics

        Returns:
            Dict[str, Any]: 统计信息字典 / Statistics dictionary
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Prompt总数 / Total prompts
            cursor.execute("SELECT COUNT(*) as cnt FROM prompts")
            total_prompts = cursor.fetchone()["cnt"]

            # 平均评分 / Average score
            cursor.execute("SELECT AVG(score) as avg FROM prompts")
            avg_score = cursor.fetchone()["avg"] or 0.0

            # 标签总数 / Total tags
            cursor.execute("SELECT COUNT(*) as cnt FROM tags")
            total_tags = cursor.fetchone()["cnt"]

            # 总使用次数 / Total usage
            cursor.execute("SELECT SUM(usage_count) as total FROM prompts")
            total_usage = cursor.fetchone()["total"] or 0

            # 分类统计 / Category statistics
            cursor.execute("""
                SELECT category, COUNT(*) as cnt
                FROM prompts
                GROUP BY category
                ORDER BY cnt DESC
            """)
            categories = {row["category"]: row["cnt"] for row in cursor.fetchall()}

            # 评分分布 / Score distribution
            cursor.execute("""
                SELECT
                    CASE
                        WHEN score >= 80 THEN 'excellent'
                        WHEN score >= 60 THEN 'good'
                        WHEN score >= 40 THEN 'average'
                        ELSE 'poor'
                    END as level,
                    COUNT(*) as cnt
                FROM prompts
                GROUP BY level
            """)
            score_dist = {row["level"]: row["cnt"] for row in cursor.fetchall()}

            # 最近添加 / Recently added
            cursor.execute("""
                SELECT title, created_at FROM prompts
                ORDER BY created_at DESC LIMIT 5
            """)
            recent = [
                {"title": row["title"], "created_at": row["created_at"]}
                for row in cursor.fetchall()
            ]

            return {
                "total_prompts": total_prompts,
                "avg_score": round(avg_score, 1),
                "total_tags": total_tags,
                "total_usage": total_usage,
                "categories": categories,
                "score_distribution": score_dist,
                "recent_prompts": recent,
            }

    # ============================================================
    # 全文搜索支持 / Full-text Search Support
    # ============================================================

    def get_all_prompts_for_search(self) -> List[Prompt]:
        """获取所有prompt用于搜索索引 / Get all prompts for search index

        Returns:
            List[Prompt]: 所有Prompt列表 / All Prompt list
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prompts")
            rows = cursor.fetchall()
            return [self._row_to_prompt(row) for row in rows]

    # ============================================================
    # 内部方法 / Internal Methods
    # ============================================================

    @staticmethod
    def _row_to_prompt(row: sqlite3.Row) -> Prompt:
        """将数据库行转换为Prompt对象 / Convert database row to Prompt object

        Args:
            row: SQLite行对象 / SQLite row object

        Returns:
            Prompt: Prompt对象 / Prompt object
        """
        tags = json.loads(row["tags"]) if row["tags"] else []
        return Prompt(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            category=row["category"],
            tags=tags,
            score=row["score"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            version=row["version"],
            usage_count=row["usage_count"],
        )

    def close(self) -> None:
        """关闭数据库连接 / Close database connection

        注意：由于使用上下文管理器，此方法主要用于兼容性。
        Note: Since context managers are used, this method is mainly for compatibility.
        """
        pass

    def __repr__(self) -> str:
        return f"Database(db_path='{self.db_path}')"
