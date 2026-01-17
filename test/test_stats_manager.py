"""StatsManager 테스트"""
import pytest
import os
from managers.stats_manager import StatsManager


@pytest.fixture
def temp_stats_db(tmp_path):
    """임시 데이터베이스 경로"""
    return str(tmp_path / "test_stats.db")


def test_stats_manager_initialization(temp_stats_db):
    """StatsManager 초기화 테스트"""
    manager = StatsManager(temp_stats_db)
    assert os.path.exists(temp_stats_db)


def test_record_game(temp_stats_db):
    """게임 기록 테스트"""
    manager = StatsManager(temp_stats_db)
    manager.record_game(120.0, 10, 2, 3)
    
    stats = manager.get_global_stats()
    assert stats['total_playtime'] == 120.0
    assert stats['total_games'] == 1
    assert stats['total_food_eaten'] == 10
    assert stats['total_golden_apples'] == 2
    assert stats['total_powerups_collected'] == 3


def test_difficulty_highscore(temp_stats_db):
    """난이도별 최고 점수 테스트"""
    manager = StatsManager(temp_stats_db)
    
    # 첫 기록
    is_new = manager.update_difficulty_highscore("easy", 100)
    assert is_new
    
    # 더 낮은 점수
    is_new = manager.update_difficulty_highscore("easy", 50)
    assert not is_new
    
    # 더 높은 점수
    is_new = manager.update_difficulty_highscore("easy", 150)
    assert is_new
    
    # 최고 점수 확인
    score, _ = manager.get_difficulty_highscore("easy")
    assert score == 150


def test_mode_highscore(temp_stats_db):
    """모드별 최고 점수 테스트"""
    manager = StatsManager(temp_stats_db)
    
    manager.update_mode_highscore("classic", 200)
    manager.update_mode_highscore("time_attack", 300)
    
    score1, _ = manager.get_mode_highscore("classic")
    score2, _ = manager.get_mode_highscore("time_attack")
    
    assert score1 == 200
    assert score2 == 300


def test_survival_time(temp_stats_db):
    """생존 시간 기록 테스트"""
    manager = StatsManager(temp_stats_db)
    
    manager.record_survival_time(120.5)
    manager.record_survival_time(200.3)
    manager.record_survival_time(150.7)
    
    longest, _ = manager.get_longest_survival_time()
    assert longest == 200.3


def test_reset_stats(temp_stats_db):
    """통계 초기화 테스트"""
    manager = StatsManager(temp_stats_db)
    
    # 데이터 추가
    manager.record_game(100.0, 10, 1, 2)
    manager.update_difficulty_highscore("hard", 500)
    
    # 초기화
    manager.reset_stats()
    
    # 확인
    stats = manager.get_global_stats()
    assert stats['total_games'] == 0
    
    score, _ = manager.get_difficulty_highscore("hard")
    assert score == 0
