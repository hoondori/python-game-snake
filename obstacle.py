"""장애물 클래스"""
import random
from constants import GRID_WIDTH, GRID_HEIGHT


class Obstacle:
    def __init__(self, count, snake_body, food_pos):
        """
        장애물 초기화
        
        Args:
            count: 생성할 장애물 개수
            snake_body: 뱀의 몸통 위치 리스트
            food_pos: 먹이 위치 튜플
        """
        self.positions = []
        self.generate_positions(count, snake_body, food_pos)
    
    def generate_positions(self, count, snake_body, food_pos):
        """
        겹치지 않는 위치에 장애물 생성
        
        Args:
            count: 생성할 장애물 개수
            snake_body: 뱀의 몸통 위치 리스트
            food_pos: 먹이 위치 튜플
        """
        self.positions = []
        occupied = set(snake_body + [food_pos])
        
        max_attempts = 1000  # 무한 루프 방지
        attempts = 0
        
        while len(self.positions) < count and attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            
            if pos not in occupied and pos not in self.positions:
                self.positions.append(pos)
            
            attempts += 1
    
    def get_positions(self):
        """장애물 위치 리스트 반환"""
        return self.positions
    
    def check_collision(self, position):
        """
        특정 위치가 장애물과 충돌하는지 확인
        
        Args:
            position: 확인할 위치 (x, y)
            
        Returns:
            bool: 충돌하면 True, 아니면 False
        """
        return position in self.positions
