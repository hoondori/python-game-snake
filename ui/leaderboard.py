"""리더보드 UI"""
import pygame
import json
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, 
    YELLOW, GREEN, GRAY, DARK_GRAY
)


class LeaderboardEntry:
    """리더보드 항목 클래스"""
    
    def __init__(self, name: str, score: int, difficulty: str, 
                 mode: str, date: str):
        """
        리더보드 항목 초기화
        
        Args:
            name: 플레이어 이름
            score: 점수
            difficulty: 난이도
            mode: 게임 모드
            date: 날짜
        """
        self.name = name
        self.score = score
        self.difficulty = difficulty
        self.mode = mode
        self.date = date
        
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'name': self.name,
            'score': self.score,
            'difficulty': self.difficulty,
            'mode': self.mode,
            'date': self.date
        }
        
    @staticmethod
    def from_dict(data: Dict) -> 'LeaderboardEntry':
        """딕셔너리에서 생성"""
        return LeaderboardEntry(
            data['name'],
            data['score'],
            data['difficulty'],
            data['mode'],
            data['date']
        )


class Leaderboard:
    """리더보드 관리 클래스"""
    
    def __init__(self, file_path: str = "data/leaderboard.json"):
        """
        리더보드 초기화
        
        Args:
            file_path: 리더보드 데이터 파일 경로
        """
        self.file_path = file_path
        self.entries: List[LeaderboardEntry] = []
        self._ensure_directory()
        self._load()
        
    def _ensure_directory(self) -> None:
        """데이터 디렉토리 생성"""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
    def _load(self) -> None:
        """리더보드 데이터 로드"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = [LeaderboardEntry.from_dict(e) 
                                  for e in data.get('entries', [])]
            except (json.JSONDecodeError, IOError):
                self.entries = []
        else:
            self.entries = []
            self._save()
            
    def _save(self) -> None:
        """리더보드 데이터 저장"""
        data = {
            'entries': [e.to_dict() for e in self.entries]
        }
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def add_score(self, name: str, score: int, difficulty: str, mode: str) -> int:
        """
        점수 추가
        
        Args:
            name: 플레이어 이름
            score: 점수
            difficulty: 난이도
            mode: 게임 모드
            
        Returns:
            순위 (1부터 시작, 순위권 밖이면 -1)
        """
        entry = LeaderboardEntry(
            name, score, difficulty, mode,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self.entries.append(entry)
        
        # 점수순 정렬
        self.entries.sort(key=lambda e: e.score, reverse=True)
        
        # 상위 100개만 유지
        self.entries = self.entries[:100]
        
        self._save()
        
        # 순위 찾기
        for i, e in enumerate(self.entries):
            if e.name == name and e.score == score and e.date == entry.date:
                return i + 1
                
        return -1
        
    def get_top_scores(self, difficulty: Optional[str] = None, 
                      mode: Optional[str] = None, limit: int = 10) -> List[LeaderboardEntry]:
        """
        상위 점수 가져오기
        
        Args:
            difficulty: 난이도 필터 (None이면 전체)
            mode: 모드 필터 (None이면 전체)
            limit: 최대 개수
            
        Returns:
            상위 점수 리스트
        """
        filtered = self.entries
        
        if difficulty:
            filtered = [e for e in filtered if e.difficulty == difficulty]
        if mode:
            filtered = [e for e in filtered if e.mode == mode]
            
        return filtered[:limit]
        
    def is_high_score(self, score: int, difficulty: Optional[str] = None,
                     mode: Optional[str] = None) -> bool:
        """
        최고 점수인지 확인
        
        Args:
            score: 점수
            difficulty: 난이도
            mode: 모드
            
        Returns:
            최고 점수 여부
        """
        top_scores = self.get_top_scores(difficulty, mode, limit=10)
        
        if len(top_scores) < 10:
            return True
            
        return score > top_scores[-1].score
        
    def clear(self) -> None:
        """리더보드 초기화"""
        self.entries.clear()
        self._save()


class LeaderboardUI:
    """리더보드 UI 클래스"""
    
    def __init__(self, leaderboard: Leaderboard):
        """
        리더보드 UI 초기화
        
        Args:
            leaderboard: 리더보드 인스턴스
        """
        self.leaderboard = leaderboard
        self.filter_difficulty: Optional[str] = None
        self.filter_mode: Optional[str] = None
        self.current_entry_index = -1
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        리더보드 그리기
        
        Args:
            surface: 그릴 화면
        """
        # 배경
        surface.fill(BLACK)
        
        # 타이틀
        title_font = pygame.font.Font(None, 56)
        title_text = title_font.render("HIGH SCORES", True, YELLOW)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        surface.blit(title_text, title_rect)
        
        # 필터 정보
        filter_font = pygame.font.Font(None, 28)
        filter_text = f"Difficulty: {self.filter_difficulty or 'All'}  |  Mode: {self.filter_mode or 'All'}"
        filter_render = filter_font.render(filter_text, True, GRAY)
        filter_rect = filter_render.get_rect(center=(WINDOW_WIDTH // 2, 100))
        surface.blit(filter_render, filter_rect)
        
        # 상위 10개 가져오기
        top_scores = self.leaderboard.get_top_scores(
            self.filter_difficulty, self.filter_mode, limit=10
        )
        
        if not top_scores:
            # 점수 없음
            no_scores_font = pygame.font.Font(None, 36)
            no_scores_text = no_scores_font.render("No scores yet!", True, GRAY)
            no_scores_rect = no_scores_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
            surface.blit(no_scores_text, no_scores_rect)
        else:
            # 테이블 헤더
            header_font = pygame.font.Font(None, 28)
            header_y = 150
            
            rank_x = 80
            name_x = 180
            score_x = 320
            diff_x = 420
            mode_x = 520
            
            # 헤더
            headers = [
                ("Rank", rank_x),
                ("Name", name_x),
                ("Score", score_x),
                ("Diff", diff_x),
                ("Mode", mode_x)
            ]
            
            for header, x in headers:
                header_text = header_font.render(header, True, YELLOW)
                surface.blit(header_text, (x, header_y))
                
            # 구분선
            pygame.draw.line(surface, GRAY, 
                           (50, header_y + 30), 
                           (WINDOW_WIDTH - 50, header_y + 30), 2)
            
            # 항목들
            item_font = pygame.font.Font(None, 24)
            start_y = header_y + 50
            item_spacing = 40
            
            for i, entry in enumerate(top_scores):
                y = start_y + i * item_spacing
                
                # 현재 플레이어 하이라이트
                is_current = (i == self.current_entry_index)
                color = GREEN if is_current else WHITE
                
                if is_current:
                    # 배경 박스
                    box_rect = pygame.Rect(50, y - 5, WINDOW_WIDTH - 100, 35)
                    pygame.draw.rect(surface, DARK_GRAY, box_rect)
                    pygame.draw.rect(surface, GREEN, box_rect, 2)
                
                # 순위
                rank_text = item_font.render(f"#{i + 1}", True, color)
                surface.blit(rank_text, (rank_x, y))
                
                # 이름
                name_text = item_font.render(entry.name[:10], True, color)
                surface.blit(name_text, (name_x, y))
                
                # 점수
                score_text = item_font.render(str(entry.score), True, color)
                surface.blit(score_text, (score_x, y))
                
                # 난이도
                diff_text = item_font.render(entry.difficulty[:6], True, color)
                surface.blit(diff_text, (diff_x, y))
                
                # 모드
                mode_text = item_font.render(entry.mode[:8], True, color)
                surface.blit(mode_text, (mode_x, y))
        
        # 하단 안내
        hint_font = pygame.font.Font(None, 24)
        hint_text = "Press ESC to return"
        hint_render = hint_font.render(hint_text, True, GRAY)
        hint_rect = hint_render.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        surface.blit(hint_render, hint_rect)
        
    def set_filter(self, difficulty: Optional[str] = None, 
                  mode: Optional[str] = None) -> None:
        """필터 설정"""
        self.filter_difficulty = difficulty
        self.filter_mode = mode
        
    def highlight_entry(self, name: str, score: int) -> None:
        """특정 항목 하이라이트"""
        top_scores = self.leaderboard.get_top_scores(
            self.filter_difficulty, self.filter_mode, limit=10
        )
        
        for i, entry in enumerate(top_scores):
            if entry.name == name and entry.score == score:
                self.current_entry_index = i
                return
                
        self.current_entry_index = -1
