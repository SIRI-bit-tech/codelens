"""SQLite database connection and schema setup"""

import sqlite3
import os
from pathlib import Path
from typing import Optional


class Database:
    """Manages SQLite database connection and schema"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            app_data_dir = Path.home() / ".codelens"
            app_data_dir.mkdir(exist_ok=True)
            db_path = str(app_data_dir / "codelens.db")

        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self._initialize()

    def _initialize(self):
        """Initialize database and create tables"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT NOT NULL,
                mode TEXT NOT NULL,
                code TEXT NOT NULL,
                explanation TEXT NOT NULL,
                chat_history TEXT DEFAULT '[]'
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name TEXT NOT NULL,
                language TEXT NOT NULL,
                tags TEXT DEFAULT '',
                code TEXT NOT NULL
            )
        """
        )

        self.connection.commit()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if self.connection is None:
            self._initialize()
        return self.connection

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
