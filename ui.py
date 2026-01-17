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
    
    def draw_info_panel(self, score, high_score, snake_length, speed, sound_on, music_on, combo_active, difficulty='normal', portal_mode=False):
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
        length_text = self.font_small.render(f"Len: {snake_length}", True, WHITE)
        self.screen.blit(length_text, (340, 5))
        
        # 속도 표시
        speed_text = self.font_small.render(f"Spd: {speed}", True, WHITE)
        self.screen.blit(speed_text, (450, 5))
        
        # 난이도 표시
        diff_colors = {'easy': GREEN, 'normal': YELLOW, 'hard': RED}
        diff_color = diff_colors.get(difficulty, WHITE)
        diff_text = self.font_small.render(f"[{difficulty[0].upper()}]", True, diff_color)
        self.screen.blit(diff_text, (540, 5))
        
        # 포탈 모드 표시
        portal_status = "P" if portal_mode else ""
        if portal_status:
            portal_text = self.font_small.render(portal_status, True, GREEN)
            self.screen.blit(portal_text, (610, 5))
        
        # Sound/Music 상태 표시
        sound_status = "S" if sound_on else ""
        if sound_status:
            sound_text = self.font_small.render(sound_status, True, GREEN)
            self.screen.blit(sound_text, (650, 5))
        
        music_status = "M" if music_on else ""
        if music_status:
            music_text = self.font_small.render(music_status, True, GREEN)
            self.screen.blit(music_text, (680, 5))
        
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
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # "PAUSED" 텍스트
        paused_text = self.font_large.render("PAUSED", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(paused_text, paused_rect)
        
        # 조작법
        y_offset = 140
        line_height = 28
        
        instructions = [
            ("Controls:", WHITE),
            ("Arrow Keys - Move Snake", GREEN),
            ("SPACE - Pause/Resume", GREEN),
            ("D - Change Difficulty", GREEN),
            ("P - Toggle Portal Mode", GREEN),
            ("S/M - Sound/Music", GREEN),
            ("", WHITE),
            ("Game Features:", WHITE),
            ("Golden Apple (Gold) - 50 pts", GOLD),
            ("Normal Food (Red) - 10 pts", RED),
            ("Combo (10s) - +5 bonus", YELLOW),
            ("Portal Mode - Pass walls", GREEN),
            ("Obstacles (Gray) - Game Over", GRAY),
        ]
        
        for text, color in instructions:
            if text:
                inst_text = self.font_small.render(text, True, color)
                inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(inst_text, inst_rect)
            y_offset += line_height
        
        # 재개 안내
        continue_text = self.font_medium.render("Press SPACE to Continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, 580))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_countdown(self, countdown_value):
        """카운트다운 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 카운트다운 숫자 (매우 크게)
        if countdown_value > 0:
            # 숫자 크기를 더 크게
            countdown_font = pygame.font.Font(None, 200)
            
            # 펄스 효과 (반짝임)
            pulse = abs(pygame.time.get_ticks() % 500 - 250) / 250.0
            scale = 1.0 + 0.2 * pulse
            font_size = int(200 * scale)
            countdown_font = pygame.font.Font(None, font_size)
            
            # 색상 바뀌어가며 표시 (3=초록, 2=노랑, 1=빨강)
            colors = {3: GREEN, 2: YELLOW, 1: RED}
            color = colors.get(countdown_value, WHITE)
            
            countdown_text = countdown_font.render(str(countdown_value), True, color)
            countdown_rect = countdown_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(countdown_text, countdown_rect)
        else:
            # "GO!" 표시
            go_font = pygame.font.Font(None, 150)
            go_text = go_font.render("GO!", True, GREEN)
            go_rect = go_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(go_text, go_rect)
    
    def draw_start_screen(self, difficulty, portal_mode):
        """게임 시작 대기 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # "SNAKE GAME" 타이틀
        title_text = self.font_large.render("SNAKE GAME", True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # 버전 정보
        version_text = self.font_small.render("Version 3.0", True, YELLOW)
        version_rect = version_text.get_rect(center=(WINDOW_WIDTH // 2, 110))
        self.screen.blit(version_text, version_rect)
        
        # 현재 설정
        y_offset = 160
        line_height = 30
        
        diff_colors = {'easy': GREEN, 'normal': YELLOW, 'hard': RED}
        diff_color = diff_colors.get(difficulty, WHITE)
        settings = [
            (f"Difficulty: {difficulty.upper()}", diff_color),
            (f"Portal Mode: {'ON' if portal_mode else 'OFF'}", GREEN if portal_mode else RED),
        ]
        
        for text, color in settings:
            setting_text = self.font_small.render(text, True, color)
            setting_rect = setting_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(setting_text, setting_rect)
            y_offset += line_height
        
        # 조작법 및 게임 설명
        y_offset = 240
        line_height = 28
        
        instructions = [
            ("== Controls ==", WHITE),
            ("Arrow Keys - Move Snake", GREEN),
            ("SPACE - Start/Pause", GREEN),
            ("D - Change Difficulty", GREEN),
            ("P - Toggle Portal Mode", GREEN),
            ("S/M - Sound/Music Toggle", GREEN),
            ("", WHITE),
            ("== Game Rules ==", WHITE),
            ("Golden Apple (Gold) - 50 pts", GOLD),
            ("Normal Food (Red) - 10 pts", RED),
            ("Combo (10s) - +5 bonus", YELLOW),
            ("Portal: Pass walls safely", GREEN),
            ("Gray Obstacles (Hard) - Avoid!", GRAY),
        ]
        
        for text, color in instructions:
            if text:
                inst_text = self.font_small.render(text, True, color)
                inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(inst_text, inst_rect)
            y_offset += line_height
        
        # 시작 안내 (반짝임 효과)
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
        alpha = int(150 + 105 * pulse)
        start_color = (alpha, alpha, alpha)
        start_text = self.font_medium.render("Press SPACE to Start!", True, start_color)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 590))
        self.screen.blit(start_text, start_rect)
