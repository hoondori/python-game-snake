# Snake Game - Version 3.1

고급 기능과 UI/UX가 개선된 뱀 게임입니다.

## 새로운 기능 (Version 3.1)

### 1. 메뉴 시스템 ⭐
- 직관적인 메인 메뉴
- 난이도 선택 (Easy / Normal / Hard)
- 게임 모드 선택 (Classic / Time Attack / Survival / Portal)
- 설정 메뉴 (Sound, Music, Grid, Controls)
- 최고 점수 및 업적 확인

### 2. 게임 모드
- **Classic**: 전통적인 뱀 게임
- **Time Attack**: 60초 내에 최대한 많은 점수 획득
- **Survival**: 시간이 지날수록 장애물이 추가되는 생존 모드
- **Portal**: 벽을 통과하면 반대편으로 나오는 모드

### 3. 파워업 시스템 ⭐
- **Speed Boost** (파란색): 5초간 속도 1.5배
- **Slow Motion** (보라색): 5초간 속도 0.7배
- **Invincible** (녹색): 5초간 충돌 무시

### 4. 통계 및 업적 ⭐
- SQLite 기반 통계 관리
  - 총 플레이 시간, 플레이 횟수
  - 먹은 먹이 총 개수
  - 난이도별/모드별 최고 점수
  
- 다양한 업적
  - First Bite, Growing Up, Snake Master
  - Speed Demon, Survivor, Time Master
  - Golden Hunter, Invincible
  - 점수 관련 업적 등

### 5. 그래픽 효과 ⭐
- **파티클 효과**
  - 먹이 먹을 때 폭발 효과
  - Golden Apple 반짝임
  - 파워업 빛나는 효과
  
- **애니메이션**
  - 메뉴 선택 애니메이션
  - 파워업 회전 효과
  - 타이머 깜빡임

### 6. 리더보드 ⭐
- 로컬 리더보드 시스템
- 난이도별/모드별 상위 10개 기록
- 플레이어 이름 입력 및 날짜 기록

## 프로젝트 구조

```
python-game-snake/
├── main.py                      # 메인 실행 파일
├── constants.py                 # 상수 정의
├── config.py                    # 설정 관리
│
├── core/                        # 핵심 게임 로직
│   ├── snake.py
│   ├── food.py
│   ├── obstacle.py
│   ├── powerup.py               # 파워업
│   └── game.py
│
├── modes/                       # 게임 모드
│   ├── base_mode.py             # 기본 모드 클래스
│   ├── classic_mode.py
│   ├── time_attack_mode.py
│   ├── survival_mode.py
│   └── portal_mode.py
│
├── ui/                          # UI
│   ├── menu.py                  # 메뉴 시스템
│   ├── hud.py                   # 게임 정보 표시
│   ├── effects.py               # 시각 효과
│   └── leaderboard.py           # 리더보드
│
├── managers/                    # 관리자
│   ├── score_manager.py
│   ├── sound_manager.py
│   ├── stats_manager.py         # 통계 관리
│   └── achievement_manager.py   # 업적 관리
│
├── data/                        # 데이터
│   ├── config.json
│   ├── highscores.json
│   ├── achievements.json
│   └── stats.db
│
└── test/                        # 테스트
    ├── test_powerup.py
    ├── test_effects.py
    ├── test_stats_manager.py
    └── test_achievement_manager.py
```

## 설치 및 실행

### 요구 사항
- Python 3.8+
- pygame 2.0+

### conda 환경 사용 (권장)
```bash
conda create -n pygame python=3.13
conda activate pygame
conda install -c conda-forge pygame
```

또는 pip 사용:
```bash
pip install -r requirements.txt
```

### 실행
```bash
conda run -n pygame python main.py
```

또는
```bash
python main.py
```

## 테스트

```bash
# 모든 테스트 실행
conda run -n pygame pytest test/ -v

# 특정 테스트 실행
conda run -n pygame pytest test/test_powerup.py -v
conda run -n pygame pytest test/test_effects.py -v
conda run -n pygame pytest test/test_stats_manager.py -v
conda run -n pygame pytest test/test_achievement_manager.py -v
```

## 조작 방법

### 메뉴
- **↑/↓**: 메뉴 항목 이동
- **Enter/Space**: 선택
- **ESC**: 뒤로 가기

### 게임 (기본 설정)
- **↑**: 위로 이동
- **↓**: 아래로 이동
- **←**: 왼쪽으로 이동
- **→**: 오른쪽으로 이동
- **P**: 일시정지
- **ESC**: 메뉴로 돌아가기

## 난이도

### Easy
- 느린 속도 (초기 FPS: 8)
- 장애물 없음
- 입문자에게 적합

### Normal (기본)
- 중간 속도 (초기 FPS: 10)
- 장애물 없음
- 균형잡힌 난이도

### Hard
- 빠른 속도 (초기 FPS: 12)
- 초기 장애물 5개
- 도전적인 플레이

## 점수 시스템

- **일반 먹이**: 10점
- **Golden Apple**: 50점 (10초 후 사라짐)
- **Speed Boost 파워업**: 20점
- **Slow Motion 파워업**: 20점
- **Invincible 파워업**: 30점

### 모드별 점수 배율
- Classic: 1.0배
- Portal: 1.3배
- Survival: 1.2배
- Time Attack: 1.5배

## 업적 목록

- **First Bite**: 첫 먹이 먹기
- **Growing Up**: 뱀 길이 10 달성
- **Snake Master**: 뱀 길이 30 달성
- **Speed Demon**: 최고 속도 도달
- **Survivor**: Survival 모드 5분 생존
- **Time Master**: Time Attack 모드 100점 달성
- **Golden Hunter**: Golden Apple 10개 먹기
- **Invincible**: 무적 파워업으로 장애물 통과
- **Power Collector**: 파워업 20개 수집
- **Century**: 점수 100 달성
- **High Achiever**: 점수 500 달성

## 개발 정보

- **언어**: Python 3.8+
- **라이브러리**: pygame 2.0+, json, sqlite3
- **테스트**: pytest
- **버전**: 3.1

## 변경 이력

### Version 3.1 (2026-01-17)
- 메뉴 시스템 추가
- 파워업 시스템
- Time Attack / Survival 모드
- 통계 및 업적 시스템
- 파티클 효과 및 애니메이션
- 리더보드 시스템

### Version 3.0
- 난이도 시스템
- 장애물
- Portal Mode
- Golden Apple

### Version 2.1
- Sound/Music 상태 표시
- Combo 효과

### Version 2.0
- 점수 시스템
- 사운드

### Version 1.0
- 기본 뱀 게임

## 라이선스

MIT License

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.
