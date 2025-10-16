from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from contextlib import contextmanager


class Database:
    def __init__(self, db_path: str = "doubletrust.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self) -> None:
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create agents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    id VARCHAR PRIMARY KEY,
                    file_path VARCHAR,
                    role VARCHAR,
                    system_prompt TEXT,
                    model VARCHAR,
                    temperature FLOAT,
                    framework VARCHAR,
                    risk VARCHAR,
                    risk_reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create per-agent tools table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_tools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id VARCHAR,
                    name VARCHAR,
                    description TEXT,
                    parameters JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (agent_id) REFERENCES agents (id)
                )
            """)
            # Ensure uniqueness of tool names per agent to avoid duplicates
            # First, deduplicate any existing rows by keeping the lowest id per (agent_id, name)
            cursor.execute(
                """
                DELETE FROM agent_tools
                WHERE id NOT IN (
                    SELECT MIN(id) FROM agent_tools GROUP BY agent_id, name
                )
                """
            )
            # Then create the unique index (ignore error if already exists)
            try:
                cursor.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS idx_agent_tools_unique ON agent_tools(agent_id, name)"
                )
            except Exception:
                pass
            
            
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Get a database connection with proper error handling"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get a single agent by ID"""
        results = self.execute_query(
            "SELECT * FROM agents WHERE id = ?", (agent_id,)
        )
        return results[0] if results else None

    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agents"""
        return self.execute_query("SELECT * FROM agents ORDER BY created_at DESC")

    def create_agent(self, agent_data: Dict[str, Any]) -> str:
        """Create a new agent"""
        query = """
            INSERT INTO agents (id, file_path, role, system_prompt, model, temperature, framework, risk, risk_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            agent_data["id"],
            agent_data.get("file_path"),
            agent_data["role"],
            agent_data["system_prompt"],
            agent_data.get("model"),
            agent_data.get("temperature"),
            agent_data.get("framework"),
            agent_data.get("risk"),
            agent_data.get("risk_reason"),
        )
        self.execute_update(query, params)
        return agent_data["id"]

    # Tools CRUD for per-agent tools
    def create_agent_tool(self, tool_data: Dict[str, Any]) -> int:
        query = """
            INSERT OR IGNORE INTO agent_tools (agent_id, name, description, parameters)
            VALUES (?, ?, ?, ?)
        """
        import json
        params = (
            tool_data["agent_id"],
            tool_data["name"],
            tool_data.get("description"),
            json.dumps(tool_data.get("parameters") or {}),
        )
        self.execute_update(query, params)
        result = self.execute_query(
            "SELECT id FROM agent_tools WHERE agent_id = ? AND name = ? ORDER BY id DESC LIMIT 1",
            (tool_data["agent_id"], tool_data["name"]),
        )
        return result[0]["id"]

    def has_agent_tool(self, agent_id: str, name: str) -> bool:
        """Check if a tool already exists for an agent by name"""
        res = self.execute_query(
            "SELECT 1 AS x FROM agent_tools WHERE agent_id = ? AND name = ? LIMIT 1",
            (agent_id, name),
        )
        return len(res) > 0

    def get_agent_tools(self, agent_id: str) -> List[Dict[str, Any]]:
        return self.execute_query(
            "SELECT id, name, description, parameters FROM agent_tools WHERE agent_id = ? ORDER BY name",
            (agent_id,),
        )




# Global database instance
db = Database()
