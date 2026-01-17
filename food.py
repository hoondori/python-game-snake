"""먹이(Food) 클래스"""
import random
import time
from constants import *


class Food:
    def __init__(self):
        """먹이 초기화"""
        self.position = None
        self.is_golden = False
        self.spawn_time = time.time()
        self.spawn()
    
    def spawn(self, snake_body=None, obstacle_positions=None):
        """
        랜덤 위치에 먹이 생성 (뱀/장애물과 겹치지 않게)
        
        Args:
            snake_body: 뱀의 몸통 위치 리스트
            obstacle_positions: 장애물 위치 리스트
        """
        if snake_body is None:
            snake_body = []
        if obstacle_positions is None:
            obstacle_positions = []
        
        occupied = set(snake_body + obstacle_positions)
        
        while True:
            # 랜덤 위치 생성
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)
            
            # 뱀/장애물과 겹치지 않으면 해당 위치에 생성
            if position not in occupied:
                self.position = position
                break
        
        # 10% 확률로 Golden Apple 생성
        self.is_golden = random.random() < GOLDEN_APPLE_PROBABILITY
        self.spawn_time = time.time()
    
    def get_position(self):
        """먹이 위치 반환"""
        return self.position
    
    def get_value(self):
        """먹이 점수 반환"""
        return GOLDEN_APPLE_SCORE if self.is_golden else NORMAL_FOOD_SCORE
    
    def should_respawn(self):
        """
        Golden Apple이 10초 경과했는지 확인
        
        Returns:
            bool: 재생성이 필요하면 True
        """
        if self.is_golden:
            elapsed = time.time() - self.spawn_time
            return elapsed >= GOLDEN_APPLE_TIMEOUT
        return False
