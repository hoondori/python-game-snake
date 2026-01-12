"""게임에서 사용되는 상수 정의"""

# 화면 설정
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20  # 각 블록의 크기 (픽셀)
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE  # 30
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 30

# 색상 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # 뱀 색상
RED = (255, 0, 0)    # 먹이 색상

# 게임 설정
FPS = 10  # 초당 프레임 (이동 속도)

# 방향
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
