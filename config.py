"""설정 관리 클래스"""
import json
import os


class ConfigManager:
    def __init__(self, config_file='config.json'):
        """설정 관리자 초기화"""
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """설정 파일 로드"""
        default_config = {
            'difficulty': 'normal',
            'portal_mode': False,
            'sound_enabled': True,
            'music_enabled': True
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # 기본값과 병합 (누락된 키 처리)
                    return {**default_config, **loaded_config}
        except (json.JSONDecodeError, IOError) as e:
            print(f"설정 파일 로드 실패: {e}, 기본값 사용")
        
        return default_config
    
    def save_config(self):
        """설정 파일 저장"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"설정 파일 저장 실패: {e}")
    
    def get(self, key, default=None):
        """설정값 가져오기"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """설정값 변경 및 저장"""
        self.config[key] = value
        self.save_config()
    
    def get_difficulty(self):
        """난이도 반환"""
        return self.config.get('difficulty', 'normal')
    
    def set_difficulty(self, difficulty):
        """난이도 설정"""
        if difficulty in ['easy', 'normal', 'hard']:
            self.set('difficulty', difficulty)
    
    def is_portal_mode(self):
        """포탈 모드 여부 반환"""
        return self.config.get('portal_mode', False)
    
    def toggle_portal_mode(self):
        """포탈 모드 토글"""
        current = self.is_portal_mode()
        self.set('portal_mode', not current)
        return not current
