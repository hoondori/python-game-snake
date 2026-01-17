"""게임 로직 관리 클래스"""
import pygame
from constants import *
from core.snake import Snake
from core.food import Food
from core.obstacle import Obstacle
from ui.hud import UI
from managers.score_manager import ScoreManager
from managers.sound_manager import SoundManager
from config import ConfigManager


class Game:
    def __init__(self, screen=None, difficulty='normal', portal_mode=False, sound_enabled=True, music_enabled=True):
        """게임 초기화"""
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Snake Game - Version 3.1")
            self.own_screen = True
        else:
            self.screen = screen
            self.own_screen = False
        
        # 시계 설정 (FPS 제어)
        self.clock = pygame.time.Clock()
        
        # 게임 객체
        self.snake = Snake()
        self.food = Food()
        self.ui = UI(self.screen)
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        
        # 설정 적용
        self.sound_manager.sound_enabled = sound_enabled
        self.sound_manager.music_enabled = music_enabled
        
        # 난이도 설정
        self.difficulty = difficulty
        self.apply_difficulty_settings()
        
        # 장애물 생성 (난이도에 따라)
        obstacle_count = DIFFICULTIES[self.difficulty]['obstacles']
        self.obstacle = Obstacle(obstacle_count, self.snake.body, self.food.get_position()) if obstacle_count > 0 else None
        
        # 먹이 재생성 (장애물 고려)
        obstacle_positions = self.obstacle.get_positions() if self.obstacle else []
        self.food.spawn(self.snake.body, obstacle_positions)
        
        # 포탈 모드
        self.portal_mode = portal_mode
        
        # 게임 상태
        self.running = True
        self.game_over = False
        self.paused = False
        self.waiting = True  # 게임 시작 대기 상태
        self.countdown = False  # 카운트다운 상태
        self.countdown_value = 3  # 카운트다운 숫자 (3, 2, 1)
        self.countdown_start_time = 0  # 카운트다운 시작 시간
        
        # 배경 음악 시작
        if self.sound_manager.music_enabled:
            self.sound_manager.start_background_music()
    
    def apply_difficulty_settings(self):
        """난이도 설정 적용"""
        settings = DIFFICULTIES[self.difficulty]
        self.initial_fps = settings['initial_fps']
        self.speed_increase_interval = settings['speed_increase_interval']
        self.max_fps = settings['max_fps']
        self.current_fps = self.initial_fps
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # ESC - 종료
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # SPACE - 게임 시작 또는 일시정지/재개
                elif event.key == pygame.K_SPACE:
                    if self.waiting:
                        # 게임 시작
                        self.waiting = False
                    elif not self.game_over:
                        # 일시정지/재개
                        self.paused = not self.paused
                
                # R - 재시작 (게임 오버 상태에서만)
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                
                # M - 배경 음악 토글
                elif event.key == pygame.K_m:
                    self.sound_manager.toggle_music()
                    self.config_manager.set('music_enabled', self.sound_manager.music_enabled)
                
                # S - 사운드 효과 토글
                elif event.key == pygame.K_s:
                    self.sound_manager.toggle_sound()
                    self.config_manager.set('sound_enabled', self.sound_manager.sound_enabled)
                
                # D - 난이도 변경 (게임 시작 전/게임 오버 시)
                elif event.key == pygame.K_d:
                    self.cycle_difficulty()
                
                # P - 포탈 모드 토글
                elif event.key == pygame.K_p:
                    self.portal_mode = self.config_manager.toggle_portal_mode()
                
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
        # 카운트다운 처리
        if self.countdown:
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.countdown_start_time) / 1000.0
            
            # 1초마다 카운트다운 감소
            if elapsed >= 1.0:
                self.countdown_value -= 1
                self.countdown_start_time = current_time
                
                # 카운트다운 종료
                if self.countdown_value <= 0:
                    self.countdown = False
                    return
            
            return
        
        if self.waiting or self.game_over or self.paused:
            return
        
        # Golden Apple 타이머 체크 (10초 경과 시 재생성)
        if self.food.should_respawn():
            obstacle_positions = self.obstacle.get_positions() if self.obstacle else []
            self.food.spawn(self.snake.body, obstacle_positions)
        
        # 뱀 이동 (Portal 모드 적용)
        self.snake.move(self.portal_mode)
        
        # 벽 충돌 확인 (Portal 모드가 아닐 때만)
        if not self.portal_mode and self.snake.check_wall_collision():
            self.game_over = True
            self.score_manager.end_game()
            self.sound_manager.play_game_over_sound()
            return
        
        # 장애물 충돌 확인
        if self.obstacle and self.obstacle.check_collision(self.snake.get_head()):
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
            
            # 점수 추가 (Golden Apple이면 50점, 일반은 10점)
            food_value = self.food.get_value()
            if food_value == GOLDEN_APPLE_SCORE:
                # Golden Apple: 직접 점수 추가
                self.score_manager.score += food_value
                if self.score_manager.score > self.score_manager.high_score:
                    self.score_manager.high_score = self.score_manager.score
                    self.score_manager.save_high_score()
                self.score_manager.food_eaten += 1
            else:
                # 일반 먹이: 기존 로직 (콤보 포함)
                self.score_manager.add_food()
            
            # 먹이 재생성
            obstacle_positions = self.obstacle.get_positions() if self.obstacle else []
            self.food.spawn(self.snake.body, obstacle_positions)
            self.sound_manager.play_eat_sound()
            
            # 속도 증가
            if self.score_manager.get_food_eaten() % self.speed_increase_interval == 0:
                if self.current_fps < self.max_fps:
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
        
        # Portal 모드일 때 테두리 효과
        if self.portal_mode:
            # 펄스 효과 (0.6 ~ 1.0 사이로 반짝임)
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
            brightness = 0.6 + 0.4 * pulse
            
            # 초록색/청록색 (Portal 느낌)
            portal_color = (
                int(0 * brightness),
                int(255 * brightness),
                int(200 * brightness)
            )
            
            # 점선 테두리 그리기 (상, 하, 좌, 우)
            dash_length = 15
            gap_length = 10
            border_width = 4
            
            # 상단 테두리
            x = 0
            while x < 600:
                pygame.draw.line(game_surface, portal_color, 
                               (x, 0), (min(x + dash_length, 600), 0), border_width)
                x += dash_length + gap_length
            
            # 하단 테두리
            x = 0
            while x < 600:
                pygame.draw.line(game_surface, portal_color, 
                               (x, 599), (min(x + dash_length, 600), 599), border_width)
                x += dash_length + gap_length
            
            # 좌측 테두리
            y = 0
            while y < 600:
                pygame.draw.line(game_surface, portal_color, 
                               (0, y), (0, min(y + dash_length, 600)), border_width)
                y += dash_length + gap_length
            
            # 우측 테두리
            y = 0
            while y < 600:
                pygame.draw.line(game_surface, portal_color, 
                               (599, y), (599, min(y + dash_length, 600)), border_width)
                y += dash_length + gap_length
        
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
        
        # 먹이 그리기 (Golden Apple이면 금색, 일반은 빨간색 + 펄스 효과)
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
        food_color = GOLD if self.food.is_golden else RED
        pygame.draw.rect(game_surface, food_color, food_rect)
        
        # 장애물 그리기
        if self.obstacle:
            for obs_pos in self.obstacle.get_positions():
                obs_rect = pygame.Rect(
                    obs_pos[0] * GRID_SIZE,
                    obs_pos[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE
                )
                pygame.draw.rect(game_surface, GRAY, obs_rect)
        
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
            self.score_manager.is_combo_active(),
            self.difficulty,
            self.portal_mode
        )
        
        # 카운트다운 화면
        if self.countdown:
            self.ui.draw_countdown(self.countdown_value)
        
        # 시작 대기 화면
        elif self.waiting:
            self.ui.draw_start_screen(self.difficulty, self.portal_mode)
        
        # 일시정지 화면
        elif self.paused:
            self.ui.draw_pause_screen()
        
        # 게임 오버 화면
        elif self.game_over:
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
        
        # 난이도 재적용
        self.apply_difficulty_settings()
        
        # 장애물 재생성
        obstacle_count = DIFFICULTIES[self.difficulty]['obstacles']
        self.obstacle = Obstacle(obstacle_count, self.snake.body, (0, 0)) if obstacle_count > 0 else None
        
        # 먹이 재생성
        obstacle_positions = self.obstacle.get_positions() if self.obstacle else []
        self.food = Food()
        self.food.spawn(self.snake.body, obstacle_positions)
        
        self.score_manager.reset()
        self.game_over = False
        self.paused = False
    
    def cycle_difficulty(self):
        """난이도 순환 변경 (Easy → Normal → Hard → Easy)"""
        difficulties = ['easy', 'normal', 'hard']
        current_index = difficulties.index(self.difficulty)
        self.difficulty = difficulties[(current_index + 1) % 3]
        self.config_manager.set_difficulty(self.difficulty)
        
        # 난이도 변경 시 게임 재시작 + 카운트다운
        if not self.game_over:
            self.reset_game()
            # 카운트다운 시작
            self.countdown = True
            self.countdown_value = 3
            self.countdown_start_time = pygame.time.get_ticks()
    
    def run(self):
        """게임 메인 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # FPS 제어
            self.clock.tick(self.current_fps)
        
        # 배경 음악 정지
        if self.sound_manager.music_enabled:
            self.sound_manager.stop_background_music()
        
        # 자체 화면인 경우만 pygame.quit() 호출
        if self.own_screen:
            pygame.quit()
