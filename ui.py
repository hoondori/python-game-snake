"""UI 렌더링 클래스"""
import pygame
from constants import *


class UI:
    def __init__(self, screen):
        """UI 초기화"""
        self.screen = screen
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
    
    def draw_info_panel(self, score, high_score, snake_length, speed, sound_on, music_on, combo_active):
        """게임 정보 패널 그리기"""
        # 패널 배경
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        
        # 경계선
        pygame.draw.line(self.screen, WHITE, 
                        (0, INFO_PANEL_HEIGHT), 
                        (WINDOW_WIDTH, INFO_PANEL_HEIGHT), 2)
        
        # 점수 표시
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_text, (10, 5))
        
        # 최고 점수 표시
        high_score_text = self.font_small.render(f"High: {high_score}", True, YELLOW)
        self.screen.blit(high_score_text, (180, 5))
        
        # 뱀 길이 표시
        length_text = self.font_small.render(f"Length: {snake_length}", True, WHITE)
        self.screen.blit(length_text, (360, 5))
        
        # 속도 표시
        speed_text = self.font_small.render(f"Speed: {speed}", True, WHITE)
        self.screen.blit(speed_text, (520, 5))
        
        # Sound/Music 상태 표시
        sound_status = "ON" if sound_on else "OFF"
        sound_color = GREEN if sound_on else RED
        sound_text = self.font_small.render(f"S:{sound_status}", True, sound_color)
        self.screen.blit(sound_text, (650, 5))
        
        music_status = "ON" if music_on else "OFF"
        music_color = GREEN if music_on else RED
        music_text = self.font_small.render(f"M:{music_status}", True, music_color)
        self.screen.blit(music_text, (730, 5))
        
        # COMBO 활성화 표시 (반짝이는 효과)
        if combo_active:
            # 빠른 펄스로 반짝임 (0.3초 주기)
            pulse = abs(pygame.time.get_ticks() % 300 - 150) / 150.0
            # 주황색과 노란색 사이를 진동
            r = int(255)
            g = int(165 + 90 * pulse)  # 165 ~ 255
            b = int(0)
            combo_color = (r, g, b)
            combo_text = self.font_medium.render("COMBO!", True, combo_color)
            combo_rect = combo_text.get_rect(center=(WINDOW_WIDTH // 2, INFO_PANEL_HEIGHT // 2))
            self.screen.blit(combo_text, combo_rect)
    
    def draw_game_over_screen(self, score, high_score, food_eaten, play_time):
        """게임 오버 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # "GAME OVER" 텍스트
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 최종 점수
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        # 최고 점수 (0점보다 크고 최고점을 넘었을 때만 NEW HIGH SCORE 표시)
        if score > high_score and score > 0:
            high_text = self.font_small.render("NEW HIGH SCORE!", True, YELLOW)
        else:
            high_text = self.font_small.render(f"High Score: {high_score}", True, YELLOW)
        high_rect = high_text.get_rect(center=(WINDOW_WIDTH // 2, 310))
        self.screen.blit(high_text, high_rect)
        
        # 통계 정보
        stats_y = 370
        stats = [
            f"Food Eaten: {food_eaten}",
            f"Play Time: {play_time}s",
        ]
        
        for stat in stats:
            stat_text = self.font_small.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(WINDOW_WIDTH // 2, stats_y))
            self.screen.blit(stat_text, stat_rect)
            stats_y += 40
        
        # 재시작/종료 안내
        restart_text = self.font_small.render("Press R to Restart or ESC to Quit", True, GREEN)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 500))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause_screen(self):
        """일시정지 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # "PAUSED" 텍스트
        paused_text = self.font_large.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(paused_text, paused_rect)
        
        # 재개 안내
        continue_text = self.font_small.render("Press SPACE to Continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(continue_text, continue_rect)
        
        # 사운드/음악 컨트롤 안내
        control_text = self.font_small.render("M: Music | S: Sound", True, WHITE)
        control_rect = control_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(control_text, control_rect)
