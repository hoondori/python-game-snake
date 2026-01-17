"""기본 게임 모드 클래스"""
from abc import ABC, abstractmethod
from typing import Tuple, Optional
import pygame


class BaseMode(ABC):
    """모든 게임 모드의 기본 클래스"""
    
    def __init__(self, name: str, description: str):
        """
        게임 모드 초기화
        
        Args:
            name: 모드 이름
            description: 모드 설명
        """
        self.name = name
        self.description = description
        self.active = False
        
    @abstractmethod
    def setup(self, game) -> None:
        """
        게임 모드 설정
        
        Args:
            game: 게임 인스턴스
        """
        pass
        
    @abstractmethod
    def update(self, game) -> None:
        """
        게임 모드 업데이트 (매 프레임)
        
        Args:
            game: 게임 인스턴스
        """
        pass
        
    @abstractmethod
    def check_game_over(self, game) -> Tuple[bool, Optional[str]]:
        """
        게임 오버 조건 확인
        
        Args:
            game: 게임 인스턴스
            
        Returns:
            (게임 오버 여부, 메시지)
        """
        pass
        
    @abstractmethod
    def draw_hud(self, surface: pygame.Surface, game) -> None:
        """
        모드별 HUD 그리기
        
        Args:
            surface: 그릴 화면
            game: 게임 인스턴스
        """
        pass
        
    def activate(self) -> None:
        """모드 활성화"""
        self.active = True
        
    def deactivate(self) -> None:
        """모드 비활성화"""
        self.active = False
        
    def get_score_multiplier(self) -> float:
        """
        모드별 점수 배율
        
        Returns:
            점수 배율
        """
        return 1.0
        
    def is_active(self) -> bool:
        """모드 활성 상태 확인"""
        return self.active
