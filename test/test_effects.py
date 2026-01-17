"""Effects 시스템 테스트"""
import pytest
from ui.effects import Particle, ParticleSystem, AnimationEffect


def test_particle_creation():
    """파티클 생성 테스트"""
    particle = Particle(100, 100, (255, 0, 0), (1.0, -1.0), 30)
    assert particle.x == 100
    assert particle.y == 100
    assert particle.lifetime == 30


def test_particle_update():
    """파티클 업데이트 테스트"""
    particle = Particle(100, 100, (255, 0, 0), (2.0, -2.0), 30)
    
    # 업데이트
    is_alive = particle.update()
    
    assert is_alive
    assert particle.x != 100  # 위치가 변경되어야 함
    assert particle.lifetime < 30


def test_particle_death():
    """파티클 소멸 테스트"""
    particle = Particle(100, 100, (255, 0, 0), (1.0, 1.0), 1)
    
    # 한 번 업데이트 후 소멸
    particle.update()
    is_alive = particle.update()
    
    assert not is_alive


def test_particle_system_explosion():
    """파티클 시스템 폭발 효과 테스트"""
    system = ParticleSystem()
    system.create_explosion((10, 10), (255, 0, 0), count=10)
    
    assert len(system.particles) == 10


def test_particle_system_glow():
    """파티클 시스템 빛나는 효과 테스트"""
    system = ParticleSystem()
    system.create_glow((5, 5), (0, 255, 0), count=5)
    
    assert len(system.particles) == 5


def test_particle_system_update():
    """파티클 시스템 업데이트 테스트"""
    system = ParticleSystem()
    system.create_explosion((10, 10), (255, 0, 0), count=5)
    
    initial_count = len(system.particles)
    
    # 여러 번 업데이트
    for _ in range(50):
        system.update()
    
    # 일부 파티클이 소멸되어야 함
    assert len(system.particles) < initial_count


def test_particle_system_clear():
    """파티클 시스템 클리어 테스트"""
    system = ParticleSystem()
    system.create_explosion((10, 10), (255, 0, 0), count=10)
    system.clear()
    
    assert len(system.particles) == 0


def test_animation_pulse():
    """펄스 애니메이션 테스트"""
    scale1 = AnimationEffect.pulse(0)
    scale2 = AnimationEffect.pulse(7)
    scale3 = AnimationEffect.pulse(15)
    
    # 0과 15는 주기의 중간이므로 같을 수 있지만, 7은 다름
    assert scale1 == scale3  # 주기의 대칭점
    assert scale1 != scale2  # 중간 지점은 다름


def test_animation_blink():
    """깜빡임 애니메이션 테스트"""
    visible1 = AnimationEffect.blink(0)
    visible2 = AnimationEffect.blink(10)
    
    # 깜빡임 상태가 다름
    assert visible1 != visible2


def test_animation_rotate():
    """회전 애니메이션 테스트"""
    angle1 = AnimationEffect.rotate(0)
    angle2 = AnimationEffect.rotate(10)
    
    assert angle1 != angle2
    assert 0 <= angle1 < 360
    assert 0 <= angle2 < 360


def test_animation_fade_in():
    """페이드 인 애니메이션 테스트"""
    alpha1 = AnimationEffect.fade_in(0, 30)
    alpha2 = AnimationEffect.fade_in(15, 30)
    alpha3 = AnimationEffect.fade_in(30, 30)
    
    assert alpha1 == 0.0
    assert 0.0 < alpha2 < 1.0
    assert alpha3 == 1.0


def test_animation_fade_out():
    """페이드 아웃 애니메이션 테스트"""
    alpha1 = AnimationEffect.fade_out(0, 30)
    alpha2 = AnimationEffect.fade_out(15, 30)
    alpha3 = AnimationEffect.fade_out(30, 30)
    
    assert alpha1 == 1.0
    assert 0.0 < alpha2 < 1.0
    assert alpha3 == 0.0
