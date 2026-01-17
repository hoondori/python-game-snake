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

# 파워업 설정
POWERUP_SPEED_BOOST = 'speed_boost'
POWERUP_SLOW_MOTION = 'slow_motion'
POWERUP_INVINCIBLE = 'invincible'

POWERUP_COLORS = {
    POWERUP_SPEED_BOOST: (0, 100, 255),  # 파란색
    POWERUP_SLOW_MOTION: (138, 43, 226),  # 보라색
    POWERUP_INVINCIBLE: (0, 255, 100)  # 녹색
}

POWERUP_PROBABILITY = {
    POWERUP_SPEED_BOOST: 0.05,  # 5%
    POWERUP_SLOW_MOTION: 0.05,  # 5%
    POWERUP_INVINCIBLE: 0.03  # 3%
}

POWERUP_DURATION = 5  # 5초 지속
POWERUP_SCORE = {
    POWERUP_SPEED_BOOST: 20,
    POWERUP_SLOW_MOTION: 20,
    POWERUP_INVINCIBLE: 30
}

POWERUP_EFFECTS = {
    POWERUP_SPEED_BOOST: 1.5,  # 속도 1.5배
    POWERUP_SLOW_MOTION: 0.7  # 속도 0.7배
}

# 게임 모드
MODE_CLASSIC = 'classic'
MODE_TIME_ATTACK = 'time_attack'
MODE_SURVIVAL = 'survival'
MODE_PORTAL = 'portal'

# Time Attack 설정
TIME_ATTACK_DURATION = 60  # 60초
TIME_ATTACK_BONUS_TIME = 5  # 시간 보너스 +5초

# Survival 설정
SURVIVAL_OBSTACLE_INTERVAL = 10  # 10초마다 장애물 추가
SURVIVAL_MAX_OBSTACLES = 20  # 최대 20개

# 파티클 효과
PARTICLE_LIFETIME = 30  # 30 프레임
PARTICLE_COUNT = 10  # 폭발 시 파티클 수
