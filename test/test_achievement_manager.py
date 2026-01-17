"""AchievementManager 테스트"""
import pytest
import os
import json
from managers.achievement_manager import AchievementManager, Achievement


@pytest.fixture
def temp_achievement_file(tmp_path):
    """임시 업적 파일 경로"""
    return str(tmp_path / "test_achievements.json")


def test_achievement_creation():
    """업적 생성 테스트"""
    achievement = Achievement("test_id", "Test Achievement", 
                            "Test Description", "test_condition")
    assert achievement.id == "test_id"
    assert achievement.name == "Test Achievement"
    assert not achievement.unlocked


def test_achievement_unlock():
    """업적 잠금 해제 테스트"""
    achievement = Achievement("test_id", "Test", "Desc", "cond")
    achievement.unlock()
    
    assert achievement.unlocked
    assert achievement.unlocked_at is not None


def test_achievement_manager_initialization(temp_achievement_file):
    """AchievementManager 초기화 테스트"""
    manager = AchievementManager(temp_achievement_file)
    assert os.path.exists(temp_achievement_file)
    assert len(manager.achievements) > 0


def test_check_first_bite(temp_achievement_file):
    """First Bite 업적 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    newly_unlocked = manager.check_and_unlock(food_eaten=1)
    
    assert len(newly_unlocked) > 0
    first_bite = manager.get_achievement('first_bite')
    assert first_bite.unlocked


def test_check_growing_up(temp_achievement_file):
    """Growing Up 업적 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    newly_unlocked = manager.check_and_unlock(snake_length=10)
    
    growing_up = manager.get_achievement('growing_up')
    assert growing_up.unlocked


def test_check_snake_master(temp_achievement_file):
    """Snake Master 업적 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    manager.check_and_unlock(snake_length=30)
    
    snake_master = manager.get_achievement('snake_master')
    assert snake_master.unlocked


def test_check_score_achievements(temp_achievement_file):
    """점수 관련 업적 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    # 100점
    manager.check_and_unlock(score=100)
    score_100 = manager.get_achievement('score_100')
    assert score_100.unlocked
    
    # 500점
    manager.check_and_unlock(score=500)
    score_500 = manager.get_achievement('score_500')
    assert score_500.unlocked


def test_check_golden_hunter(temp_achievement_file):
    """Golden Hunter 업적 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    manager.check_and_unlock(golden_apples=10)
    
    golden_hunter = manager.get_achievement('golden_hunter')
    assert golden_hunter.unlocked


def test_check_survivor(temp_achievement_file):
    """Survivor 업적 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    manager.check_and_unlock(survival_time=300)
    
    survivor = manager.get_achievement('survivor')
    assert survivor.unlocked


def test_get_progress(temp_achievement_file):
    """업적 진행도 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    # 일부 업적 잠금 해제
    manager.check_and_unlock(food_eaten=1, snake_length=10)
    
    progress = manager.get_progress()
    assert progress['unlocked'] >= 2
    assert progress['total'] > 0
    assert 0 <= progress['percentage'] <= 100


def test_reset_achievements(temp_achievement_file):
    """업적 초기화 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    # 업적 잠금 해제
    manager.check_and_unlock(food_eaten=1)
    
    # 초기화
    manager.reset_achievements()
    
    # 확인
    unlocked = manager.get_unlocked_achievements()
    assert len(unlocked) == 0


def test_newly_unlocked_list(temp_achievement_file):
    """최근 잠금 해제 목록 테스트"""
    manager = AchievementManager(temp_achievement_file)
    
    newly_unlocked = manager.check_and_unlock(
        food_eaten=1, 
        snake_length=10, 
        score=100
    )
    
    assert len(newly_unlocked) >= 3
    
    # 다시 확인 (이미 잠금 해제됨)
    newly_unlocked2 = manager.check_and_unlock(
        food_eaten=1,
        snake_length=10,
        score=100
    )
    
    assert len(newly_unlocked2) == 0
