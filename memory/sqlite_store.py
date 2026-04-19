"""
SQLite Store

Structured memory storage using SQLite3 with FTS5 full-text search.
"""

from typing import Dict, Any, Optional, List
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


class SQLiteStore:
    """
    Structured memory store using SQLite3 with FTS5.
    
    Features:
    - Fast structured storage layer
    - Full-text search indexing
    - Task history and execution logs
    """
    
    def __init__(self, db_path: str = "memory/sqlite/brain.db"):
        """
        Initialize the SQLite Store.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._connect()
        self._initialize_schema()
        logger.info(f"SQLiteStore initialized at {self.db_path}")
    
    def _connect(self) -> None:
        """Establish database connection."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
    
    def _initialize_schema(self) -> None:
        """Initialize database schema with FTS5 support."""
        cursor = self.conn.cursor()
        
        # Create main memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                memory_type TEXT DEFAULT 'structured',
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create FTS5 virtual table for full-text search
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                key,
                value,
                content='memory_entries',
                content_rowid='id'
            )
        ''')
        
        # Create task history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE NOT NULL,
                task_type TEXT,
                description TEXT,
                status TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create execution logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT,
                action TEXT,
                details TEXT
            )
        ''')
        
        self.conn.commit()
        logger.info("Database schema initialized")
    
    def write(self, key: str, value: Any, memory_type: str = "structured", 
              metadata: Dict[str, Any] = None) -> bool:
        """
        Write data to the database.
        
        Args:
            key: Unique identifier
            value: Data to store
            memory_type: Type of memory entry
            metadata: Additional metadata
            
        Returns:
            True if write was successful
        """
        try:
            cursor = self.conn.cursor()
            import json
            
            cursor.execute('''
                INSERT OR REPLACE INTO memory_entries (key, value, memory_type, metadata, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (key, str(value), memory_type, json.dumps(metadata or {})))
            
            # Update FTS index
            cursor.execute('''
                INSERT OR REPLACE INTO memory_fts (rowid, key, value)
                VALUES ((SELECT id FROM memory_entries WHERE key = ?), ?, ?)
            ''', (key, key, str(value)))
            
            self.conn.commit()
            logger.info(f"Memory entry written: {key}")
            return True
        except Exception as e:
            logger.error(f"Error writing memory entry: {e}")
            self.conn.rollback()
            return False
    
    def read(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Read data from the database.
        
        Args:
            key: Unique identifier
            
        Returns:
            Dictionary with entry data or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM memory_entries WHERE key = ?', (key,))
        row = cursor.fetchone()
        
        if row:
            logger.info(f"Memory entry read: {key}")
            return dict(row)
        
        logger.warning(f"Memory entry not found: {key}")
        return None
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search entries using FTS5 full-text search.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching entries
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT me.* FROM memory_fts mft
            JOIN memory_entries me ON mft.rowid = me.id
            WHERE memory_fts MATCH ?
            LIMIT ?
        ''', (query, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        logger.info(f"Search returned {len(results)} results for: {query[:50]}...")
        return results
    
    def delete(self, key: str) -> bool:
        """
        Delete an entry from the database.
        
        Args:
            key: Unique identifier
            
        Returns:
            True if deletion was successful
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM memory_entries WHERE key = ?', (key,))
            self.conn.commit()
            logger.info(f"Memory entry deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting memory entry: {e}")
            self.conn.rollback()
            return False
    
    def log_task(self, task_id: str, task_type: str, description: str, 
                 status: str, result: str = None) -> bool:
        """
        Log a task execution to history.
        
        Args:
            task_id: Unique task identifier
            task_type: Type of task
            description: Task description
            status: Task status
            result: Task result
            
        Returns:
            True if logging was successful
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO task_history (task_id, task_type, description, status, result)
                VALUES (?, ?, ?, ?, ?)
            ''', (task_id, task_type, description, status, result))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error logging task: {e}")
            return False
    
    def log_execution(self, agent_name: str, action: str, details: str = None) -> bool:
        """
        Log an agent execution action.
        
        Args:
            agent_name: Name of the agent
            action: Action performed
            details: Additional details
            
        Returns:
            True if logging was successful
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO execution_logs (agent_name, action, details)
                VALUES (?, ?, ?)
            ''', (agent_name, action, details))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error logging execution: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary containing database statistics
        """
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM memory_entries')
        entry_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM task_history')
        task_count = cursor.fetchone()[0]
        
        return {
            "database_path": str(self.db_path),
            "memory_entries": entry_count,
            "task_history_entries": task_count,
            "status": "connected"
        }
    
    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
