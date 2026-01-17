"""메뉴 시스템"""
import pygame
from typing import List, Tuple, Optional, Callable
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GREEN, 
    YELLOW, RED, GRAY, DARK_GRAY
)


class MenuItem:
    """메뉴 항목 클래스"""
    
    def __init__(self, text: str, action: Optional[Callable] = None, 
                 submenu: Optional['Menu'] = None):
        """
        메뉴 항목 초기화
        
        Args:
            text: 표시 텍스트
            action: 선택 시 실행할 함수
            submenu: 하위 메뉴
        """
        self.text = text
        self.action = action
        self.submenu = submenu
        self.selected = False
        
    def select(self):
        """메뉴 항목 선택 표시"""
        self.selected = True
        
    def deselect(self):
        """메뉴 항목 선택 해제"""
        self.selected = False
        
    def execute(self):
        """메뉴 항목 실행"""
        if self.action:
            return self.action()
        return None


class Menu:
    """메뉴 클래스"""
    
    def __init__(self, title: str, items: List[MenuItem], 
                 parent: Optional['Menu'] = None):
        """
        메뉴 초기화
        
        Args:
            title: 메뉴 제목
            items: 메뉴 항목 리스트
            parent: 부모 메뉴
        """
        self.title = title
        self.items = items
        self.parent = parent
        self.selected_index = 0
        self.active = True
        self.frame = 0
        
        # 첫 항목 선택
        if self.items:
            self.items[0].select()
            
    def handle_input(self, event: pygame.event.Event) -> Optional[str]:
        """
        입력 처리
        
        Args:
            event: 이벤트
            
        Returns:
            액션 또는 None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._move_selection(-1)
                return "move"
            elif event.key == pygame.K_DOWN:
                self._move_selection(1)
                return "move"
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._execute_selected()
            elif event.key == pygame.K_ESCAPE:
                return "back"
                
        return None
        
    def _move_selection(self, direction: int) -> None:
        """
        선택 이동
        
        Args:
            direction: 이동 방향 (1: 아래, -1: 위)
        """
        self.items[self.selected_index].deselect()
        self.selected_index = (self.selected_index + direction) % len(self.items)
        self.items[self.selected_index].select()
        
    def _execute_selected(self) -> Optional[str]:
        """
        선택된 항목 실행
        
        Returns:
            실행 결과
        """
        selected_item = self.items[self.selected_index]
        
        if selected_item.submenu:
            return "submenu"
        elif selected_item.action:
            result = selected_item.execute()
            return result if result else "action"
            
        return None
        
    def get_selected_item(self) -> MenuItem:
        """선택된 항목 반환"""
        return self.items[self.selected_index]
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        메뉴 그리기
        
        Args:
            surface: 그릴 화면
        """
        self.frame += 1
        
        # 배경
        surface.fill(BLACK)
        
        # 타이틀
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render(self.title, True, GREEN)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        surface.blit(title_text, title_rect)
        
        # 메뉴 항목들
        item_font = pygame.font.Font(None, 36)
        start_y = 250
        item_spacing = 60
        
        for i, item in enumerate(self.items):
            y = start_y + i * item_spacing
            
            # 선택된 항목 하이라이트
            if item.selected:
                # 깜빡이는 효과
                pulse = abs((self.frame % 60) - 30) / 30.0
                color = (
                    int(255 * pulse),
                    int(255 * (0.5 + 0.5 * pulse)),
                    0
                )
                
                # 선택 표시
                marker = "► "
                marker_text = item_font.render(marker, True, color)
                marker_rect = marker_text.get_rect(right=WINDOW_WIDTH // 2 - 20, centery=y)
                surface.blit(marker_text, marker_rect)
                
                # 배경 박스
                text_width = item_font.size(item.text)[0]
                box_rect = pygame.Rect(
                    WINDOW_WIDTH // 2 - text_width // 2 - 20,
                    y - 25,
                    text_width + 40,
                    50
                )
                pygame.draw.rect(surface, DARK_GRAY, box_rect)
                pygame.draw.rect(surface, YELLOW, box_rect, 2)
            else:
                color = WHITE
                
            # 텍스트
            text = item_font.render(item.text, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            surface.blit(text, text_rect)
            
        # 하단 안내
        hint_font = pygame.font.Font(None, 24)
        hint_text = "↑↓: Move  Enter: Select  ESC: Back"
        hint_render = hint_font.render(hint_text, True, GRAY)
        hint_rect = hint_render.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        surface.blit(hint_render, hint_rect)


class MainMenu:
    """메인 메뉴 관리 클래스"""
    
    def __init__(self):
        """메인 메뉴 초기화"""
        self.current_menu: Optional[Menu] = None
        self.menu_stack: List[Menu] = []
        self.selected_difficulty = "normal"
        self.selected_mode = "classic"
        self.settings = {
            'sound': True,
            'music': True,
            'grid': True,
            'controls': 'arrows'
        }
        self._create_menus()
        
    def _create_menus(self) -> None:
        """메뉴들 생성"""
        # 메인 메뉴 먼저 생성 (parent 없음)
        self.main_menu = Menu("SNAKE GAME", [])
        
        # 메인 메뉴 아이템 생성 및 설정
        difficulty_text = f"Difficulty (Current: {self.selected_difficulty.capitalize()})"
        mode_text = f"Game Mode (Current: {self.selected_mode.replace('_', ' ').title()})"
        
        main_items = [
            MenuItem("Start Game", action=lambda: "start"),
            MenuItem(difficulty_text, submenu=self._create_difficulty_menu()),
            MenuItem(mode_text, submenu=self._create_mode_menu()),
            MenuItem("Settings", submenu=self._create_settings_menu()),
            MenuItem("High Scores", action=lambda: "highscores"),
            MenuItem("Achievements", action=lambda: "achievements"),
            MenuItem("Quit", action=lambda: "quit")
        ]
        self.main_menu.items = main_items
        self.main_menu.selected_index = 0
        if main_items:
            main_items[0].select()
            
        self.current_menu = self.main_menu
        self.menu_stack = [self.main_menu]
        
    def _create_difficulty_menu(self) -> Menu:
        """난이도 선택 메뉴 생성"""
        easy_text = "✓ Easy - Slow speed, no obstacles" if self.selected_difficulty == "easy" else "  Easy - Slow speed, no obstacles"
        normal_text = "✓ Normal - Medium speed" if self.selected_difficulty == "normal" else "  Normal - Medium speed"
        hard_text = "✓ Hard - Fast speed, obstacles" if self.selected_difficulty == "hard" else "  Hard - Fast speed, obstacles"
        
        items = [
            MenuItem(easy_text, action=lambda: self._set_difficulty("easy")),
            MenuItem(normal_text, action=lambda: self._set_difficulty("normal")),
            MenuItem(hard_text, action=lambda: self._set_difficulty("hard")),
            MenuItem("Back", action=lambda: "back")
        ]
        return Menu("SELECT DIFFICULTY", items, self.main_menu)
        
    def _create_mode_menu(self) -> Menu:
        """게임 모드 선택 메뉴 생성"""
        classic_text = "✓ Classic - Traditional snake" if self.selected_mode == "classic" else "  Classic - Traditional snake"
        time_attack_text = "✓ Time Attack - 60 seconds" if self.selected_mode == "time_attack" else "  Time Attack - 60 seconds"
        survival_text = "✓ Survival - Increasing obstacles" if self.selected_mode == "survival" else "  Survival - Increasing obstacles"
        portal_text = "✓ Portal - Wrap around walls" if self.selected_mode == "portal" else "  Portal - Wrap around walls"
        
        items = [
            MenuItem(classic_text, action=lambda: self._set_mode("classic")),
            MenuItem(time_attack_text, action=lambda: self._set_mode("time_attack")),
            MenuItem(survival_text, action=lambda: self._set_mode("survival")),
            MenuItem(portal_text, action=lambda: self._set_mode("portal")),
            MenuItem("Back", action=lambda: "back")
        ]
        return Menu("SELECT GAME MODE", items, self.main_menu)
        
    def _create_settings_menu(self) -> Menu:
        """설정 메뉴 생성"""
        items = [
            MenuItem("Sound: ON" if self.settings['sound'] else "Sound: OFF",
                    action=lambda: self._toggle_setting("sound")),
            MenuItem("Music: ON" if self.settings['music'] else "Music: OFF",
                    action=lambda: self._toggle_setting("music")),
            MenuItem("Grid: ON" if self.settings['grid'] else "Grid: OFF",
                    action=lambda: self._toggle_setting("grid")),
            MenuItem("Controls: Arrow Keys" if self.settings['controls'] == 'arrows' 
                    else "Controls: WASD",
                    action=lambda: self._toggle_setting("controls")),
            MenuItem("Back", action=lambda: "back")
        ]
        return Menu("SETTINGS", items, self.main_menu)
        
    def _update_settings_menu(self) -> None:
        """설정 메뉴의 텍스트 업데이트"""
        if self.current_menu and self.current_menu.title == "SETTINGS":
            items = self.current_menu.items
            items[0].text = "Sound: ON" if self.settings['sound'] else "Sound: OFF"
            items[1].text = "Music: ON" if self.settings['music'] else "Music: OFF"
            items[2].text = "Grid: ON" if self.settings['grid'] else "Grid: OFF"
            items[3].text = ("Controls: Arrow Keys" if self.settings['controls'] == 'arrows' 
                           else "Controls: WASD")
    
    def _update_difficulty_menu(self) -> None:
        """난이도 메뉴의 텍스트 업데이트"""
        if self.current_menu and self.current_menu.title == "SELECT DIFFICULTY":
            items = self.current_menu.items
            items[0].text = "✓ Easy - Slow speed, no obstacles" if self.selected_difficulty == "easy" else "  Easy - Slow speed, no obstacles"
            items[1].text = "✓ Normal - Medium speed" if self.selected_difficulty == "normal" else "  Normal - Medium speed"
            items[2].text = "✓ Hard - Fast speed, obstacles" if self.selected_difficulty == "hard" else "  Hard - Fast speed, obstacles"
        
        # 메인 메뉴의 난이도 항목도 업데이트
        if hasattr(self, 'main_menu'):
            self.main_menu.items[1].text = f"Difficulty (Current: {self.selected_difficulty.capitalize()})"
    
    def _update_mode_menu(self) -> None:
        """게임 모드 메뉴의 텍스트 업데이트"""
        if self.current_menu and self.current_menu.title == "SELECT GAME MODE":
            items = self.current_menu.items
            items[0].text = "✓ Classic - Traditional snake" if self.selected_mode == "classic" else "  Classic - Traditional snake"
            items[1].text = "✓ Time Attack - 60 seconds" if self.selected_mode == "time_attack" else "  Time Attack - 60 seconds"
            items[2].text = "✓ Survival - Increasing obstacles" if self.selected_mode == "survival" else "  Survival - Increasing obstacles"
            items[3].text = "✓ Portal - Wrap around walls" if self.selected_mode == "portal" else "  Portal - Wrap around walls"
        
        # 메인 메뉴의 모드 항목도 업데이트
        if hasattr(self, 'main_menu'):
            self.main_menu.items[2].text = f"Game Mode (Current: {self.selected_mode.replace('_', ' ').title()})"
    
    def _set_difficulty(self, difficulty: str) -> str:
        """난이도 설정"""
        self.selected_difficulty = difficulty
        self._update_difficulty_menu()
        return "stay"
        
    def _set_mode(self, mode: str) -> str:
        """게임 모드 설정"""
        self.selected_mode = mode
        self._update_mode_menu()
        return "stay"
        
    def _toggle_setting(self, setting: str) -> str:
        """설정 토글"""
        if setting == "controls":
            self.settings[setting] = "wasd" if self.settings[setting] == "arrows" else "arrows"
        else:
            self.settings[setting] = not self.settings[setting]
        
        # 현재 설정 메뉴의 텍스트만 업데이트
        self._update_settings_menu()
        return "stay"
        
    def handle_input(self, event: pygame.event.Event) -> Optional[str]:
        """
        입력 처리
        
        Args:
            event: 이벤트
            
        Returns:
            액션
        """
        if self.current_menu is None:
            return None
            
        result = self.current_menu.handle_input(event)
        
        if result == "back":
            self._go_back()
        elif result == "submenu":
            submenu = self.current_menu.get_selected_item().submenu
            if submenu:
                self._push_menu(submenu)
        elif result == "stay":
            pass
        else:
            return result
            
        return None
        
    def _push_menu(self, menu: Menu) -> None:
        """메뉴 스택에 추가"""
        self.menu_stack.append(menu)
        self.current_menu = menu
        
    def _go_back(self) -> None:
        """이전 메뉴로 돌아가기"""
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            self.current_menu = self.menu_stack[-1]
            
    def draw(self, surface: pygame.Surface) -> None:
        """메뉴 그리기"""
        if self.current_menu:
            self.current_menu.draw(surface)
            
    def get_selected_difficulty(self) -> str:
        """선택된 난이도 반환"""
        return self.selected_difficulty
        
    def get_selected_mode(self) -> str:
        """선택된 게임 모드 반환"""
        return self.selected_mode
        
    def get_settings(self) -> dict:
        """설정 반환"""
        return self.settings.copy()
