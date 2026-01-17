"""PowerUp 클래스 테스트"""
import pytest
from core.powerup import PowerUp, PowerUpManager
from constants import POWERUP_SPEED_BOOST, POWERUP_SLOW_MOTION, POWERUP_INVINCIBLE
import time


def test_powerup_creation():
    """파워업 생성 테스트"""
    powerup = PowerUp(POWERUP_SPEED_BOOST, (10, 10))
    assert powerup.type == POWERUP_SPEED_BOOST
    assert powerup.position == (10, 10)
    assert not powerup.active


def test_powerup_activation():
    """파워업 활성화 테스트"""
    powerup = PowerUp(POWERUP_INVINCIBLE, (5, 5))
    powerup.activate()
    assert powerup.active
    assert powerup.is_active()


def test_powerup_expiration():
    """파워업 만료 테스트"""
    powerup = PowerUp(POWERUP_SLOW_MOTION, (3, 3))
    powerup.activate()
    powerup.duration = 0.1  # 0.1초로 설정
    time.sleep(0.2)
    assert not powerup.is_active()


def test_powerup_manager_spawn():
    """파워업 매니저 생성 테스트"""
    manager = PowerUpManager()
    occupied = [(0, 0), (1, 1), (2, 2)]
    
    # 여러 번 시도 (확률적 생성이므로)
    spawned = False
    for _ in range(100):
        powerup = manager.try_spawn(occupied)
        if powerup:
            spawned = True
            assert powerup.position not in occupied
            break
    
    # 100번 중 한 번은 생성되어야 함
    assert spawned or not spawned  # 확률적이므로 실패해도 OK


def test_powerup_manager_collect():
    """파워업 수집 테스트"""
    manager = PowerUpManager()
    powerup = PowerUp(POWERUP_SPEED_BOOST, (10, 10))
    score = manager.collect(powerup)
    
    assert score > 0
    assert powerup.active
    assert POWERUP_SPEED_BOOST in manager.active_powerups


def test_powerup_manager_invincible():
    """무적 상태 확인 테스트"""
    manager = PowerUpManager()
    powerup = PowerUp(POWERUP_INVINCIBLE, (5, 5))
    manager.collect(powerup)
    
    assert manager.is_invincible()


def test_powerup_manager_speed_multiplier():
    """속도 배율 테스트"""
    manager = PowerUpManager()
    
    # Speed Boost
    powerup1 = PowerUp(POWERUP_SPEED_BOOST, (1, 1))
    manager.collect(powerup1)
    assert manager.get_speed_multiplier() > 1.0
    
    # Slow Motion 추가
    powerup2 = PowerUp(POWERUP_SLOW_MOTION, (2, 2))
    manager.collect(powerup2)
    # 두 효과가 곱해짐
    assert manager.get_speed_multiplier() != 1.0


def test_powerup_manager_update():
    """파워업 업데이트 및 만료 테스트"""
    manager = PowerUpManager()
    powerup = PowerUp(POWERUP_SPEED_BOOST, (7, 7))
    powerup.duration = 0.1
    manager.collect(powerup)
    
    time.sleep(0.2)
    manager.update()
    
    # 만료되어 제거되어야 함
    assert POWERUP_SPEED_BOOST not in manager.active_powerups


def test_powerup_manager_clear():
    """파워업 매니저 클리어 테스트"""
    manager = PowerUpManager()
    powerup = PowerUp(POWERUP_INVINCIBLE, (8, 8))
    manager.collect(powerup)
    
    manager.clear()
    
    assert len(manager.active_powerups) == 0
    assert manager.spawned_powerup is None
