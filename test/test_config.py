"""ConfigManager 테스트"""
import pytest
import os
import json
from config import ConfigManager


class TestConfigManager:
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.test_config_file = 'test_config.json'
        # 기존 테스트 파일 삭제
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)
    
    def teardown_method(self):
        """각 테스트 후에 실행"""
        # 테스트 파일 삭제
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)
    
    def test_default_config(self):
        """기본 설정 로드 테스트"""
        config_manager = ConfigManager(self.test_config_file)
        
        assert config_manager.get('difficulty') == 'normal'
        assert config_manager.get('portal_mode') == False
        assert config_manager.get('sound_enabled') == True
        assert config_manager.get('music_enabled') == True
    
    def test_save_and_load_config(self):
        """설정 저장 및 로드 테스트"""
        config_manager = ConfigManager(self.test_config_file)
        config_manager.set('difficulty', 'hard')
        config_manager.set('portal_mode', True)
        
        # 새 인스턴스로 로드
        new_config_manager = ConfigManager(self.test_config_file)
        assert new_config_manager.get('difficulty') == 'hard'
        assert new_config_manager.get('portal_mode') == True
    
    def test_difficulty_methods(self):
        """난이도 관련 메서드 테스트"""
        config_manager = ConfigManager(self.test_config_file)
        
        assert config_manager.get_difficulty() == 'normal'
        
        config_manager.set_difficulty('easy')
        assert config_manager.get_difficulty() == 'easy'
        
        config_manager.set_difficulty('hard')
        assert config_manager.get_difficulty() == 'hard'
    
    def test_portal_mode_toggle(self):
        """포탈 모드 토글 테스트"""
        config_manager = ConfigManager(self.test_config_file)
        
        assert config_manager.is_portal_mode() == False
        
        result = config_manager.toggle_portal_mode()
        assert result == True
        assert config_manager.is_portal_mode() == True
        
        result = config_manager.toggle_portal_mode()
        assert result == False
        assert config_manager.is_portal_mode() == False
    
    def test_invalid_difficulty(self):
        """잘못된 난이도 설정 테스트"""
        config_manager = ConfigManager(self.test_config_file)
        original_difficulty = config_manager.get_difficulty()
        
        # 잘못된 난이도는 설정되지 않아야 함
        config_manager.set_difficulty('invalid')
        assert config_manager.get_difficulty() == original_difficulty
    
    def test_corrupted_config_file(self):
        """손상된 설정 파일 처리 테스트"""
        # 잘못된 JSON 파일 생성
        with open(self.test_config_file, 'w') as f:
            f.write("{ invalid json }")
        
        # 기본값으로 로드되어야 함
        config_manager = ConfigManager(self.test_config_file)
        assert config_manager.get('difficulty') == 'normal'
