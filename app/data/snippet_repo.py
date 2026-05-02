"""Repository for code snippets CRUD operations"""

from typing import List, Dict, Optional
from .database import Database


class SnippetRepository:
    """Manages code snippets in SQLite"""

    def __init__(self, database: Database):
        self.db = database

    def create(self, name: str, language: str, code: str, tags: str = "") -> int:
        """Create a new snippet"""
        cursor = self.db.get_connection().cursor()
        cursor.execute(
            """
            INSERT INTO snippets (name, language, code, tags)
            VALUES (?, ?, ?, ?)
        """,
            (name, language, code, tags),
        )
        self.db.get_connection().commit()
        return cursor.lastrowid

    def get_by_id(self, snippet_id: int) -> Optional[Dict]:
        """Get a snippet by ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM snippets WHERE id = ?", (snippet_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_dict(row)
        return None

    def get_all(self) -> List[Dict]:
        """Get all snippets, most recent first"""
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM snippets ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def search(self, query: str) -> List[Dict]:
        """Search snippets by name, language, or tags"""
        cursor = self.db.get_connection().cursor()
        search_pattern = f"%{query}%"
        cursor.execute(
            """
            SELECT * FROM snippets
            WHERE name LIKE ? OR language LIKE ? OR tags LIKE ?
            ORDER BY created_at DESC
        """,
            (search_pattern, search_pattern, search_pattern),
        )
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update(
        self, snippet_id: int, name: str, language: str, code: str, tags: str
    ):
        """Update a snippet"""
        cursor = self.db.get_connection().cursor()
        cursor.execute(
            """
            UPDATE snippets
            SET name = ?, language = ?, code = ?, tags = ?
            WHERE id = ?
        """,
            (name, language, code, tags, snippet_id),
        )
        self.db.get_connection().commit()

    def delete(self, snippet_id: int):
        """Delete a snippet"""
        cursor = self.db.get_connection().cursor()
        cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        self.db.get_connection().commit()

    def _row_to_dict(self, row) -> Dict:
        """Convert a database row to a dictionary"""
        return {
            "id": row["id"],
            "created_at": row["created_at"],
            "name": row["name"],
            "language": row["language"],
            "tags": row["tags"],
            "code": row["code"],
        }
