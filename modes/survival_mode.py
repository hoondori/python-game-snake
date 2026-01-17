"""Survival 모드 - 생존"""
import time
import pygame
from modes.base_mode import BaseMode
from typing import Tuple, Optional
from constants import (
    WHITE, YELLOW, RED, SURVIVAL_OBSTACLE_INTERVAL,
    SURVIVAL_MAX_OBSTACLES
)


class SurvivalMode(BaseMode):
    """생존 모드 - 시간이 지날수록 장애물이 추가됨"""
    
    def __init__(self):
        """Survival 모드 초기화"""
        super().__init__(
            name="Survival",
            description="장애물이 계속 추가됩니다. 최대한 오래 생존하세요!"
        )
        self.start_time: Optional[float] = None
        self.last_obstacle_time: Optional[float] = None
        self.obstacle_interval = SURVIVAL_OBSTACLE_INTERVAL
        self.max_obstacles = SURVIVAL_MAX_OBSTACLES
        self.initial_obstacle_count = 0
        
    def setup(self, game) -> None:
        """
        Survival 모드 설정
        
        Args:
            game: 게임 인스턴스
        """
        self.start_time = time.time()
        self.last_obstacle_time = time.time()
        self.initial_obstacle_count = len(game.obstacles) if hasattr(game, 'obstacles') else 0
        
    def update(self, game) -> None:
        """
        Survival 모드 업데이트
        
        Args:
            game: 게임 인스턴스
        """
        if not hasattr(game, 'obstacles'):
            return
            
        current_time = time.time()
        
        # 10초마다 장애물 추가
        if (self.last_obstacle_time is not None and 
            current_time - self.last_obstacle_time >= self.obstacle_interval):
            
            # 최대 개수 확인
            if len(game.obstacles) < self.max_obstacles:
                self._add_obstacle(game)
                self.last_obstacle_time = current_time
                
    def _add_obstacle(self, game) -> None:
        """
        새로운 장애물 추가
        
        Args:
            game: 게임 인스턴스
        """
        import random
        from constants import GRID_WIDTH, GRID_HEIGHT
        from core.obstacle import Obstacle
        
        # 빈 위치 찾기
        occupied = set(game.snake.body)
        occupied.add(game.food.position)
        
        # 기존 장애물 위치 추가
        for obs in game.obstacles:
            occupied.add(obs.position)
            
        # 파워업 위치 추가
        if hasattr(game, 'powerup_manager') and game.powerup_manager.spawn_position:
            occupied.add(game.powerup_manager.spawn_position)
            
        available = []
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x, y) not in occupied:
                    available.append((x, y))
                    
        if available:
            pos = random.choice(available)
            game.obstacles.append(Obstacle(pos))
            
    def check_game_over(self, game) -> Tuple[bool, Optional[str]]:
        """
        Survival 모드 게임 오버 조건 확인
        
        Args:
            game: 게임 인스턴스
            
        Returns:
            (게임 오버 여부, 메시지)
        """
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
        Survival 모드 HUD 그리기
        
        Args:
            surface: 그릴 화면
            game: 게임 인스턴스
        """
        font = pygame.font.Font(None, 24)
        large_font = pygame.font.Font(None, 36)
        
        # 생존 시간
        if self.start_time is not None:
            survival_time = time.time() - self.start_time
            time_text = large_font.render(f"Time: {int(survival_time)}s", True, YELLOW)
            surface.blit(time_text, (10, 5))
            
        # 장애물 수
        if hasattr(game, 'obstacles'):
            obstacle_count = len(game.obstacles)
            color = RED if obstacle_count >= self.max_obstacles * 0.8 else WHITE
            obstacles_text = font.render(f"Obstacles: {obstacle_count}/{self.max_obstacles}", 
                                        True, color)
            surface.blit(obstacles_text, (250, 10))
            
        # 점수
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        surface.blit(score_text, (480, 10))
        
    def get_survival_time(self) -> float:
        """생존 시간 반환"""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
        
    def get_score_multiplier(self) -> float:
        """Survival 모드 점수 배율"""
        return 1.2  # 1.2배 점수
