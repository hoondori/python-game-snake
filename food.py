"""먹이(Food) 클래스"""
import random
from constants import *


class Food:
    def __init__(self):
        """먹이 초기화"""
        self.position = None
        self.spawn()
    
    def spawn(self, snake_body=None):
        """랜덤 위치에 먹이 생성 (뱀과 겹치지 않게)"""
        if snake_body is None:
            snake_body = []
        
        while True:
            # 랜덤 위치 생성
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)
            
            # 뱀과 겹치지 않으면 해당 위치에 생성
            if position not in snake_body:
                self.position = position
                break
    
    def get_position(self):
        """먹이 위치 반환"""
        return self.position
