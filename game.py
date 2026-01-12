"""게임 로직 관리 클래스"""
import pygame
from constants import *
from snake import Snake
from food import Food


class Game:
    def __init__(self):
        """게임 초기화"""
        pygame.init()
        
        # 화면 설정
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
        # 시계 설정 (FPS 제어)
        self.clock = pygame.time.Clock()
        
        # 게임 객체
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.body)
        
        # 게임 상태
        self.running = True
        self.game_over = False
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 키보드 입력 처리
            if event.type == pygame.KEYDOWN and not self.game_over:
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
        if self.game_over:
            return
        
        # 뱀 이동
        self.snake.move()
        
        # 벽 충돌 확인
        if self.snake.check_wall_collision():
            self.game_over = True
            return
        
        # 자기 몸통 충돌 확인
        if self.snake.check_self_collision():
            self.game_over = True
            return
        
        # 먹이 먹기 확인
        if self.snake.get_head() == self.food.get_position():
            self.snake.grow()
            self.food.spawn(self.snake.body)
    
    def draw(self):
        """화면 그리기"""
        # 배경 (검은색)
        self.screen.fill(BLACK)
        
        # 뱀 그리기 (녹색)
        for segment in self.snake.body:
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(self.screen, GREEN, rect)
        
        # 먹이 그리기 (빨간색)
        food_pos = self.food.get_position()
        food_rect = pygame.Rect(
            food_pos[0] * GRID_SIZE,
            food_pos[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # 게임 오버 메시지
        if self.game_over:
            self.draw_game_over()
        
        # 화면 업데이트
        pygame.display.flip()
    
    def draw_game_over(self):
        """게임 오버 메시지 표시"""
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)
    
    def run(self):
        """게임 메인 루프"""
        game_over_time = None
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # 게임 오버 후 2초 대기
            if self.game_over and game_over_time is None:
                game_over_time = pygame.time.get_ticks()
            
            if game_over_time and pygame.time.get_ticks() - game_over_time > 2000:
                self.running = False
            
            # FPS 제어
            self.clock.tick(FPS)
        
        pygame.quit()
