"""Time Attack 모드 - 시간 제한"""
import time
import pygame
from modes.base_mode import BaseMode
from typing import Tuple, Optional
from constants import (
    WHITE, RED, YELLOW, TIME_ATTACK_DURATION, 
    TIME_ATTACK_BONUS_TIME
)


class TimeAttackMode(BaseMode):
    """시간 제한 모드 - 60초 내에 최대한 많은 점수 획득"""
    
    def __init__(self):
        """Time Attack 모드 초기화"""
        super().__init__(
            name="Time Attack",
            description="60초 내에 최대한 많은 점수를 획득하세요!"
        )
        self.start_time: Optional[float] = None
        self.duration = TIME_ATTACK_DURATION
        self.bonus_time = TIME_ATTACK_BONUS_TIME
        self.time_bonus_collected = 0
        
    def setup(self, game) -> None:
        """
        Time Attack 모드 설정
        
        Args:
            game: 게임 인스턴스
        """
        self.start_time = time.time()
        self.time_bonus_collected = 0
        
    def update(self, game) -> None:
        """
        Time Attack 모드 업데이트
        
        Args:
            game: 게임 인스턴스
        """
        # 시간 체크는 check_game_over에서 수행
        pass
        
    def check_game_over(self, game) -> Tuple[bool, Optional[str]]:
        """
        Time Attack 모드 게임 오버 조건 확인
        
        Args:
            game: 게임 인스턴스
            
        Returns:
            (게임 오버 여부, 메시지)
        """
        # 일반적인 충돌 체크
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
        
        # 시간 초과 체크
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            if elapsed >= self.duration:
                return True, "Time's Up!"
                
        return False, None
        
    def draw_hud(self, surface: pygame.Surface, game) -> None:
        """
        Time Attack 모드 HUD 그리기
        
        Args:
            surface: 그릴 화면
            game: 게임 인스턴스
        """
        font = pygame.font.Font(None, 24)
        large_font = pygame.font.Font(None, 36)
        
        # 점수
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        
        # 남은 시간
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            remaining = max(0, self.duration - elapsed)
            
            # 10초 이하일 때 빨간색
            color = RED if remaining <= 10 else WHITE
            
            # 10초 이하일 때 깜빡임
            if remaining <= 10:
                if int(remaining * 2) % 2 == 0:
                    color = RED
                else:
                    color = WHITE
                    
            time_text = large_font.render(f"Time: {int(remaining)}s", True, color)
            surface.blit(time_text, (200, 5))
            
        # 시간 보너스 획득 횟수
        if self.time_bonus_collected > 0:
            bonus_text = font.render(f"Time Bonuses: {self.time_bonus_collected}", True, YELLOW)
            surface.blit(bonus_text, (450, 10))
            
    def add_time_bonus(self) -> None:
        """시간 보너스 추가"""
        self.duration += self.bonus_time
        self.time_bonus_collected += 1
        
    def get_remaining_time(self) -> float:
        """남은 시간 반환"""
        if self.start_time is None:
            return self.duration
        elapsed = time.time() - self.start_time
        return max(0, self.duration - elapsed)
        
    def get_score_multiplier(self) -> float:
        """Time Attack 모드 점수 배율"""
        return 1.5  # 1.5배 점수
