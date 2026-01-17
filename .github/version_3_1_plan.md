# Snake Game - Version 3.1 계획서

## 목표
Version 3.0의 기반 위에 **고급 게임 기능과 UI/UX 개선**을 추가하여 완성도 높은 게임을 만듭니다.

## Version 3.0에서 추가/개선되는 고급 기능

### 1. 메뉴 시스템 ⭐
게임 시작 전에 설정을 변경할 수 있는 직관적인 메뉴를 제공합니다.

- **메인 메뉴**:
  - 게임 시작 (Start Game)
  - 난이도 선택 (Difficulty)
  - 게임 모드 선택 (Game Mode)
  - 설정 (Settings)
  - 최고 점수 (High Scores)
  - 종료 (Quit)

- **난이도 선택 메뉴**:
  - Easy / Normal / Hard 선택
  - 각 난이도 설명 표시
  - 선택 시 하이라이트

- **게임 모드 선택 메뉴**:
  - Classic (클래식)
  - Time Attack (시간 제한)
  - Survival (생존)
  - Portal (포탈)

- **설정 메뉴**:
  - Sound ON/OFF
  - Music ON/OFF
  - Grid ON/OFF
  - 키 설정 (Arrow Keys / WASD)

- **Menu 클래스**:
  - `__init__(screen)`: 메뉴 초기화
  - `draw()`: 메뉴 화면 렌더링
  - `handle_input(event)`: 입력 처리
  - `get_selected()`: 선택된 옵션 반환

### 2. 추가 게임 모드 ⭐

#### Time Attack Mode (시간 제한)
- 60초 제한 시간
- 제한 시간 내 최대한 많은 점수 획득
- 특수 먹이(시계 아이콘)로 시간 연장 (+5초)
- 타이머 UI 표시 (상단 패널)
- 시간 종료 시 게임 오버

#### Survival Mode (생존)
- 시간이 지날수록 장애물이 추가됨
- 10초마다 새로운 장애물 1개 추가
- 최대 20개까지 추가
- 생존 시간이 점수
- 최대한 오래 생존하는 것이 목표

### 3. 파워업 시스템 ⭐
게임을 더욱 재미있게 만드는 특수 아이템들입니다.

- **Speed Boost (속도 향상)**:
  - 외형: 파란색 번개 아이콘
  - 효과: 5초간 속도 1.5배
  - 점수: +20
  - 출현 확률: 5%

- **Slow Motion (슬로우)**:
  - 외형: 보라색 시계 아이콘
  - 효과: 5초간 속도 0.7배
  - 점수: +20
  - 출현 확률: 5%

- **Invincible (무적)**:
  - 외형: 녹색 별 아이콘
  - 효과: 5초간 충돌 무시 (벽/장애물/자기 몸)
  - 점수: +30
  - 출현 확률: 3%

- **PowerUp 클래스**:
  - `type`: 파워업 종류
  - `position`: 위치
  - `duration`: 지속 시간
  - `is_active()`: 활성 상태 확인
  - `apply(game)`: 효과 적용
  - `expire()`: 효과 종료

### 4. 통계 및 업적 시스템 ⭐

#### 통계 (StatsManager)
SQLite 데이터베이스로 관리:
- 총 플레이 시간
- 총 플레이 횟수
- 먹은 먹이 총 개수
- 난이도별 최고 점수
- 모드별 최고 점수
- 최장 생존 시간

#### 업적 (AchievementManager)
JSON 파일로 관리:
- **"First Bite"**: 첫 먹이 먹기
- **"Growing Up"**: 길이 10 달성
- **"Snake Master"**: 길이 30 달성
- **"Speed Demon"**: 최고 속도 도달
- **"Survivor"**: Survival 모드 5분 생존
- **"Time Master"**: Time Attack 100점 달성
- **"Golden Hunter"**: Golden Apple 10개 먹기
- **"Invincible"**: 무적 파워업으로 장애물 통과

업적 잠금 해제 시:
- 화면에 알림 표시 (2초간)
- 사운드 효과
- 업적 목록에 기록

### 5. 그래픽 효과 및 애니메이션 ⭐

#### 파티클 효과
- **먹이 먹을 때**: 색상 파티클 폭발
- **Golden Apple**: 반짝이는 별 파티클
- **파워업 활성화**: 빛나는 원형 효과
- **게임 오버**: 뱀 사라지는 페이드 아웃

#### 애니메이션
- **뱀 이동**: 부드러운 보간 애니메이션
- **파워업**: 회전 애니메이션
- **타이머**: 10초 이하일 때 깜빡임
- **메뉴**: 선택 시 스케일 애니메이션

#### Effects 클래스
- `Particle`: 단일 파티클
- `ParticleSystem`: 파티클 관리
- `create_explosion(pos, color)`: 폭발 효과
- `create_glow(pos, color)`: 빛나는 효과
- `update()`: 파티클 업데이트
- `draw(surface)`: 파티클 렌더링

### 6. 리더보드 시스템 ⭐

#### 로컬 리더보드
- 난이도별 상위 10개 기록
- 모드별 상위 10개 기록
- 플레이어 이름 입력 (최대 10자)
- 날짜 및 시간 기록

#### 리더보드 UI
- 테이블 형식으로 표시
- 순위 / 이름 / 점수 / 날짜
- 현재 플레이어 기록 하이라이트
- ESC로 돌아가기

#### Leaderboard 클래스
- `add_score(name, score, difficulty, mode)`: 점수 추가
- `get_top_scores(difficulty, mode, limit)`: 상위 점수 가져오기
- `is_high_score(score, difficulty, mode)`: 최고 점수 확인
- `save()` / `load()`: 데이터 저장/로드

### 7. 사운드 개선
Version 2.1의 사운드 시스템에 추가:
- 파워업 획득 사운드
- 업적 잠금 해제 사운드
- 메뉴 선택 사운드
- 시간 경고 사운드 (Time Attack 모드)
- 게임 모드별 배경 음악

## 기술 스택
- **언어**: Python 3.8+
- **라이브러리**: 
  - pygame 2.0+
  - json (설정, 업적)
  - sqlite3 (통계)

## 파일 구조 (추가/수정)
```
snake/
├── main.py                      # 메뉴에서 시작
├── constants.py                 # 상수 (파워업 상수 추가)
├── config.py                    # 설정 관리
│
├── core/                        # 핵심 게임 로직
│   ├── snake.py
│   ├── food.py
│   ├── obstacle.py
│   ├── powerup.py               # 파워업 (새로 추가)
│   └── game.py                  # 게임 로직
│
├── modes/                       # 게임 모드 (새로 추가)
│   ├── base_mode.py             # 기본 모드 클래스
│   ├── classic_mode.py          # 클래식 모드
│   ├── time_attack_mode.py      # 시간 제한 모드
│   ├── survival_mode.py         # 생존 모드
│   └── portal_mode.py           # 포탈 모드
│
├── ui/                          # UI (새로 추가)
│   ├── menu.py                  # 메뉴 시스템
│   ├── hud.py                   # 게임 정보 표시 (ui.py 리팩토링)
│   ├── effects.py               # 시각 효과
│   └── leaderboard.py           # 리더보드 UI
│
├── managers/                    # 관리자 (새로 추가)
│   ├── score_manager.py
│   ├── sound_manager.py
│   ├── stats_manager.py         # 통계 관리
│   └── achievement_manager.py   # 업적 관리
│
├── data/                        # 데이터 (새로 추가)
│   ├── config.json
│   ├── highscores.json
│   ├── achievements.json
│   └── stats.db
│
└── test/                        # 테스트
    ├── test_powerup.py          # 파워업 테스트
    ├── test_modes.py            # 게임 모드 테스트
    ├── test_menu.py             # 메뉴 테스트
    ├── test_stats.py            # 통계 테스트
    ├── test_achievements.py     # 업적 테스트
    └── test_effects.py          # 효과 테스트
```

## 구현 순서
1. **프로젝트 리팩토링**: 파일 구조 정리 (core/, ui/, managers/, modes/)
2. **Menu 시스템**: 메인 메뉴 및 서브 메뉴 구현
3. **게임 모드**: Time Attack, Survival 모드 구현
4. **PowerUp 시스템**: 파워업 클래스 및 효과 구현
5. **StatsManager**: SQLite 기반 통계 관리
6. **AchievementManager**: JSON 기반 업적 관리
7. **Effects 시스템**: 파티클 효과 구현
8. **Leaderboard**: 리더보드 UI 및 데이터 관리
9. **사운드 추가**: 새로운 효과음 추가
10. **테스트 코드**: 모든 새 기능 테스트
11. **문서 작성**: Manual 및 VERSION 업데이트

## 테스트 계획

### 1. 단위 테스트

#### Menu 시스템
- [ ] 메뉴 항목 선택
- [ ] 키보드 내비게이션
- [ ] 메뉴 간 전환
- [ ] 설정 저장 및 적용

#### PowerUp 클래스
- [ ] 각 파워업 효과 정확성
- [ ] 지속 시간 관리
- [ ] 확률적 생성 (5%, 3%)
- [ ] 중복 효과 처리

#### StatsManager
- [ ] 데이터베이스 CRUD
- [ ] 통계 누적 정확성
- [ ] 쿼리 성능

#### AchievementManager
- [ ] 업적 조건 확인
- [ ] 중복 잠금 해제 방지
- [ ] JSON 저장/로드

#### Effects 시스템
- [ ] 파티클 생성 및 소멸
- [ ] 애니메이션 부드러움
- [ ] 성능 (많은 파티클)

### 2. 통합 테스트

#### Time Attack Mode
- [ ] 타이머 정확성 (60초)
- [ ] 시간 보너스 아이템 (+5초)
- [ ] 시간 종료 시 게임 오버
- [ ] 점수 저장

#### Survival Mode
- [ ] 10초마다 장애물 추가
- [ ] 최대 20개 제한
- [ ] 생존 시간 기록
- [ ] 점수 계산

#### 파워업 시스템
- [ ] Speed Boost 효과 적용
- [ ] Slow Motion 효과 적용
- [ ] Invincible 효과 (충돌 무시)
- [ ] 효과 종료 후 정상 복귀

#### 업적 시스템
- [ ] 조건 달성 시 잠금 해제
- [ ] 알림 표시
- [ ] 데이터 저장
- [ ] 게임 재시작 시 유지

### 3. UI/UX 테스트
- [ ] 메뉴 내비게이션이 직관적
- [ ] 모든 버튼 작동
- [ ] 리더보드 정확성
- [ ] 업적 알림이 잘 보임
- [ ] 파티클 효과가 부드러움
- [ ] 폰트 가독성

### 4. 성능 테스트
- [ ] 파티클 효과로 프레임 드롭 없음
- [ ] 많은 장애물에도 부드러운 동작
- [ ] 데이터베이스 작업이 게임 방해 안 함
- [ ] 메모리 누수 없음

### 5. 데이터 무결성 테스트
- [ ] 설정 파일 손상 시 기본값
- [ ] 데이터베이스 손상 시 재생성
- [ ] 업적 데이터 손실 방지
- [ ] 리더보드 정합성

## 키 바인딩
기존 키에 추가 없음 (메뉴에서 모든 설정)

## 성공 기준
- [ ] 메뉴 시스템이 직관적이고 사용하기 쉬움
- [ ] 4가지 게임 모드가 모두 안정적으로 작동
- [ ] 파워업이 게임플레이를 풍부하게 만듦
- [ ] 통계 및 업적이 정확하게 추적됨
- [ ] 파티클 효과가 게임 경험을 향상
- [ ] 리더보드가 경쟁심을 유발
- [ ] 모든 테스트 통과
- [ ] 버그 없이 30분 이상 연속 플레이 가능

## 코드 품질
- 모듈화된 구조 (core, ui, managers, modes)
- 모든 클래스에 docstring
- 타입 힌트 사용
- 일관된 코딩 스타일
- DRY 원칙 준수

## 예상 소요 시간
- 프로젝트 리팩토링: 2시간
- Menu 시스템: 4시간
- 게임 모드 구현: 6시간
- PowerUp 시스템: 3시간
- Stats/Achievement: 4시간
- Effects 시스템: 5시간
- Leaderboard: 3시간
- 사운드 추가: 2시간
- 테스트 코드: 6시간
- 문서 및 버그 수정: 3시간
- **총 예상 시간**: 38-42시간

## 향후 개선 방향 (v4+)
- 온라인 멀티플레이어
- AI 대전 모드
- 커스텀 스킨
- 맵 에디터
- 모바일 버전
- 클라우드 세이브

## 변경 이력

### Version 3.1 (예정)
- 메뉴 시스템
- Time Attack / Survival 모드
- 파워업 시스템
- 통계 및 업적
- 그래픽 효과
- 리더보드

### Version 3.0
- 난이도 시스템
- 장애물
- Portal Mode
- Golden Apple

### Version 2.1
- Sound/Music 상태 표시
- Combo 효과 강화

### Version 2.0
- 점수 시스템
- 사운드

### Version 1.0
- 기본 뱀 게임
