"""Repository for explanation history CRUD operations"""

import json
from typing import List, Dict, Optional
from datetime import datetime
from .database import Database


class HistoryRepository:
    """Manages explanation history in SQLite"""

    def __init__(self, database: Database):
        self.db = database

    def create(
        self,
        language: str,
        mode: str,
        code: str,
        explanation: str,
        chat_history: Optional[List[Dict]] = None,
    ) -> int:
        """Create a new history entry"""
        if chat_history is None:
            chat_history = []

        cursor = self.db.get_connection().cursor()
        cursor.execute(
            """
            INSERT INTO history (language, mode, code, explanation, chat_history)
            VALUES (?, ?, ?, ?, ?)
        """,
            (language, mode, code, explanation, json.dumps(chat_history)),
        )
        self.db.get_connection().commit()
        return cursor.lastrowid

    def get_by_id(self, history_id: int) -> Optional[Dict]:
        """Get a history entry by ID"""
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM history WHERE id = ?", (history_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_dict(row)
        return None

    def get_all(self, limit: int = 20) -> List[Dict]:
        """Get all history entries, most recent first"""
        cursor = self.db.get_connection().cursor()
        cursor.execute(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update_chat_history(self, history_id: int, chat_history: List[Dict]):
        """Update chat history for an entry"""
        cursor = self.db.get_connection().cursor()
        cursor.execute(
            "UPDATE history SET chat_history = ? WHERE id = ?",
            (json.dumps(chat_history), history_id),
        )
        self.db.get_connection().commit()

    def delete(self, history_id: int):
        """Delete a history entry"""
        cursor = self.db.get_connection().cursor()
        cursor.execute("DELETE FROM history WHERE id = ?", (history_id,))
        self.db.get_connection().commit()

    def delete_old_entries(self, keep_count: int = 20):
        """Delete old entries, keeping only the most recent ones"""
        cursor = self.db.get_connection().cursor()
        cursor.execute(
            """
            DELETE FROM history
            WHERE id NOT IN (
                SELECT id FROM history
                ORDER BY created_at DESC
                LIMIT ?
            )
        """,
            (keep_count,),
        )
        self.db.get_connection().commit()

    def _row_to_dict(self, row) -> Dict:
        """Convert a database row to a dictionary"""
        return {
            "id": row["id"],
            "created_at": row["created_at"],
            "language": row["language"],
            "mode": row["mode"],
            "code": row["code"],
            "explanation": row["explanation"],
            "chat_history": json.loads(row["chat_history"]),
        }
