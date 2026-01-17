"""통계 관리 시스템 (SQLite)"""
import sqlite3
import os
from typing import Dict, Optional, Tuple
from datetime import datetime


class StatsManager:
    """게임 통계 관리 클래스 (SQLite 기반)"""
    
    def __init__(self, db_path: str = "data/stats.db"):
        """
        통계 매니저 초기화
        
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self._ensure_directory()
        self._init_database()
        
    def _ensure_directory(self) -> None:
        """데이터 디렉토리 생성"""
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
    def _init_database(self) -> None:
        """데이터베이스 초기화 및 테이블 생성"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 전체 통계 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS global_stats (
                id INTEGER PRIMARY KEY,
                total_playtime REAL DEFAULT 0,
                total_games INTEGER DEFAULT 0,
                total_food_eaten INTEGER DEFAULT 0,
                total_golden_apples INTEGER DEFAULT 0,
                total_powerups_collected INTEGER DEFAULT 0
            )
        """)
        
        # 난이도별 최고 점수
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS difficulty_highscores (
                difficulty TEXT PRIMARY KEY,
                highscore INTEGER DEFAULT 0,
                achieved_at TEXT
            )
        """)
        
        # 모드별 최고 점수
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mode_highscores (
                mode TEXT PRIMARY KEY,
                highscore INTEGER DEFAULT 0,
                achieved_at TEXT
            )
        """)
        
        # 생존 시간 기록
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS survival_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survival_time REAL,
                achieved_at TEXT
            )
        """)
        
        # 초기 데이터 삽입
        cursor.execute("SELECT COUNT(*) FROM global_stats")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO global_stats (id) VALUES (1)")
            
        conn.commit()
        conn.close()
        
    def record_game(self, playtime: float, food_eaten: int, 
                   golden_apples: int = 0, powerups_collected: int = 0) -> None:
        """
        게임 플레이 기록
        
        Args:
            playtime: 플레이 시간 (초)
            food_eaten: 먹은 먹이 수
            golden_apples: 먹은 골든 애플 수
            powerups_collected: 수집한 파워업 수
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE global_stats 
            SET total_playtime = total_playtime + ?,
                total_games = total_games + 1,
                total_food_eaten = total_food_eaten + ?,
                total_golden_apples = total_golden_apples + ?,
                total_powerups_collected = total_powerups_collected + ?
            WHERE id = 1
        """, (playtime, food_eaten, golden_apples, powerups_collected))
        
        conn.commit()
        conn.close()
        
    def update_difficulty_highscore(self, difficulty: str, score: int) -> bool:
        """
        난이도별 최고 점수 업데이트
        
        Args:
            difficulty: 난이도
            score: 점수
            
        Returns:
            새로운 최고 점수인지 여부
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT highscore FROM difficulty_highscores WHERE difficulty = ?",
            (difficulty,)
        )
        result = cursor.fetchone()
        
        is_new_highscore = False
        if result is None or score > result[0]:
            is_new_highscore = True
            cursor.execute("""
                INSERT OR REPLACE INTO difficulty_highscores 
                (difficulty, highscore, achieved_at) 
                VALUES (?, ?, ?)
            """, (difficulty, score, datetime.now().isoformat()))
            
        conn.commit()
        conn.close()
        return is_new_highscore
        
    def update_mode_highscore(self, mode: str, score: int) -> bool:
        """
        모드별 최고 점수 업데이트
        
        Args:
            mode: 게임 모드
            score: 점수
            
        Returns:
            새로운 최고 점수인지 여부
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT highscore FROM mode_highscores WHERE mode = ?",
            (mode,)
        )
        result = cursor.fetchone()
        
        is_new_highscore = False
        if result is None or score > result[0]:
            is_new_highscore = True
            cursor.execute("""
                INSERT OR REPLACE INTO mode_highscores 
                (mode, highscore, achieved_at) 
                VALUES (?, ?, ?)
            """, (mode, score, datetime.now().isoformat()))
            
        conn.commit()
        conn.close()
        return is_new_highscore
        
    def record_survival_time(self, survival_time: float) -> None:
        """
        생존 시간 기록
        
        Args:
            survival_time: 생존 시간 (초)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO survival_records (survival_time, achieved_at)
            VALUES (?, ?)
        """, (survival_time, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
    def get_global_stats(self) -> Dict[str, float]:
        """
        전체 통계 가져오기
        
        Returns:
            통계 딕셔너리
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT total_playtime, total_games, total_food_eaten,
                   total_golden_apples, total_powerups_collected
            FROM global_stats WHERE id = 1
        """)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_playtime': result[0],
                'total_games': result[1],
                'total_food_eaten': result[2],
                'total_golden_apples': result[3],
                'total_powerups_collected': result[4]
            }
        return {}
        
    def get_difficulty_highscore(self, difficulty: str) -> Tuple[int, Optional[str]]:
        """
        난이도별 최고 점수 가져오기
        
        Args:
            difficulty: 난이도
            
        Returns:
            (최고 점수, 달성 일시)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT highscore, achieved_at 
            FROM difficulty_highscores 
            WHERE difficulty = ?
        """, (difficulty,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1]
        return 0, None
        
    def get_mode_highscore(self, mode: str) -> Tuple[int, Optional[str]]:
        """
        모드별 최고 점수 가져오기
        
        Args:
            mode: 게임 모드
            
        Returns:
            (최고 점수, 달성 일시)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT highscore, achieved_at 
            FROM mode_highscores 
            WHERE mode = ?
        """, (mode,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1]
        return 0, None
        
    def get_longest_survival_time(self) -> Tuple[float, Optional[str]]:
        """
        최장 생존 시간 가져오기
        
        Returns:
            (생존 시간, 달성 일시)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT survival_time, achieved_at 
            FROM survival_records 
            ORDER BY survival_time DESC 
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1]
        return 0.0, None
        
    def reset_stats(self) -> None:
        """모든 통계 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM global_stats")
        cursor.execute("INSERT INTO global_stats (id) VALUES (1)")
        cursor.execute("DELETE FROM difficulty_highscores")
        cursor.execute("DELETE FROM mode_highscores")
        cursor.execute("DELETE FROM survival_records")
        
        conn.commit()
        conn.close()
