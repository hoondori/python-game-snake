"""Snake 클래스 단위 테스트"""
import pytest

from snake import Snake
from constants import *


@pytest.fixture
def snake():
    """테스트용 Snake 인스턴스를 생성하는 fixture"""
    return Snake()


def test_initial_position_and_length(snake):
    """초기 위치 및 길이 확인"""
    # 길이가 3이어야 함
    assert len(snake.body) == 3
    
    # 화면 중앙에 위치해야 함
    center_x = GRID_WIDTH // 2
    center_y = GRID_HEIGHT // 2
    
    assert snake.body[0] == (center_x, center_y)
    assert snake.body[1] == (center_x - 1, center_y)
    assert snake.body[2] == (center_x - 2, center_y)


def test_initial_direction(snake):
    """초기 방향 확인 (오른쪽)"""
    assert snake.direction == RIGHT


def test_direction_change(snake):
    """방향 전환 테스트 (4방향)"""
    # 오른쪽 -> 위
    snake.change_direction(UP)
    assert snake.direction == UP
    
    # 위 -> 왼쪽
    snake.change_direction(LEFT)
    assert snake.direction == LEFT
    
    # 왼쪽 -> 아래
    snake.change_direction(DOWN)
    assert snake.direction == DOWN
    
    # 아래 -> 오른쪽
    snake.change_direction(RIGHT)
    assert snake.direction == RIGHT


def test_opposite_direction_ignored(snake):
    """반대 방향 입력 무시 확인"""
    # 초기 방향: 오른쪽
    assert snake.direction == RIGHT
    
    # 왼쪽으로 변경 시도 (반대 방향)
    snake.change_direction(LEFT)
    
    # 방향이 변경되지 않아야 함
    assert snake.direction == RIGHT
    
    # 위로 변경 (가능)
    snake.change_direction(UP)
    assert snake.direction == UP
    
    # 아래로 변경 시도 (반대 방향)
    snake.change_direction(DOWN)
    
    # 방향이 변경되지 않아야 함
    assert snake.direction == UP


def test_move(snake):
    """이동 후 위치 확인"""
    initial_head = snake.body[0]
    initial_length = len(snake.body)
    
    # 오른쪽으로 이동
    snake.move()
    
    # 머리가 오른쪽으로 한 칸 이동했는지 확인
    new_head = snake.body[0]
    assert new_head == (initial_head[0] + 1, initial_head[1])
    
    # 길이는 유지되어야 함 (성장하지 않음)
    assert len(snake.body) == initial_length


def test_grow(snake):
    """성장 기능 테스트"""
    initial_length = len(snake.body)
    
    # 성장 명령
    snake.grow()
    
    # 이동
    snake.move()
    
    # 길이가 1 증가해야 함
    assert len(snake.body) == initial_length + 1


def test_wall_collision_left(snake):
    """벽 충돌 감지 - 왼쪽"""
    # 뱀을 왼쪽 경계로 이동
    snake.body = [(0, 10), (1, 10), (2, 10)]
    snake.direction = LEFT
    
    # 이동
    snake.move()
    
    # 충돌 감지
    assert snake.check_wall_collision()


def test_wall_collision_right(snake):
    """벽 충돌 감지 - 오른쪽"""
    # 뱀을 오른쪽 경계로 이동
    snake.body = [(GRID_WIDTH - 1, 10), (GRID_WIDTH - 2, 10), (GRID_WIDTH - 3, 10)]
    snake.direction = RIGHT
    
    # 이동
    snake.move()
    
    # 충돌 감지
    assert snake.check_wall_collision()


def test_wall_collision_top(snake):
    """벽 충돌 감지 - 위쪽"""
    # 뱀을 위쪽 경계로 이동
    snake.body = [(10, 0), (10, 1), (10, 2)]
    snake.direction = UP
    
    # 이동
    snake.move()
    
    # 충돌 감지
    assert snake.check_wall_collision()


def test_wall_collision_bottom(snake):
    """벽 충돌 감지 - 아래쪽"""
    # 뱀을 아래쪽 경계로 이동
    snake.body = [(10, GRID_HEIGHT - 1), (10, GRID_HEIGHT - 2), (10, GRID_HEIGHT - 3)]
    snake.direction = DOWN
    
    # 이동
    snake.move()
    
    # 충돌 감지
    assert snake.check_wall_collision()


def test_self_collision(snake):
    """자기 몸통 충돌 감지"""
    # 뱀을 'ㄷ' 자 모양으로 만들어서 자기 몸통과 충돌하도록 설정
    snake.body = [
        (5, 5),  # 머리
        (5, 6),
        (5, 7),
        (6, 7),
        (7, 7),
        (7, 6),
        (7, 5),
        (6, 5)   # 꼬리
    ]
    snake.direction = LEFT
    
    # 이동 (머리가 (4, 5)로 이동)
    snake.move()
    
    # 이제 위로 이동
    snake.direction = UP
    snake.move()  # (4, 4)
    
    # 오른쪽으로 이동
    snake.direction = RIGHT
    snake.move()  # (5, 4)
    
    # 아래로 이동하면 몸통과 충돌
    snake.direction = DOWN
    snake.move()  # (5, 5) - 몸통과 충돌
    
    # 충돌 감지
    assert snake.check_self_collision()


def test_no_collision_in_normal_state(snake):
    """정상 상태에서는 충돌 감지 안 됨"""
    # 벽 충돌 없음
    assert not snake.check_wall_collision()
    
    # 자기 충돌 없음
    assert not snake.check_self_collision()


def test_get_head(snake):
    """머리 위치 반환 테스트"""
    head = snake.get_head()
    assert head == snake.body[0]
