import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from models import ComparisonRequest, ComparisonResult

class Database:
    def __init__(self, db_path: str = "decisions.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create comparisons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparisons (
                id TEXT PRIMARY KEY,
                request_data TEXT NOT NULL,
                result_data TEXT NOT NULL,
                use_case TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create options table for easier querying
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparison_options (
                comparison_id TEXT,
                option_name TEXT,
                option_data TEXT,
                score REAL,
                FOREIGN KEY (comparison_id) REFERENCES comparisons (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def store_comparison(self, request: ComparisonRequest, result: ComparisonResult) -> str:
        """Store a comparison request and result"""
        comparison_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Store main comparison
            cursor.execute('''
                INSERT INTO comparisons (id, request_data, result_data, use_case, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                comparison_id,
                json.dumps(request.dict()),
                json.dumps(result.dict()),
                request.use_case,
                timestamp
            ))
            
            # Store individual options for easier querying
            for option in request.options:
                # Find the score for this option
                option_score = next((s for s in result.scores if s.option_name == option.name), None)
                score = option_score.weighted_score if option_score else 0.0
                
                cursor.execute('''
                    INSERT INTO comparison_options (comparison_id, option_name, option_data, score)
                    VALUES (?, ?, ?, ?)
                ''', (
                    comparison_id,
                    option.name,
                    json.dumps(option.dict()),
                    score
                ))
            
            conn.commit()
            return comparison_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    async def get_comparison(self, comparison_id: str) -> Optional[Dict]:
        """Retrieve a specific comparison by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT request_data, result_data, use_case, timestamp, created_at
                FROM comparisons
                WHERE id = ?
            ''', (comparison_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            request_data, result_data, use_case, timestamp, created_at = row
            
            return {
                "id": comparison_id,
                "request": json.loads(request_data),
                "result": json.loads(result_data),
                "use_case": use_case,
                "timestamp": timestamp,
                "created_at": created_at
            }
            
        finally:
            conn.close()
    
    async def list_comparisons(self, limit: int = 10) -> List[Dict]:
        """List recent comparisons"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, use_case, timestamp, created_at,
                       COUNT(co.option_name) as option_count
                FROM comparisons c
                LEFT JOIN comparison_options co ON c.id = co.comparison_id
                GROUP BY c.id, c.use_case, c.timestamp, c.created_at
                ORDER BY c.created_at DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            comparisons = []
            for row in rows:
                comparison_id, use_case, timestamp, created_at, option_count = row
                comparisons.append({
                    "id": comparison_id,
                    "use_case": use_case,
                    "timestamp": timestamp,
                    "created_at": created_at,
                    "option_count": option_count
                })
            
            return comparisons
            
        finally:
            conn.close()
    
    async def search_comparisons(self, query: str, limit: int = 10) -> List[Dict]:
        """Search comparisons by use case or option names"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT DISTINCT c.id, c.use_case, c.timestamp, c.created_at
                FROM comparisons c
                LEFT JOIN comparison_options co ON c.id = co.comparison_id
                WHERE c.use_case LIKE ? OR co.option_name LIKE ?
                ORDER BY c.created_at DESC
                LIMIT ?
            ''', (f"%{query}%", f"%{query}%", limit))
            
            rows = cursor.fetchall()
            
            comparisons = []
            for row in rows:
                comparison_id, use_case, timestamp, created_at = row
                comparisons.append({
                    "id": comparison_id,
                    "use_case": use_case,
                    "timestamp": timestamp,
                    "created_at": created_at
                })
            
            return comparisons
            
        finally:
            conn.close()
    
    async def get_popular_options(self, limit: int = 10) -> List[Dict]:
        """Get most frequently compared options"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT option_name, COUNT(*) as usage_count, AVG(score) as avg_score
                FROM comparison_options
                GROUP BY option_name
                ORDER BY usage_count DESC, avg_score DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            
            options = []
            for row in rows:
                option_name, usage_count, avg_score = row
                options.append({
                    "name": option_name,
                    "usage_count": usage_count,
                    "average_score": round(avg_score, 2) if avg_score else 0
                })
            
            return options
            
        finally:
            conn.close()