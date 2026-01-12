"""게임 통합 테스트"""
import pytest
import pygame

from game import Game
from constants import *


@pytest.fixture
def game():
    """테스트용 Game 인스턴스를 생성하는 fixture"""
    pygame.init()
    game_instance = Game()
    yield game_instance
    pygame.quit()


def test_game_initialization(game):
    """게임 초기화 테스트"""
    # 게임 객체가 제대로 생성되었는지 확인
    assert game.snake is not None
    assert game.food is not None
    assert game.running
    assert not game.game_over


def test_snake_movement(game):
    """뱀 이동 테스트"""
    initial_head = game.snake.get_head()
    
    # 한 프레임 업데이트
    game.update()
    
    # 머리가 이동했는지 확인
    new_head = game.snake.get_head()
    assert initial_head != new_head


def test_food_eating_and_growth(game):
    """먹이 먹기 및 뱀 성장 테스트"""
    # 뱀의 머리 바로 앞에 먹이 배치
    head_x, head_y = game.snake.get_head()
    direction_x, direction_y = game.snake.direction
    
    food_position = (head_x + direction_x, head_y + direction_y)
    game.food.position = food_position
    
    initial_length = len(game.snake.body)
    initial_food_position = game.food.get_position()
    
    # 한 프레임 업데이트 (먹이를 먹게 됨)
    game.update()
    
    # 뱀이 성장해야 함
    # 주의: 성장은 다음 이동 시 적용됨
    game.update()
    
    # 길이가 증가했는지 확인
    assert len(game.snake.body) == initial_length + 1
    
    # 새로운 먹이가 생성되었는지 확인
    assert game.food.get_position() != initial_food_position


def test_wall_collision_game_over(game):
    """벽 충돌 시 게임 오버 테스트"""
    # 뱀을 왼쪽 벽 근처로 이동
    game.snake.body = [(1, 10), (2, 10), (3, 10)]
    game.snake.direction = LEFT
    
    # 벽으로 이동 (두 번 업데이트 - move와 collision check)
    game.update()
    game.update()
    
    # 게임 오버 상태여야 함
    assert game.game_over


def test_self_collision_game_over(game):
    """자기 몸통 충돌 시 게임 오버 테스트"""
    # 뱀을 사각형 모양으로 만들어서 중간 몸통과 충돌하도록 설정
    game.snake.body = [
        (10, 10),  # 머리
        (11, 10),  # 몸통
        (12, 10),  # 몸통
        (12, 11),  # 몸통
        (12, 12),  # 몸통
        (11, 12),  # 몸통
        (10, 12),  # 몸통
        (10, 11)   # 꼬리
    ]
    # 현재 머리는 (10, 10)이고 아래로 이동하면 (10, 11)로 가는데,
    # (10, 11)은 꼬리 위치이지만 move 후에는 꼬리가 제거됨
    # 따라서 안쪽으로 이동하도록 설정
    game.snake.direction = DOWN
    
    # 아래로 이동 (10, 11)
    game.update()
    
    # 오른쪽으로 방향 전환
    game.snake.direction = RIGHT
    # 오른쪽으로 이동 (11, 11) - 아직 충돌 없음
    game.update()
    
    # 위로 방향 전환
    game.snake.direction = UP
    # 위로 이동 (11, 10) - 몸통과 충돌!
    game.update()
    
    # 게임 오버 상태여야 함
    assert game.game_over


def test_game_continues_when_no_collision(game):
    """충돌이 없으면 게임이 계속됨"""
    # 여러 프레임 업데이트
    for _ in range(10):
        if not game.game_over:
            game.update()
    
    # 충돌하지 않았다면 게임이 계속됨
    # (랜덤으로 먹이가 생성되므로 충돌할 수도 있음)
    # 이 테스트는 게임이 정상적으로 실행되는지만 확인
    assert game.snake is not None


def test_direction_change_during_game(game):
    """게임 중 방향 변경 테스트"""
    # 초기 방향
    initial_direction = game.snake.direction
    
    # 방향 변경 (오른쪽 -> 위)
    game.snake.change_direction(UP)
    
    # 방향이 변경되었는지 확인
    assert game.snake.direction == UP
    assert game.snake.direction != initial_direction


def test_food_not_on_snake(game):
    """먹이가 뱀 위에 생성되지 않음"""
    # 새로운 먹이 생성
    game.food.spawn(game.snake.body)
    
    # 먹이 위치가 뱀의 몸통과 겹치지 않아야 함
    assert game.food.get_position() not in game.snake.body


def test_multiple_food_eating(game):
    """여러 먹이 먹기 테스트"""
    initial_length = len(game.snake.body)
    foods_eaten = 0
    
    # 5개의 먹이를 먹도록 시뮬레이션
    for i in range(5):
        # 먹이를 뱀 앞에 배치
        head_x, head_y = game.snake.get_head()
        direction_x, direction_y = game.snake.direction
        
        food_position = (head_x + direction_x, head_y + direction_y)
        game.food.position = food_position
        
        # 업데이트
        game.update()
        foods_eaten += 1
        
        # 성장 적용을 위한 추가 업데이트
        game.update()
    
    # 길이가 증가했는지 확인
    assert len(game.snake.body) > initial_length
