"""Food 클래스 단위 테스트"""
import pytest

from food import Food
from constants import *


def test_food_initialization():
    """먹이 초기화 테스트"""
    food = Food()
    
    # 위치가 할당되어야 함
    assert food.position is not None
    
    # 위치가 그리드 범위 내에 있어야 함
    x, y = food.position
    assert 0 <= x < GRID_WIDTH
    assert 0 <= y < GRID_HEIGHT


def test_random_position_generation():
    """랜덤 위치 생성 확인"""
    positions = set()
    
    # 여러 번 생성하여 랜덤성 확인
    for _ in range(100):
        food = Food()
        positions.add(food.position)
    
    # 최소한 10개 이상의 다른 위치가 생성되어야 함
    assert len(positions) > 10


def test_spawn_without_snake():
    """뱀 없이 먹이 생성"""
    food = Food()
    food.spawn()
    
    # 위치가 할당되어야 함
    assert food.position is not None
    
    # 그리드 범위 내
    x, y = food.position
    assert 0 <= x < GRID_WIDTH
    assert 0 <= y < GRID_HEIGHT


def test_spawn_avoiding_snake():
    """뱀과 겹치지 않는 위치에 생성"""
    # 뱀의 몸통 (가로로 긴 뱀)
    snake_body = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10)]
    
    food = Food()
    
    # 여러 번 생성하여 뱀과 겹치지 않는지 확인
    for _ in range(50):
        food.spawn(snake_body)
        
        # 뱀의 몸통과 겹치지 않아야 함
        assert food.position not in snake_body


def test_spawn_with_large_snake():
    """큰 뱀이 있을 때도 먹이 생성 가능"""
    # 화면의 절반을 차지하는 큰 뱀
    snake_body = []
    for i in range(GRID_WIDTH * GRID_HEIGHT // 2):
        x = i % GRID_WIDTH
        y = i // GRID_WIDTH
        snake_body.append((x, y))
    
    food = Food()
    food.spawn(snake_body)
    
    # 뱀과 겹치지 않는 위치에 생성되어야 함
    assert food.position not in snake_body


def test_get_position():
    """위치 반환 메서드 테스트"""
    food = Food()
    position = food.get_position()
    
    # 반환된 위치가 실제 위치와 같아야 함
    assert position == food.position
    
    # 튜플이어야 함
    assert isinstance(position, tuple)
    assert len(position) == 2


def test_respawn():
    """재생성 테스트"""
    food = Food()
    first_position = food.position
    
    # 재생성
    food.spawn()
    second_position = food.position
    
    # 위치가 변경될 수 있음 (랜덤이므로 항상 다르지는 않음)
    # 하지만 유효한 위치여야 함
    x, y = second_position
    assert 0 <= x < GRID_WIDTH
    assert 0 <= y < GRID_HEIGHT
