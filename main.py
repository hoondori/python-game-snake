"""Snake Game - Version 3.1
메인 실행 파일
"""
import pygame
import sys
from ui.menu import MainMenu
from ui.leaderboard import Leaderboard, LeaderboardUI
from managers.achievement_manager import AchievementManager
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK


class GameApp:
    """게임 애플리케이션 메인 클래스"""
    
    def __init__(self):
        """게임 애플리케이션 초기화"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game v3.1")
        self.clock = pygame.time.Clock()
        
        # 메뉴 및 관리자
        self.main_menu = MainMenu()
        self.leaderboard = Leaderboard()
        self.leaderboard_ui = LeaderboardUI(self.leaderboard)
        self.achievement_manager = AchievementManager()
        
        # 상태
        self.state = "menu"  # menu, game, leaderboard, achievements
        self.game = None
        
    def run(self):
        """메인 루프"""
        running = True
        
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._handle_input(event)
                    
            self._update()
            self._draw()
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
        
    def _handle_input(self, event):
        """입력 처리"""
        if self.state == "menu":
            result = self.main_menu.handle_input(event)
            if result == "start":
                self._start_game()
            elif result == "highscores":
                self.state = "leaderboard"
            elif result == "achievements":
                self.state = "achievements"
            elif result == "quit":
                pygame.quit()
                sys.exit()
                
        elif self.state == "game":
            if self.game:
                # 게임 입력은 game.run() 내부에서 처리
                pass
                
        elif self.state == "leaderboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    
        elif self.state == "achievements":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    
    def _update(self):
        """업데이트"""
        pass
        
    def _draw(self):
        """화면 그리기"""
        if self.state == "menu":
            self.main_menu.draw(self.screen)
        elif self.state == "leaderboard":
            self.leaderboard_ui.draw(self.screen)
        elif self.state == "achievements":
            self._draw_achievements()
            
    def _start_game(self):
        """게임 시작"""
        from core.game import Game
        
        # 설정 가져오기
        difficulty = self.main_menu.get_selected_difficulty()
        mode = self.main_menu.get_selected_mode()
        settings = self.main_menu.get_settings()
        
        # 포탈 모드 확인 (mode가 'portal'인 경우)
        portal_mode = (mode == 'portal')
        
        # 게임 생성 및 실행
        try:
            game = Game(
                screen=self.screen,
                difficulty=difficulty,
                portal_mode=portal_mode,
                sound_enabled=settings.get('sound', True),
                music_enabled=settings.get('music', True)
            )
            game.run()
            
            # 게임 종료 후 점수를 리더보드에 추가
            if game.score_manager.get_score() > 0:
                player_name = "Player"  # 기본 이름 (추후 입력 기능 추가 가능)
                rank = self.leaderboard.add_score(
                    player_name,
                    game.score_manager.get_score(),
                    difficulty,
                    mode
                )
                print(f"Score saved: {game.score_manager.get_score()} (Rank: {rank})")
        except Exception as e:
            print(f"Game error: {e}")
        
        # 게임 종료 후 메뉴로 돌아가기
        self.state = "menu"
        
    def _draw_achievements(self):
        """업적 화면 그리기"""
        from constants import WHITE, YELLOW, GREEN, GRAY
        
        self.screen.fill(BLACK)
        
        # 타이틀
        title_font = pygame.font.Font(None, 56)
        title_text = title_font.render("ACHIEVEMENTS", True, YELLOW)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # 진행도
        progress = self.achievement_manager.get_progress()
        progress_font = pygame.font.Font(None, 28)
        progress_text = f"{progress['unlocked']}/{progress['total']} ({progress['percentage']}%)"
        progress_render = progress_font.render(progress_text, True, GREEN)
        progress_rect = progress_render.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(progress_render, progress_rect)
        
        # 업적 목록
        achievements = self.achievement_manager.get_all_achievements()
        item_font = pygame.font.Font(None, 24)
        start_y = 150
        item_spacing = 50
        
        for i, achievement in enumerate(achievements[:8]):  # 최대 8개 표시
            y = start_y + i * item_spacing
            
            # 잠금 해제 여부에 따른 색상
            color = GREEN if achievement.unlocked else GRAY
            
            # 이름
            name_text = item_font.render(
                f"{'✓' if achievement.unlocked else '✗'} {achievement.name}",
                True, color
            )
            self.screen.blit(name_text, (100, y))
            
            # 설명
            desc_font = pygame.font.Font(None, 20)
            desc_text = desc_font.render(achievement.description, True, GRAY)
            self.screen.blit(desc_text, (120, y + 25))
            
        # 하단 안내
        hint_font = pygame.font.Font(None, 24)
        hint_text = "Press ESC to return"
        hint_render = hint_font.render(hint_text, True, GRAY)
        hint_rect = hint_render.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(hint_render, hint_rect)


def main():
    """게임 시작"""
    app = GameApp()
    app.run()


if __name__ == "__main__":
    main()

