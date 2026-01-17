"""클래식 모드"""
from modes.base_mode import BaseMode
from typing import Tuple, Optional
import pygame
from constants import WHITE, YELLOW


class ClassicMode(BaseMode):
    """기본 클래식 게임 모드"""
    
    def __init__(self):
        """클래식 모드 초기화"""
        super().__init__(
            name="Classic",
            description="전통적인 뱀 게임"
        )
        
    def setup(self, game) -> None:
        """
        클래식 모드 설정
        
        Args:
            game: 게임 인스턴스
        """
        # 특별한 설정 없음 (기본 게임)
        pass
        
    def update(self, game) -> None:
        """
        클래식 모드 업데이트
        
        Args:
            game: 게임 인스턴스
        """
        # 특별한 업데이트 로직 없음
        pass
        
    def check_game_over(self, game) -> Tuple[bool, Optional[str]]:
        """
        클래식 모드 게임 오버 조건 확인
        
        Args:
            game: 게임 인스턴스
            
        Returns:
            (게임 오버 여부, 메시지)
        """
        # 벽 충돌 또는 자기 몸 충돌
        head = game.snake.body[0]
        
        # 벽 충돌
        from constants import GRID_WIDTH, GRID_HEIGHT
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True, "Wall Collision!"
            
        # 자기 몸 충돌
        if head in game.snake.body[1:]:
            return True, "Self Collision!"
            
        # 장애물 충돌
        if hasattr(game, 'obstacles'):
            for obstacle in game.obstacles:
                if head == obstacle.position:
                    return True, "Obstacle Collision!"
                    
        return False, None
        
    def draw_hud(self, surface: pygame.Surface, game) -> None:
        """
        클래식 모드 HUD 그리기
        
        Args:
            surface: 그릴 화면
            game: 게임 인스턴스
        """
        # 기본 정보만 표시
        font = pygame.font.Font(None, 24)
        
        # 점수
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # 최고 점수
        if hasattr(game, 'high_score'):
            high_score_text = font.render(f"High: {game.high_score}", True, YELLOW)
            surface.blit(high_score_text, (200, 10))
