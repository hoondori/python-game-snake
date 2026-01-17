"""뱀(Snake) 클래스"""
from constants import *


class Snake:
    def __init__(self):
        """뱀 초기화: 화면 중앙에 길이 3으로 시작"""
        # 화면 중앙 위치
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        
        # 뱀의 몸통 (머리부터 꼬리까지)
        self.body = [
            (center_x, center_y),      # 머리
            (center_x - 1, center_y),  # 몸통
            (center_x - 2, center_y)   # 꼬리
        ]
        
        # 초기 방향: 오른쪽
        self.direction = RIGHT
        self.growing = False  # 성장 여부
    
    def change_direction(self, new_direction):
        """방향 변경 (반대 방향으로는 변경 불가)"""
        # 현재 방향의 반대 방향인지 확인
        opposite = (self.direction[0] * -1, self.direction[1] * -1)
        
        # 반대 방향이 아니면 방향 변경
        if new_direction != opposite:
            self.direction = new_direction
    
    def move(self, portal_mode=False):
        """
        뱀을 현재 방향으로 이동
        
        Args:
            portal_mode: Portal 모드 활성화 여부
        """
        # 현재 머리 위치
        head_x, head_y = self.body[0]
        
        # 새로운 머리 위치 계산
        new_head_x = head_x + self.direction[0]
        new_head_y = head_y + self.direction[1]
        
        # Portal 모드: 벽을 넘으면 반대편으로
        if portal_mode:
            new_head_x = new_head_x % GRID_WIDTH
            new_head_y = new_head_y % GRID_HEIGHT
        
        new_head = (new_head_x, new_head_y)
        
        # 새 머리를 몸통 앞에 추가
        self.body.insert(0, new_head)
        
        # 성장 중이 아니면 꼬리 제거
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
    
    def grow(self):
        """뱀 성장"""
        self.growing = True
    
    def check_wall_collision(self):
        """벽 충돌 확인"""
        head_x, head_y = self.body[0]
        
        if head_x < 0 or head_x >= GRID_WIDTH:
            return True
        if head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        
        return False
    
    def check_self_collision(self):
        """자기 몸통 충돌 확인"""
        head = self.body[0]
        
        # 머리가 몸통의 나머지 부분과 충돌하는지 확인
        return head in self.body[1:]
    
    def get_head(self):
        """머리 위치 반환"""
        return self.body[0]
