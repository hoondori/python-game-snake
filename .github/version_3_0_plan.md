# Snake Game - Version 3.0 계획서

## 목표
Version 2.1의 기능에 **핵심 게임플레이 요소**를 추가하여 게임의 깊이를 더합니다.
Version 3.1에서 추가될 고급 기능들의 기반을 마련합니다.

## Version 2.1에서 추가/개선되는 핵심 기능

### 1. 난이도 시스템 ⭐
플레이어가 자신의 실력에 맞는 난이도를 선택할 수 있습니다.

- **Easy (쉬움)**:
  - 초기 속도: 8 FPS
  - 속도 증가: 느림 (10개마다 +1 FPS)
  - 최대 속도: 15 FPS
  - 장애물: 없음
  - 추천: 초보자

- **Normal (보통)**:
  - 초기 속도: 10 FPS (기존 기본값)
  - 속도 증가: 보통 (5개마다 +1 FPS)
  - 최대 속도: 18 FPS
  - 장애물: 없음
  - 추천: 일반 플레이어

- **Hard (어려움)**:
  - 초기 속도: 12 FPS
  - 속도 증가: 빠름 (3개마다 +1 FPS)
  - 최대 속도: 22 FPS
  - 장애물: 5개 랜덤 배치
  - 추천: 숙련자

### 2. 장애물 시스템 ⭐
Hard 난이도에서 장애물이 등장하여 게임의 난이도를 높입니다.

- **특징**:
  - 회색 블록으로 표시
  - 게임 시작 시 랜덤 위치에 배치
  - 뱀/먹이와 겹치지 않는 위치에 생성
  - 충돌 시 게임 오버
  
- **Obstacle 클래스**:
  - `__init__(count, snake_body, food_pos)`: 장애물 생성
  - `generate_positions()`: 겹치지 않는 위치 생성
  - `get_positions()`: 장애물 위치 반환
  - `check_collision(position)`: 충돌 확인

### 3. Portal Mode (벽 통과 모드) ⭐
벽에 부딪혀도 게임 오버되지 않고 반대편으로 나타나는 모드입니다.

- **특징**:
  - 왼쪽 벽 → 오른쪽 끝에서 나타남
  - 오른쪽 벽 → 왼쪽 끝에서 나타남
  - 위쪽 벽 → 아래쪽 끝에서 나타남
  - 아래쪽 벽 → 위쪽 끝에서 나타남
  - 자기 몸통 충돌만 게임 오버
  
- **시각적 효과**:
  - 초록색/청록색 점선 테두리 (통과 가능 암시)
  - 반짝이는 펄스 효과 (Portal 활성화 표시)
  - 명확한 시각적 피드백으로 모드 구분
  
- **활성화 방법**:
  - 게임 중 P 키로 토글
  - 상단 패널에 "[P]" 표시
  - 시작 화면 및 Pause 화면에 설명 표시

### 4. 특수 먹이 (Golden Apple) ⭐
일반 먹이보다 높은 점수를 주는 특수 먹이가 등장합니다.

- **Golden Apple (금 사과)**:
  - 외형: 노란색 + 반짝이는 효과
  - 점수: +50점 (일반 먹이의 5배)
  - 출현 확률: 10% (일반 먹이 10개당 1개 꼴)
  - 지속 시간: 10초 후 사라지고 일반 먹이로 재생성
  
- **Food 클래스 확장**:
  - `is_golden` 속성 추가
  - `spawn_time` 속성 추가 (타이머용)
  - `get_value()`: 먹이 점수 반환
  - `should_respawn()`: 10초 경과 확인

### 5. 게임 설정 시스템
난이도와 포탈 모드를 저장하고 불러올 수 있습니다.

- **config.json 파일**:
  ```json
  {
    "difficulty": "normal",
    "portal_mode": false,
    "sound_enabled": true,
    "music_enabled": true
  }
  ```

- **ConfigManager 클래스**:
  - `load_config()`: 설정 불러오기
  - `save_config()`: 설정 저장
  - `get(key, default)`: 설정값 가져오기
  - `set(key, value)`: 설정값 변경

## 기술 스택
- **언어**: Python 3.8+
- **라이브러리**: 
  - pygame 2.0+
  - json (설정 저장)

## 파일 구조 (추가/수정)
```
snake/
├── main.py              # 게임 실행 파일
├── constants.py         # 상수 정의 (확장)
├── config.py            # 설정 관리 (새로 추가)
├── snake.py             # Snake 클래스 (Portal 모드 추가)
├── food.py              # Food 클래스 (Golden Apple 추가)
├── obstacle.py          # Obstacle 클래스 (새로 추가)
├── game.py              # Game 로직 (난이도/모드 통합)
├── ui.py                # UI 렌더링 (난이도/포탈 표시)
├── score_manager.py     # 점수 관리
├── sound_manager.py     # 사운드 관리
├── config.json          # 설정 파일 (자동 생성)
└── test/                # 테스트
    ├── test_obstacle.py      # Obstacle 테스트 (새로 추가)
    ├── test_food.py          # Food 테스트 (Golden Apple)
    ├── test_snake.py         # Snake 테스트 (Portal 모드)
    ├── test_config.py        # Config 테스트 (새로 추가)
    └── test_game.py          # Game 테스트 (통합)
```

## 구현 순서
1. **constants.py 확장**: 난이도별 상수 정의
2. **ConfigManager 구현**: 설정 저장/불러오기
3. **Obstacle 클래스 구현**: 장애물 생성 및 충돌 감지
4. **Food 클래스 확장**: Golden Apple 기능 추가
5. **Snake 클래스 수정**: Portal 모드 지원
6. **Game 클래스 수정**: 난이도/모드 통합
7. **UI 클래스 수정**: 난이도/포탈 상태 표시
8. **시작 화면 및 Pause 화면 추가**: 게임 설명 및 조작법 표시
9. **Portal 모드 시각적 효과**: 초록색 점선 테두리 + 펄스 효과
10. **테스트 코드 작성**: 모든 새 기능 테스트
11. **Manual.md 업데이트**: 새 기능 설명
12. **VERSION 파일 업데이트**: 3.0

## 테스트 계획

### 1. 단위 테스트 (Unit Test)

#### Obstacle 클래스
- [x] 지정된 개수만큼 장애물 생성
- [x] 장애물이 뱀/먹이와 겹치지 않음
- [x] 장애물 충돌 감지 정확성
- [x] 장애물 위치 반환

#### Food 클래스 (Golden Apple)
- [x] 10% 확률로 Golden Apple 생성
- [x] Golden Apple의 점수가 50점
- [x] 일반 먹이의 점수가 10점
- [x] 10초 후 Golden Apple이 일반 먹이로 변경

#### ConfigManager 클래스
- [x] 설정 파일이 없을 때 기본값 로드
- [x] 설정 저장 및 불러오기
- [x] 잘못된 설정값 처리

#### Snake 클래스 (Portal Mode)
- [x] Portal 모드에서 벽 통과 시 반대편 출현
- [x] Portal 모드에서도 자기 몸통 충돌 감지
- [x] 일반 모드에서 벽 충돌 감지

### 2. 통합 테스트 (Integration Test)
- [x] Easy 난이도에서 게임 실행 및 속도 확인
- [x] Normal 난이도에서 게임 실행 및 속도 확인
- [x] Hard 난이도에서 장애물 생성 및 충돌 확인
- [x] Portal 모드에서 벽 통과 확인
- [x] Golden Apple 먹었을 때 점수 +50 확인
- [x] 난이도 변경 후 재시작 시 설정 유지

### 3. 난이도별 테스트
- [x] Easy: 초기 8 FPS, 10개마다 +1, 최대 15
- [x] Normal: 초기 10 FPS, 5개마다 +1, 최대 18
- [x] Hard: 초기 12 FPS, 3개마다 +1, 최대 22, 장애물 5개

### 4. 게임 흐름 테스트
- [x] 게임 시작 → 플레이 → 게임 오버 → 재시작
- [x] 난이도 변경 → 재시작 시 새 난이도 적용
- [x] Portal 모드 토글 → 즉시 적용
- [x] Golden Apple 출현 → 10초 후 사라짐

### 5. 사용자 시나리오 테스트
- **초보자 (Easy)**
  - [x] 느린 속도로 게임을 배울 수 있는지
  - [x] 장애물 없어 집중할 수 있는지
  
- **일반 플레이어 (Normal)**
  - [x] 적절한 도전감이 있는지
  - [x] Golden Apple이 재미를 더하는지
  
- **숙련자 (Hard)**
  - [x] 장애물이 전략적 플레이를 요구하는지
  - [x] 높은 속도에서 컨트롤 가능한지

## 키 바인딩
기존 키 외 추가:
- **D**: 난이도 변경 (Easy → Normal → Hard → Easy)
- **P**: Portal 모드 토글 (ON/OFF)

## 성공 기준
- [x] 3가지 난이도가 모두 안정적으로 작동
- [x] Hard 난이도에서 장애물 5개 정상 배치
- [x] Portal 모드에서 벽 통과가 자연스럽게 작동
- [x] Golden Apple이 10%의 확률로 출현
- [x] 모든 단위 테스트 통과
- [x] 모든 통합 테스트 통과
- [x] 설정이 파일에 저장되고 재시작 시 유지됨
- [x] 버그 없이 10분 이상 연속 플레이 가능

## 코드 품질
- 모든 새 클래스에 docstring 작성
- 타입 힌트 사용 (Python 3.8+)
- 일관된 코딩 스타일 유지
- 중복 코드 최소화

## 예상 소요 시간
- constants.py 확장: 30분
- ConfigManager 구현: 1시간
- Obstacle 클래스 구현: 1.5시간
- Food 클래스 확장: 1시간
- Snake 클래스 수정: 1시간
- Game 클래스 수정: 2시간
- UI 클래스 수정: 1시간
- 테스트 코드 작성: 3시간
- 문서 작성 및 버그 수정: 2시간
- **총 예상 시간**: 13-15시간

## Version 3.1로의 연결
Version 3.0에서 구축한 기반 위에 다음 기능들이 추가될 예정:
- 메뉴 시스템 (게임 시작 전 설정)
- Time Attack 모드 (시간 제한)
- Survival 모드 (점진적 난이도 상승)
- 파워업 시스템 (속도 변화, 무적 등)
- 통계 및 업적 시스템
- 그래픽 효과 및 애니메이션 개선
- 리더보드 시스템

## 변경 이력

### Version 3.0 (2026-01-17)
- ✅ 난이도 시스템 (Easy/Normal/Hard) 구현
- ✅ 장애물 시스템 추가 (Hard 모드 5개)
- ✅ Portal Mode (벽 통과) 구현
- ✅ Portal Mode 시각적 효과 (초록색 점선 테두리 + 펄스)
- ✅ Golden Apple (특수 먹이) 추가 (50점, 10초 타이머)
- ✅ ConfigManager (설정 관리) 구현
- ✅ 시작 대기 화면 추가 (게임 설명 및 조작법)
- ✅ Pause 화면 개선 (상세한 게임 가이드)
- ✅ 전체 테스트 코드 작성 (41개 테스트 통과)
- ✅ Manual.md 전면 업데이트

### Version 2.1
- Sound/Music ON/OFF 상태 UI 표시
- Combo 시각 효과 강화
- Combo 자동 해제 (10초)

### Version 2.0
- 점수 시스템
- 속도 조절
- 사운드 효과
- Combo 시스템

### Version 1.0
- 기본 뱀 게임
