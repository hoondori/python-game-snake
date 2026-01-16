"""점수 관리 클래스"""
import json
import os
import time


class ScoreManager:
    def __init__(self, highscore_file='highscore.json'):
        """점수 관리자 초기화"""
        self.highscore_file = highscore_file
        self.score = 0
        self.high_score = self.load_high_score()
        self.food_eaten = 0
        self.start_time = time.time()
        self.end_time = None  # 게임 종료 시간
        self.last_food_time = time.time()
        self.combo_active = False
        self.combo_timeout = 3.0  # 3초 이내에 먹어야 콤보
    
    def load_high_score(self):
        """최고 점수 로드"""
        try:
            if os.path.exists(self.highscore_file):
                with open(self.highscore_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except (json.JSONDecodeError, IOError):
            pass
        return 0
    
    def save_high_score(self):
        """최고 점수 저장"""
        try:
            with open(self.highscore_file, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except IOError:
            pass
    
    def add_food(self):
        """먹이를 먹었을 때 점수 추가"""
        current_time = time.time()
        base_points = 10
        
        # 첫 번째 먹이가 아니고 3초 이내에 먹으면 콤보
        if self.food_eaten > 0 and current_time - self.last_food_time <= self.combo_timeout:
            self.score += base_points + 5  # 콤보 보너스
            self.combo_active = True
        else:
            self.score += base_points
            self.combo_active = False
        
        self.food_eaten += 1
        self.last_food_time = current_time
        
        # 최고 점수 갱신
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def get_score(self):
        """현재 점수 반환"""
        return self.score
    
    def get_high_score(self):
        """최고 점수 반환"""
        return self.high_score
    
    def get_food_eaten(self):
        """먹은 먹이 개수 반환"""
        return self.food_eaten
    
    def get_play_time(self):
        """플레이 시간 반환 (초)"""
        if self.end_time is not None:
            # 게임 오버 후에는 고정된 시간 반환
            return int(self.end_time - self.start_time)
        return int(time.time() - self.start_time)
    
    def end_game(self):
        """게임 종료 시점 기록"""
        if self.end_time is None:
            self.end_time = time.time()
    
    def is_combo_active(self):
        """콤보 활성 여부 반환"""
        return self.combo_active
    
    def reset(self):
        """점수 리셋 (재시작 시)"""
        self.score = 0
        self.food_eaten = 0
        self.start_time = time.time()
        self.end_time = None
        self.last_food_time = time.time()
        self.combo_active = False
