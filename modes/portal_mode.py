"""Portal 모드"""
from modes.base_mode import BaseMode
from typing import Tuple, Optional
import pygame
from constants import WHITE, YELLOW


class PortalMode(BaseMode):
    """포탈 모드 - 벽을 통과하면 반대편으로 이동"""
    
    def __init__(self):
        """Portal 모드 초기화"""
        super().__init__(
            name="Portal",
            description="벽을 통과하면 반대편으로 나옵니다!"
        )
        
    def setup(self, game) -> None:
        """
        Portal 모드 설정
        
        Args:
            game: 게임 인스턴스
        """
        # 특별한 설정 없음
        pass
        
    def update(self, game) -> None:
        """
        Portal 모드 업데이트
        
        Args:
            game: 게임 인스턴스
        """
        # 뱀 머리가 벽을 벗어나면 반대편으로 이동
        from constants import GRID_WIDTH, GRID_HEIGHT
        
        head_x, head_y = game.snake.body[0]
        
        # 포탈 효과 적용
        new_x = head_x % GRID_WIDTH
        new_y = head_y % GRID_HEIGHT
        
        if (new_x, new_y) != (head_x, head_y):
            game.snake.body[0] = (new_x, new_y)
        
    def check_game_over(self, game) -> Tuple[bool, Optional[str]]:
        """
        Portal 모드 게임 오버 조건 확인
        
        Args:
            game: 게임 인스턴스
            
        Returns:
            (게임 오버 여부, 메시지)
        """
        head = game.snake.body[0]
        
        # 벽 충돌 없음 (포탈 모드)
        
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
        Portal 모드 HUD 그리기
        
        Args:
            surface: 그릴 화면
            game: 게임 인스턴스
        """
        font = pygame.font.Font(None, 24)
        
        # 점수
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # 최고 점수
        if hasattr(game, 'high_score'):
            high_score_text = font.render(f"High: {game.high_score}", True, YELLOW)
            surface.blit(high_score_text, (200, 10))
            
        # 모드 표시
        mode_text = font.render("Portal Mode", True, (100, 200, 255))
        surface.blit(mode_text, (450, 10))
        
    def get_score_multiplier(self) -> float:
        """Portal 모드 점수 배율"""
        return 1.3  # 1.3배 점수
