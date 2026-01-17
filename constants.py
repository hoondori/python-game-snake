"""게임에서 사용되는 상수 정의"""

# 화면 설정
INFO_PANEL_HEIGHT = 40  # 정보 패널 높이
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600 + INFO_PANEL_HEIGHT  # 패널 포함
GRID_SIZE = 20  # 각 블록의 크기 (픽셀)
GRID_WIDTH = 600 // GRID_SIZE  # 30
GRID_HEIGHT = 600 // GRID_SIZE  # 30

# 색상 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # 뱀 색상
LIGHT_GREEN = (0, 255, 0)  # 뱀 머리 색상
DARK_GREEN = (0, 136, 0)  # 뱀 몸통 색상
RED = (255, 0, 0)    # 먹이 색상
YELLOW = (255, 255, 0)  # 최고 점수 색상
GOLD = (255, 215, 0)  # Golden Apple 색상
DARK_GRAY = (40, 40, 40)  # 패널 배경
GRID_COLOR = (30, 30, 30)  # 그리드 라인 색상
GRAY = (128, 128, 128)  # 장애물 색상

# 난이도 설정
DIFFICULTIES = {
    'easy': {
        'initial_fps': 8,
        'speed_increase_interval': 10,
        'max_fps': 15,
        'obstacles': 0
    },
    'normal': {
        'initial_fps': 10,
        'speed_increase_interval': 5,
        'max_fps': 18,
        'obstacles': 0
    },
    'hard': {
        'initial_fps': 12,
        'speed_increase_interval': 3,
        'max_fps': 22,
        'obstacles': 5
    }
}

# 게임 설정 (기본값 - Normal)
INITIAL_FPS = 10  # 초기 속도
MAX_FPS = 20  # 최대 속도
SPEED_INCREASE_INTERVAL = 5  # 몇 개마다 속도 증가

# Golden Apple 설정
GOLDEN_APPLE_PROBABILITY = 0.1  # 10% 확률
GOLDEN_APPLE_SCORE = 50  # 점수
GOLDEN_APPLE_TIMEOUT = 10  # 10초 후 사라짐
NORMAL_FOOD_SCORE = 10  # 일반 먹이 점수

# 방향
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
