"""사운드 관리 클래스"""
import pygame
import os


class SoundManager:
    def __init__(self):
        """사운드 관리자 초기화"""
        # 사운드 시스템 초기화
        pygame.mixer.init()
        
        # 사운드 활성화 상태
        self.sound_enabled = True
        self.music_enabled = True
        
        # 사운드 파일 경로
        self.sounds_dir = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
        
        # 사운드 로드
        self.eat_sound = self._create_eat_sound()
        self.game_over_sound = self._create_game_over_sound()
        
        # 배경 음악은 별도로 관리 (pygame.mixer.music 사용)
        self.background_music_loaded = False
    
    def _create_eat_sound(self):
        """먹이 먹는 소리 생성 (프로그래매틱 사운드)"""
        try:
            # 짧은 비프음 생성 (440Hz, 0.1초)
            frequency = 600
            duration = 0.1
            sample_rate = 22050
            
            import numpy as np
            samples = int(sample_rate * duration)
            wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))
            # 볼륨 조절 및 페이드 아웃
            fade = np.linspace(1.0, 0.0, samples)
            wave = wave * fade * 0.3  # 볼륨 30%
            
            # 16비트 정수로 변환
            wave = (wave * 32767).astype(np.int16)
            
            # 스테레오로 변환
            stereo_wave = np.column_stack((wave, wave))
            
            # pygame Sound 객체 생성
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            print(f"먹이 사운드 생성 실패: {e}")
            return None
    
    def _create_game_over_sound(self):
        """게임 오버 소리 생성 (프로그래매틱 사운드)"""
        try:
            # 하강하는 톤 (500Hz -> 200Hz, 0.5초)
            sample_rate = 22050
            duration = 0.5
            
            import numpy as np
            samples = int(sample_rate * duration)
            # 주파수가 점점 낮아지는 효과
            frequencies = np.linspace(500, 200, samples)
            time_points = np.linspace(0, duration, samples)
            
            wave = np.zeros(samples)
            for i in range(samples):
                wave[i] = np.sin(2 * np.pi * frequencies[i] * time_points[i])
            
            # 페이드 아웃
            fade = np.linspace(1.0, 0.0, samples)
            wave = wave * fade * 0.3
            
            # 16비트 정수로 변환
            wave = (wave * 32767).astype(np.int16)
            
            # 스테레오로 변환
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            print(f"게임 오버 사운드 생성 실패: {e}")
            return None
    
    def play_eat_sound(self):
        """먹이 먹는 소리 재생"""
        if self.sound_enabled and self.eat_sound:
            self.eat_sound.play()
    
    def play_game_over_sound(self):
        """게임 오버 소리 재생"""
        if self.sound_enabled and self.game_over_sound:
            self.game_over_sound.play()
    
    def start_background_music(self):
        """배경 음악 시작"""
        if not self.music_enabled:
            return
        
        try:
            # desert-snake.wav 파일 로드
            music_file = os.path.join(os.path.dirname(__file__), 'desert-snake.wav')
            
            if not os.path.exists(music_file):
                print(f"배경 음악 파일을 찾을 수 없습니다: {music_file}")
                return
            
            # 배경 음악 로드 및 재생
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # 무한 반복
            self.background_music_loaded = True
            
        except Exception as e:
            print(f"배경 음악 로드 실패: {e}")
    
    def stop_background_music(self):
        """배경 음악 정지"""
        if self.background_music_loaded:
            pygame.mixer.music.stop()
    
    def toggle_sound(self):
        """사운드 효과 ON/OFF 토글"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """배경 음악 ON/OFF 토글"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled and not pygame.mixer.music.get_busy():
            self.start_background_music()
        elif not self.music_enabled:
            self.stop_background_music()
        return self.music_enabled
    
    def is_sound_enabled(self):
        """사운드 효과 활성화 여부"""
        return self.sound_enabled
    
    def is_music_enabled(self):
        """배경 음악 활성화 여부"""
        return self.music_enabled
