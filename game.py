"""게임 로직 관리 클래스"""
import pygame
from constants import *
from snake import Snake
from food import Food
from ui import UI
from score_manager import ScoreManager
from sound_manager import SoundManager


class Game:
    def __init__(self):
        """게임 초기화"""
        pygame.init()
        
        # 화면 설정
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Version 2")
        
        # 시계 설정 (FPS 제어)
        self.clock = pygame.time.Clock()
        
        # 게임 객체
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.body)
        self.ui = UI(self.screen)
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        
        # 게임 상태
        self.running = True
        self.game_over = False
        self.paused = False
        
        # 속도 설정
        self.current_fps = INITIAL_FPS
        
        # 배경 음악 시작
        self.sound_manager.start_background_music()
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # ESC - 종료
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # SPACE - 일시정지/재개
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.paused = not self.paused
                
                # R - 재시작 (게임 오버 상태에서만)
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                
                # M - 배경 음악 토글
                elif event.key == pygame.K_m:
                    self.sound_manager.toggle_music()
                
                # S - 사운드 효과 토글
                elif event.key == pygame.K_s:
                    self.sound_manager.toggle_sound()
                
                # 방향키 (게임 진행 중일 때만)
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
    
    def update(self):
        """게임 상태 업데이트"""
        if self.game_over or self.paused:
            return
        
        # 뱀 이동
        self.snake.move()
        
        # 벽 충돌 확인
        if self.snake.check_wall_collision():
            self.game_over = True
            self.score_manager.end_game()
            self.sound_manager.play_game_over_sound()
            return
        
        # 자기 몸통 충돌 확인
        if self.snake.check_self_collision():
            self.game_over = True
            self.score_manager.end_game()
            self.sound_manager.play_game_over_sound()
            return
        
        # 먹이 먹기 확인
        if self.snake.get_head() == self.food.get_position():
            self.snake.grow()
            self.food.spawn(self.snake.body)
            self.score_manager.add_food()
            self.sound_manager.play_eat_sound()
            
            # 속도 증가 (5개마다)
            if self.score_manager.get_food_eaten() % SPEED_INCREASE_INTERVAL == 0:
                if self.current_fps < MAX_FPS:
                    self.current_fps += 1
    
    def draw(self):
        """화면 그리기"""
        # 배경 (검은색)
        self.screen.fill(BLACK)
        
        # 게임 영역만 따로 그리기 (정보 패널 아래)
        game_surface = pygame.Surface((600, 600))
        game_surface.fill(BLACK)
        
        # 그리드 라인 그리기
        for x in range(0, 600, GRID_SIZE):
            pygame.draw.line(game_surface, GRID_COLOR, (x, 0), (x, 600))
        for y in range(0, 600, GRID_SIZE):
            pygame.draw.line(game_surface, GRID_COLOR, (0, y), (600, y))
        
        # 뱀 그리기
        for i, segment in enumerate(self.snake.body):
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            # 머리는 밝은 녹색, 몸통은 어두운 녹색
            if i == 0:
                base_color = LIGHT_GREEN
            else:
                base_color = DARK_GREEN
            
            # 콤보 활성화 시 반짝이는 효과
            if self.score_manager.is_combo_active():
                # 0.0 ~ 1.0 사이로 진동하는 값 (더 빠른 주기)
                pulse = abs(pygame.time.get_ticks() % 300 - 150) / 150.0
                # 밝기 조절 (0.5 ~ 1.3) - 더 강한 효과
                brightness = 0.5 + 0.8 * pulse
                # 색상에 노란색 톤 추가
                if i == 0:  # 머리
                    r = min(255, int(base_color[0] * brightness + 50 * pulse))
                    g = min(255, int(base_color[1] * brightness + 50 * pulse))
                    b = int(base_color[2] * brightness)
                else:  # 몸통
                    r = min(255, int(base_color[0] * brightness + 30 * pulse))
                    g = min(255, int(base_color[1] * brightness + 30 * pulse))
                    b = int(base_color[2] * brightness)
                color = (r, g, b)
            else:
                color = base_color
            
            pygame.draw.rect(game_surface, color, rect)
        
        # 먹이 그리기 (빨간색 + 펄스 효과)
        food_pos = self.food.get_position()
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0  # 0.0 ~ 1.0 왕복
        food_size = int(GRID_SIZE * (0.8 + 0.2 * pulse))  # 80% ~ 100% 크기
        food_offset = (GRID_SIZE - food_size) // 2
        
        food_rect = pygame.Rect(
            food_pos[0] * GRID_SIZE + food_offset,
            food_pos[1] * GRID_SIZE + food_offset,
            food_size,
            food_size
        )
        pygame.draw.rect(game_surface, RED, food_rect)
        
        # 게임 화면을 메인 화면에 그리기 (패널 아래)
        self.screen.blit(game_surface, (0, INFO_PANEL_HEIGHT))
        
        # 정보 패널 그리기
        self.ui.draw_info_panel(
            self.score_manager.get_score(),
            self.score_manager.get_high_score(),
            len(self.snake.body),
            self.current_fps,
            self.sound_manager.sound_enabled,
            self.sound_manager.music_enabled,
            self.score_manager.is_combo_active()
        )
        
        # 일시정지 화면
        if self.paused:
            self.ui.draw_pause_screen()
        
        # 게임 오버 화면
        if self.game_over:
            self.ui.draw_game_over_screen(
                self.score_manager.get_score(),
                self.score_manager.get_high_score(),
                self.score_manager.get_food_eaten(),
                self.score_manager.get_play_time()
            )
        
        # 화면 업데이트
        pygame.display.flip()
    
    def reset_game(self):
        """게임 재시작"""
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.body)
        self.score_manager.reset()
        self.game_over = False
        self.paused = False
        self.current_fps = INITIAL_FPS
    
    def run(self):
        """게임 메인 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # FPS 제어
            self.clock.tick(self.current_fps)
        
        pygame.quit()
