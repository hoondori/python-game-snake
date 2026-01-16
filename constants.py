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
DARK_GRAY = (40, 40, 40)  # 패널 배경
GRID_COLOR = (30, 30, 30)  # 그리드 라인 색상

# 게임 설정
INITIAL_FPS = 10  # 초기 속도
MAX_FPS = 20  # 최대 속도
SPEED_INCREASE_INTERVAL = 5  # 몇 개마다 속도 증가

# 방향
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
