"""시각 효과 및 파티클 시스템"""
import pygame
import random
import math
from typing import Tuple, List
from constants import PARTICLE_LIFETIME, PARTICLE_COUNT, GRID_SIZE


class Particle:
    """단일 파티클 클래스"""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 velocity: Tuple[float, float], lifetime: int = PARTICLE_LIFETIME):
        """
        파티클 초기화
        
        Args:
            x, y: 초기 위치
            color: 파티클 색상
            velocity: 속도 (vx, vy)
            lifetime: 생존 시간 (프레임)
        """
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
        
    def update(self) -> bool:
        """
        파티클 업데이트
        
        Returns:
            파티클이 살아있으면 True, 죽으면 False
        """
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        # 중력 효과
        self.vy += 0.2
        
        # 속도 감소 (마찰)
        self.vx *= 0.98
        self.vy *= 0.98
        
        return self.lifetime > 0
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        파티클 그리기
        
        Args:
            surface: 그릴 화면
        """
        # 생존 시간에 따라 투명도 조정
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        
        # 현재 크기 (시간에 따라 감소)
        current_size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        
        # 원 그리기
        try:
            temp_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color_with_alpha, 
                             (current_size, current_size), current_size)
            surface.blit(temp_surface, (int(self.x - current_size), int(self.y - current_size)))
        except:
            # 화면 밖으로 나간 경우 무시
            pass


class ParticleSystem:
    """파티클 시스템 관리 클래스"""
    
    def __init__(self):
        """파티클 시스템 초기화"""
        self.particles: List[Particle] = []
        
    def create_explosion(self, position: Tuple[int, int], color: Tuple[int, int, int], 
                        count: int = PARTICLE_COUNT) -> None:
        """
        폭발 효과 생성
        
        Args:
            position: 폭발 위치 (그리드 좌표)
            color: 파티클 색상
            count: 파티클 수
        """
        x, y = position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        for _ in range(count):
            # 랜덤한 방향과 속도
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # 색상 변형
            color_variation = tuple(
                max(0, min(255, c + random.randint(-30, 30))) for c in color
            )
            
            particle = Particle(center_x, center_y, color_variation, (vx, vy))
            self.particles.append(particle)
            
    def create_glow(self, position: Tuple[int, int], color: Tuple[int, int, int],
                    count: int = 5) -> None:
        """
        빛나는 효과 생성
        
        Args:
            position: 위치 (그리드 좌표)
            color: 파티클 색상
            count: 파티클 수
        """
        x, y = position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        for _ in range(count):
            # 느린 속도로 위로 떠오름
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-2, -0.5)
            
            # 밝은 색상
            bright_color = tuple(min(255, c + 50) for c in color)
            
            particle = Particle(center_x, center_y, bright_color, (vx, vy), 
                              lifetime=PARTICLE_LIFETIME * 2)
            self.particles.append(particle)
            
    def create_trail(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        꼬리 효과 생성 (이동 시 자취)
        
        Args:
            position: 위치 (그리드 좌표)
            color: 파티클 색상
        """
        x, y = position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # 작은 파티클 1-2개
        for _ in range(random.randint(1, 2)):
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-0.5, 0.5)
            
            particle = Particle(center_x, center_y, color, (vx, vy), 
                              lifetime=PARTICLE_LIFETIME // 2)
            self.particles.append(particle)
            
    def create_sparkle(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        반짝임 효과 생성 (Golden Apple 등)
        
        Args:
            position: 위치 (그리드 좌표)
            color: 파티클 색상
        """
        x, y = position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # 작은 파티클들이 사방으로
        for _ in range(3):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 1.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # 노란색/흰색 계열
            sparkle_color = (255, 255, random.randint(200, 255))
            
            particle = Particle(center_x, center_y, sparkle_color, (vx, vy),
                              lifetime=PARTICLE_LIFETIME // 3)
            self.particles.append(particle)
            
    def update(self) -> None:
        """모든 파티클 업데이트"""
        # 살아있는 파티클만 유지
        self.particles = [p for p in self.particles if p.update()]
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        모든 파티클 그리기
        
        Args:
            surface: 그릴 화면
        """
        for particle in self.particles:
            particle.draw(surface)
            
    def clear(self) -> None:
        """모든 파티클 제거"""
        self.particles.clear()
        
    def get_particle_count(self) -> int:
        """현재 파티클 수 반환"""
        return len(self.particles)


class AnimationEffect:
    """애니메이션 효과 클래스"""
    
    @staticmethod
    def pulse(frame: int, period: int = 30, min_scale: float = 0.8, 
             max_scale: float = 1.2) -> float:
        """
        펄스 애니메이션 (크기 변화)
        
        Args:
            frame: 현재 프레임
            period: 주기 (프레임)
            min_scale: 최소 크기 배율
            max_scale: 최대 크기 배율
            
        Returns:
            현재 크기 배율
        """
        progress = (frame % period) / period
        scale = min_scale + (max_scale - min_scale) * (0.5 + 0.5 * math.sin(2 * math.pi * progress))
        return scale
        
    @staticmethod
    def blink(frame: int, period: int = 15) -> bool:
        """
        깜빡임 애니메이션
        
        Args:
            frame: 현재 프레임
            period: 주기 (프레임)
            
        Returns:
            현재 표시 여부
        """
        return (frame % period) < (period // 2)
        
    @staticmethod
    def rotate(frame: int, speed: float = 2.0) -> float:
        """
        회전 애니메이션
        
        Args:
            frame: 현재 프레임
            speed: 회전 속도
            
        Returns:
            현재 각도 (도)
        """
        return (frame * speed) % 360
        
    @staticmethod
    def fade_in(frame: int, duration: int = 30) -> float:
        """
        페이드 인 애니메이션
        
        Args:
            frame: 현재 프레임
            duration: 지속 시간 (프레임)
            
        Returns:
            투명도 (0.0 ~ 1.0)
        """
        return min(1.0, frame / duration)
        
    @staticmethod
    def fade_out(frame: int, duration: int = 30) -> float:
        """
        페이드 아웃 애니메이션
        
        Args:
            frame: 현재 프레임
            duration: 지속 시간 (프레임)
            
        Returns:
            투명도 (0.0 ~ 1.0)
        """
        return max(0.0, 1.0 - frame / duration)
