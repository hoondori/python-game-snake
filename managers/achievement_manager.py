"""업적 관리 시스템 (JSON)"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class Achievement:
    """업적 클래스"""
    
    def __init__(self, achievement_id: str, name: str, description: str, 
                 condition: str, unlocked: bool = False):
        """
        업적 초기화
        
        Args:
            achievement_id: 업적 ID
            name: 업적 이름
            description: 업적 설명
            condition: 잠금 해제 조건
            unlocked: 잠금 해제 여부
        """
        self.id = achievement_id
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = unlocked
        self.unlocked_at: Optional[str] = None
        
    def unlock(self) -> None:
        """업적 잠금 해제"""
        if not self.unlocked:
            self.unlocked = True
            self.unlocked_at = datetime.now().isoformat()
            
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'condition': self.condition,
            'unlocked': self.unlocked,
            'unlocked_at': self.unlocked_at
        }
        
    @staticmethod
    def from_dict(data: Dict) -> 'Achievement':
        """딕셔너리에서 생성"""
        achievement = Achievement(
            data['id'],
            data['name'],
            data['description'],
            data['condition'],
            data.get('unlocked', False)
        )
        achievement.unlocked_at = data.get('unlocked_at')
        return achievement


class AchievementManager:
    """업적 관리 클래스"""
    
    # 기본 업적 정의
    DEFAULT_ACHIEVEMENTS = {
        'first_bite': {
            'name': 'First Bite',
            'description': 'Eat your first food item and start growing',
            'condition': 'food_eaten >= 1'
        },
        'growing_up': {
            'name': 'Growing Up',
            'description': 'Grow your snake to a length of 10 segments',
            'condition': 'snake_length >= 10'
        },
        'snake_master': {
            'name': 'Snake Master',
            'description': 'Achieve an impressive snake length of 30 segments',
            'condition': 'snake_length >= 30'
        },
        'speed_demon': {
            'name': 'Speed Demon',
            'description': 'Reach the maximum game speed by eating enough food',
            'condition': 'reached_max_speed'
        },
        'survivor': {
            'name': 'Survivor',
            'description': 'Stay alive for 5 minutes in Survival mode',
            'condition': 'survival_time >= 300'
        },
        'time_master': {
            'name': 'Time Master',
            'description': 'Score 100 points in Time Attack mode (60 seconds)',
            'condition': 'time_attack_score >= 100'
        },
        'golden_hunter': {
            'name': 'Golden Hunter',
            'description': 'Collect 10 rare Golden Apples (worth 50 points each)',
            'condition': 'golden_apples >= 10'
        },
        'invincible_pass': {
            'name': 'Invincible',
            'description': 'Pass through obstacles using the invincibility power-up',
            'condition': 'invincible_obstacle_pass'
        },
        'power_collector': {
            'name': 'Power Collector',
            'description': 'Collect 20 power-ups during your gameplay',
            'condition': 'powerups_collected >= 20'
        },
        'score_100': {
            'name': 'Century',
            'description': 'Reach a score of 100 points in any game mode',
            'condition': 'score >= 100'
        },
        'score_500': {
            'name': 'High Achiever',
            'description': 'Reach an impressive score of 500 points',
            'condition': 'score >= 500'
        }
    }
    
    def __init__(self, file_path: str = "data/achievements.json"):
        """
        업적 매니저 초기화
        
        Args:
            file_path: 업적 데이터 파일 경로
        """
        self.file_path = file_path
        self.achievements: Dict[str, Achievement] = {}
        self.newly_unlocked: List[Achievement] = []
        self._ensure_directory()
        self._load_or_create()
        
    def _ensure_directory(self) -> None:
        """데이터 디렉토리 생성"""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
    def _load_or_create(self) -> None:
        """업적 데이터 로드 또는 생성"""
        if os.path.exists(self.file_path):
            self._load()
        else:
            self._create_default()
            self._save()
            
    def _create_default(self) -> None:
        """기본 업적 생성"""
        for achievement_id, data in self.DEFAULT_ACHIEVEMENTS.items():
            self.achievements[achievement_id] = Achievement(
                achievement_id,
                data['name'],
                data['description'],
                data['condition']
            )
            
    def _load(self) -> None:
        """업적 데이터 로드"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 기존 업적 로드
            for achievement_data in data.get('achievements', []):
                achievement = Achievement.from_dict(achievement_data)
                self.achievements[achievement.id] = achievement
                
            # 새로운 업적 추가
            for achievement_id, achievement_data in self.DEFAULT_ACHIEVEMENTS.items():
                if achievement_id not in self.achievements:
                    self.achievements[achievement_id] = Achievement(
                        achievement_id,
                        achievement_data['name'],
                        achievement_data['description'],
                        achievement_data['condition']
                    )
        except (json.JSONDecodeError, IOError):
            self._create_default()
            
    def _save(self) -> None:
        """업적 데이터 저장"""
        data = {
            'achievements': [a.to_dict() for a in self.achievements.values()]
        }
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def check_and_unlock(self, **conditions) -> List[Achievement]:
        """
        조건 확인 및 업적 잠금 해제
        
        Args:
            **conditions: 조건 키워드 인자
            
        Returns:
            새로 잠금 해제된 업적 리스트
        """
        self.newly_unlocked.clear()
        
        for achievement in self.achievements.values():
            if not achievement.unlocked:
                if self._check_condition(achievement.id, conditions):
                    achievement.unlock()
                    self.newly_unlocked.append(achievement)
                    
        if self.newly_unlocked:
            self._save()
            
        return self.newly_unlocked.copy()
        
    def _check_condition(self, achievement_id: str, conditions: Dict) -> bool:
        """
        특정 업적의 조건 확인
        
        Args:
            achievement_id: 업적 ID
            conditions: 현재 조건들
            
        Returns:
            조건 만족 여부
        """
        # 먹이 관련
        if achievement_id == 'first_bite':
            return conditions.get('food_eaten', 0) >= 1
        elif achievement_id == 'growing_up':
            return conditions.get('snake_length', 0) >= 10
        elif achievement_id == 'snake_master':
            return conditions.get('snake_length', 0) >= 30
            
        # 속도 관련
        elif achievement_id == 'speed_demon':
            return conditions.get('reached_max_speed', False)
            
        # 모드 관련
        elif achievement_id == 'survivor':
            return conditions.get('survival_time', 0) >= 300
        elif achievement_id == 'time_master':
            return conditions.get('time_attack_score', 0) >= 100
            
        # 수집 관련
        elif achievement_id == 'golden_hunter':
            return conditions.get('golden_apples', 0) >= 10
        elif achievement_id == 'invincible_pass':
            return conditions.get('invincible_obstacle_pass', False)
        elif achievement_id == 'power_collector':
            return conditions.get('powerups_collected', 0) >= 20
            
        # 점수 관련
        elif achievement_id == 'score_100':
            return conditions.get('score', 0) >= 100
        elif achievement_id == 'score_500':
            return conditions.get('score', 0) >= 500
            
        return False
        
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """특정 업적 가져오기"""
        return self.achievements.get(achievement_id)
        
    def get_all_achievements(self) -> List[Achievement]:
        """모든 업적 가져오기"""
        return list(self.achievements.values())
        
    def get_unlocked_achievements(self) -> List[Achievement]:
        """잠금 해제된 업적 가져오기"""
        return [a for a in self.achievements.values() if a.unlocked]
        
    def get_locked_achievements(self) -> List[Achievement]:
        """잠긴 업적 가져오기"""
        return [a for a in self.achievements.values() if not a.unlocked]
        
    def get_progress(self) -> Dict[str, int]:
        """
        업적 진행도 가져오기
        
        Returns:
            {'unlocked': 잠금 해제 수, 'total': 전체 수, 'percentage': 퍼센트}
        """
        total = len(self.achievements)
        unlocked = len([a for a in self.achievements.values() if a.unlocked])
        percentage = int((unlocked / total) * 100) if total > 0 else 0
        
        return {
            'unlocked': unlocked,
            'total': total,
            'percentage': percentage
        }
        
    def reset_achievements(self) -> None:
        """모든 업적 초기화"""
        for achievement in self.achievements.values():
            achievement.unlocked = False
            achievement.unlocked_at = None
        self._save()
        
    def get_newly_unlocked(self) -> List[Achievement]:
        """최근 잠금 해제된 업적 가져오기"""
        return self.newly_unlocked.copy()
