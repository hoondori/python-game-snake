"""ScoreManager 단위 테스트"""
import pytest
import os
import json
import time
from score_manager import ScoreManager


class TestScoreManager:
    """ScoreManager 클래스 테스트"""
    
    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.test_file = 'test_highscore.json'
        self.score_manager = ScoreManager(self.test_file)
    
    def teardown_method(self):
        """각 테스트 메서드 실행 후 정리"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_initial_score(self):
        """초기 점수가 0인지 확인"""
        assert self.score_manager.get_score() == 0
    
    def test_add_food_basic(self):
        """먹이 먹었을 때 기본 점수 추가"""
        self.score_manager.add_food()
        assert self.score_manager.get_score() == 10
        assert self.score_manager.get_food_eaten() == 1
    
    def test_add_food_combo(self):
        """콤보 점수 계산"""
        # 첫 번째 먹이
        self.score_manager.add_food()
        assert self.score_manager.get_score() == 10
        
        # 3초 이내에 두 번째 먹이 (콤보)
        time.sleep(0.5)
        self.score_manager.add_food()
        assert self.score_manager.get_score() == 25  # 10 + 15 (콤보 보너스)
        assert self.score_manager.is_combo_active() == True
    
    def test_add_food_no_combo(self):
        """콤보 타임아웃 후 일반 점수"""
        # 첫 번째 먹이
        self.score_manager.add_food()
        assert self.score_manager.get_score() == 10
        
        # 3초 대기 후 두 번째 먹이 (콤보 아님)
        time.sleep(3.5)
        self.score_manager.add_food()
        assert self.score_manager.get_score() == 20  # 10 + 10
        assert self.score_manager.is_combo_active() == False
    
    def test_high_score_save_load(self):
        """최고 점수 저장 및 로드"""
        # 점수 추가
        for _ in range(5):
            self.score_manager.add_food()
        
        current_score = self.score_manager.get_score()
        
        # 새 인스턴스 생성하여 로드
        new_manager = ScoreManager(self.test_file)
        assert new_manager.get_high_score() == current_score
    
    def test_high_score_not_updated_if_lower(self):
        """최고 점수보다 낮으면 갱신 안 됨"""
        # 높은 점수 설정
        for _ in range(10):
            self.score_manager.add_food()
        
        high = self.score_manager.get_high_score()
        
        # 리셋 후 낮은 점수
        self.score_manager.reset()
        self.score_manager.add_food()
        
        assert self.score_manager.get_high_score() == high
    
    def test_reset(self):
        """리셋 기능 확인"""
        # 점수 올리기
        for _ in range(5):
            self.score_manager.add_food()
        
        # 리셋
        self.score_manager.reset()
        
        assert self.score_manager.get_score() == 0
        assert self.score_manager.get_food_eaten() == 0
        assert self.score_manager.is_combo_active() == False
    
    def test_play_time(self):
        """플레이 시간 측정"""
        time.sleep(1)
        play_time = self.score_manager.get_play_time()
        assert play_time >= 1
    
    def test_end_game_freezes_time(self):
        """게임 종료 시 플레이 시간 고정"""
        time.sleep(1)
        self.score_manager.end_game()
        frozen_time = self.score_manager.get_play_time()
        
        # 시간이 지나도 플레이 시간은 고정되어야 함
        time.sleep(1)
        assert self.score_manager.get_play_time() == frozen_time
    
    def test_no_highscore_file(self):
        """최고 점수 파일이 없을 때 기본값 0"""
        manager = ScoreManager('nonexistent_file.json')
        assert manager.get_high_score() == 0
