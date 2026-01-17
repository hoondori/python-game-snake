"""파워업 아이템 클래스"""
import pygame
import time
import random
from typing import Tuple, Optional
from constants import (
    POWERUP_SPEED_BOOST, POWERUP_SLOW_MOTION, POWERUP_INVINCIBLE,
    POWERUP_COLORS, POWERUP_PROBABILITY, POWERUP_DURATION,
    POWERUP_SCORE, POWERUP_EFFECTS, GRID_SIZE
)


class PowerUp:
    """파워업 아이템을 나타내는 클래스"""
    
    def __init__(self, powerup_type: str, position: Tuple[int, int]):
        """
        파워업 초기화
        
        Args:
            powerup_type: 파워업 종류 (speed_boost, slow_motion, invincible)
            position: 위치 (x, y)
        """
        self.type = powerup_type
        self.position = position
        self.color = POWERUP_COLORS[powerup_type]
        self.score = POWERUP_SCORE[powerup_type]
        self.duration = POWERUP_DURATION
        self.active = False
        self.start_time: Optional[float] = None
        self.animation_frame = 0
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        파워업을 화면에 그리기
        
        Args:
            surface: 그릴 화면
        """
        x, y = self.position
        pixel_x = x * GRID_SIZE
        pixel_y = y * GRID_SIZE
        
        # 회전 애니메이션을 위한 프레임 증가
        self.animation_frame += 1
        
        # 중심점
        center_x = pixel_x + GRID_SIZE // 2
        center_y = pixel_y + GRID_SIZE // 2
        
        # 종류별 모양 그리기
        if self.type == POWERUP_SPEED_BOOST:
            # 번개 모양 (삼각형)
            points = [
                (center_x, center_y - GRID_SIZE // 2 + 2),
                (center_x + GRID_SIZE // 4, center_y),
                (center_x, center_y + GRID_SIZE // 2 - 2),
                (center_x - GRID_SIZE // 4, center_y)
            ]
            pygame.draw.polygon(surface, self.color, points)
            
        elif self.type == POWERUP_SLOW_MOTION:
            # 시계 모양 (원과 선)
            pygame.draw.circle(surface, self.color, (center_x, center_y), GRID_SIZE // 3)
            # 시계 바늘
            angle = (self.animation_frame * 6) % 360
            end_x = center_x + int((GRID_SIZE // 4) * pygame.math.Vector2(1, 0).rotate(angle).x)
            end_y = center_y + int((GRID_SIZE // 4) * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.line(surface, (255, 255, 255), (center_x, center_y), (end_x, end_y), 2)
            
        elif self.type == POWERUP_INVINCIBLE:
            # 별 모양
            points = []
            for i in range(5):
                angle = i * 144 - 90 + (self.animation_frame * 2) % 360
                radius = GRID_SIZE // 2 - 2
                x = center_x + int(radius * pygame.math.Vector2(1, 0).rotate(angle).x)
                y = center_y + int(radius * pygame.math.Vector2(1, 0).rotate(angle).y)
                points.append((x, y))
            pygame.draw.polygon(surface, self.color, points)
            
    def activate(self) -> None:
        """파워업 활성화"""
        self.active = True
        self.start_time = time.time()
        
    def is_active(self) -> bool:
        """파워업이 활성 상태인지 확인"""
        if not self.active or self.start_time is None:
            return False
        return time.time() - self.start_time < self.duration
        
    def get_remaining_time(self) -> float:
        """남은 시간 반환"""
        if not self.active or self.start_time is None:
            return 0.0
        remaining = self.duration - (time.time() - self.start_time)
        return max(0.0, remaining)
        
    def expire(self) -> None:
        """파워업 효과 종료"""
        self.active = False
        self.start_time = None
        
    @staticmethod
    def should_spawn() -> Optional[str]:
        """
        파워업을 생성할지 결정하고, 생성할 경우 종류 반환
        
        Returns:
            생성할 파워업 종류 또는 None
        """
        rand = random.random()
        cumulative = 0.0
        
        for powerup_type, probability in POWERUP_PROBABILITY.items():
            cumulative += probability
            if rand < cumulative:
                return powerup_type
                
        return None
        
    def get_effect_multiplier(self) -> float:
        """
        파워업의 효과 배율 반환 (속도 관련)
        
        Returns:
            속도 배율
        """
        if self.type in POWERUP_EFFECTS:
            return POWERUP_EFFECTS[self.type]
        return 1.0


class PowerUpManager:
    """파워업 관리 클래스"""
    
    def __init__(self):
        """파워업 매니저 초기화"""
        self.active_powerups = {}  # {type: PowerUp}
        self.spawn_position: Optional[Tuple[int, int]] = None
        self.spawned_powerup: Optional[PowerUp] = None
        
    def try_spawn(self, occupied_positions: list) -> Optional[PowerUp]:
        """
        파워업 생성 시도
        
        Args:
            occupied_positions: 이미 차지된 위치들 (뱀, 먹이, 장애물 등)
            
        Returns:
            생성된 파워업 또는 None
        """
        powerup_type = PowerUp.should_spawn()
        if powerup_type is None:
            return None
            
        # 빈 위치 찾기
        from constants import GRID_WIDTH, GRID_HEIGHT
        available_positions = []
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x, y) not in occupied_positions:
                    available_positions.append((x, y))
                    
        if not available_positions:
            return None
            
        position = random.choice(available_positions)
        powerup = PowerUp(powerup_type, position)
        self.spawned_powerup = powerup
        self.spawn_position = position
        return powerup
        
    def collect(self, powerup: PowerUp) -> int:
        """
        파워업 수집
        
        Args:
            powerup: 수집할 파워업
            
        Returns:
            획득 점수
        """
        powerup.activate()
        self.active_powerups[powerup.type] = powerup
        self.spawned_powerup = None
        self.spawn_position = None
        return powerup.score
        
    def update(self) -> None:
        """활성 파워업 상태 업데이트"""
        expired = []
        for powerup_type, powerup in self.active_powerups.items():
            if not powerup.is_active():
                expired.append(powerup_type)
                
        for powerup_type in expired:
            self.active_powerups[powerup_type].expire()
            del self.active_powerups[powerup_type]
            
    def is_invincible(self) -> bool:
        """무적 상태인지 확인"""
        return POWERUP_INVINCIBLE in self.active_powerups
        
    def get_speed_multiplier(self) -> float:
        """현재 속도 배율 반환"""
        multiplier = 1.0
        
        if POWERUP_SPEED_BOOST in self.active_powerups:
            multiplier *= POWERUP_EFFECTS[POWERUP_SPEED_BOOST]
        if POWERUP_SLOW_MOTION in self.active_powerups:
            multiplier *= POWERUP_EFFECTS[POWERUP_SLOW_MOTION]
            
        return multiplier
        
    def get_active_powerups(self) -> dict:
        """활성 파워업 목록 반환"""
        return self.active_powerups.copy()
        
    def clear(self) -> None:
        """모든 파워업 제거"""
        self.active_powerups.clear()
        self.spawned_powerup = None
        self.spawn_position = None
