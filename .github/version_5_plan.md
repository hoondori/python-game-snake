# Snake Game - Version 5 계획서

## 목표
Version 4의 AI 대전 시스템에 스테이지 시스템과 리플레이 녹화 기능을 추가하여 게임의 재플레이 가치와 학습 기능을 향상시킵니다.

## Version 4에서 추가/개선되는 기능

### 1. 스테이지 시스템

#### 1.1 스테이지 구조
- **총 스테이지 수**: 10개 (확장 가능)
- **진행 방식**: 순차적 진행 (이전 스테이지 클리어 필요)
- **난이도 증가**: 스테이지가 올라갈수록 난이도 상승
- **저장 시스템**: 최고 도달 스테이지 저장 및 이어하기 가능

#### 1.2 스테이지별 특징

**Stage 1: Tutorial**
- 난이도: 매우 쉬움
- 맵 크기: 표준 (30x30)
- 장애물: 없음
- 속도: 느림 (10 FPS)
- 클리어 조건: 점수 50점 달성
- 특징: 기본 조작 익히기

**Stage 2: First Challenge**
- 난이도: 쉬움
- 맵 크기: 표준 (30x30)
- 장애물: 화면 중앙에 작은 벽 (4x4)
- 속도: 느림 (10 FPS)
- 클리어 조건: 점수 100점 달성
- 특징: 장애물 회피 연습

**Stage 3: Speed Up**
- 난이도: 보통
- 맵 크기: 표준 (30x30)
- 장애물: 화면 중앙에 '+' 모양 벽
- 속도: 보통 (12 FPS)
- 클리어 조건: 점수 150점 달성
- 특징: 빠른 반응 속도 요구

**Stage 4: Narrow Passage**
- 난이도: 보통
- 맵 크기: 표준 (30x30)
- 장애물: 좁은 통로 형태의 벽들
- 속도: 보통 (12 FPS)
- 클리어 조건: 점수 200점 달성
- 특징: 정밀한 조작 요구

**Stage 5: Maze Master**
- 난이도: 어려움
- 맵 크기: 표준 (30x30)
- 장애물: 미로 형태의 복잡한 벽
- 속도: 빠름 (15 FPS)
- 클리어 조건: 점수 250점 달성
- 특징: 경로 계획 능력 요구

**Stage 6: Time Attack**
- 난이도: 어려움
- 맵 크기: 표준 (30x30)
- 장애물: 회전하는 벽 (동적 장애물)
- 속도: 빠름 (15 FPS)
- 제한시간: 180초
- 클리어 조건: 제한시간 내 점수 300점 달성
- 특징: 시간 압박 + 동적 장애물

**Stage 7: AI Battle - Beginner**
- 난이도: 보통
- 맵 크기: 표준 (30x30)
- 장애물: 간단한 벽
- 속도: 보통 (12 FPS)
- 대전 상대: Beginner AI
- 클리어 조건: AI보다 높은 점수로 승리
- 특징: AI와의 첫 대전

**Stage 8: AI Battle - Intermediate**
- 난이도: 어려움
- 맵 크기: 표준 (30x30)
- 장애물: 복잡한 벽
- 속도: 빠름 (15 FPS)
- 대전 상대: Intermediate AI
- 클리어 조건: AI보다 높은 점수로 승리
- 특징: 더 강한 AI와 대결

**Stage 9: AI Battle - Advanced**
- 난이도: 매우 어려움
- 맵 크기: 표준 (30x30)
- 장애물: 동적 + 정적 장애물 혼합
- 속도: 매우 빠름 (18 FPS)
- 대전 상대: Advanced AI
- 클리어 조건: AI보다 높은 점수로 승리
- 특징: 고급 AI 전략 대응

**Stage 10: Final Boss - Expert AI**
- 난이도: 최고 난이도
- 맵 크기: 대형 (40x40)
- 장애물: 복잡한 미로 + 움직이는 벽
- 속도: 매우 빠름 (20 FPS)
- 대전 상대: Expert AI
- 클리어 조건: AI보다 높은 점수로 승리
- 특징: 최종 보스 AI 격파

#### 1.3 스테이지 데이터 구조
```python
class StageConfig:
    def __init__(self, stage_number, name, difficulty, 
                 map_size, obstacles, speed, 
                 clear_condition, time_limit=None,
                 ai_opponent=None):
        self.stage_number = stage_number
        self.name = name
        self.difficulty = difficulty  # 1-5 (별 표시)
        self.map_size = map_size  # (width, height)
        self.obstacles = obstacles  # [(x, y, width, height), ...]
        self.speed = speed  # FPS
        self.clear_condition = clear_condition  # {'type': 'score', 'value': 100}
        self.time_limit = time_limit  # seconds (None = unlimited)
        self.ai_opponent = ai_opponent  # AI class or None
        self.is_locked = True  # 잠김 여부
        self.best_score = 0  # 최고 점수
        self.completion_count = 0  # 클리어 횟수
```

#### 1.4 스테이지 선택 화면
- **레이아웃**:
  - 스테이지를 카드 형식으로 표시 (3x4 그리드)
  - 각 카드에 스테이지 정보 표시
  - 잠긴 스테이지는 자물쇠 아이콘 표시
  
- **표시 정보**:
  - 스테이지 번호 및 이름
  - 난이도 (별 1-5개)
  - 최고 점수
  - 클리어 여부 (별 획득 표시)
  - 클리어 조건
  
- **조작**:
  - 마우스 클릭으로 스테이지 선택
  - ESC: 메인 메뉴로 돌아가기
  - 방향키로 스테이지 탐색
  - ENTER로 선택된 스테이지 시작

#### 1.5 스테이지 진행 시스템
- **진행 상태 저장**:
  - 각 스테이지의 클리어 여부
  - 각 스테이지의 최고 점수
  - 현재 잠금 해제된 스테이지
  - JSON 파일로 저장 (`stage_progress.json`)

- **스테이지 잠금 해제**:
  - 이전 스테이지를 클리어하면 다음 스테이지 잠금 해제
  - Stage 1은 항상 잠금 해제 상태

- **스테이지 클리어**:
  - 클리어 조건 달성 시 "Stage Clear!" 메시지 표시
  - 획득 점수 표시
  - 별 등급 부여 (1-3개):
    - ★☆☆: 클리어 조건만 달성
    - ★★☆: 클리어 조건의 150% 달성
    - ★★★: 클리어 조건의 200% 달성
  - 다음 스테이지 버튼 표시
  - 재시도 버튼 표시
  - 메인 메뉴 버튼 표시

- **스테이지 실패**:
  - "Stage Failed" 메시지 표시
  - 도달 점수 표시
  - 재시도 버튼 표시
  - 스테이지 선택 버튼 표시
  - 메인 메뉴 버튼 표시

#### 1.6 스테이지 데이터 저장 형식
```json
{
  "version": "5.0",
  "last_played_stage": 3,
  "stages": [
    {
      "stage_number": 1,
      "is_unlocked": true,
      "is_cleared": true,
      "best_score": 150,
      "star_rating": 3,
      "completion_count": 5,
      "best_time": 45.3
    },
    {
      "stage_number": 2,
      "is_unlocked": true,
      "is_cleared": true,
      "best_score": 200,
      "star_rating": 2,
      "completion_count": 3,
      "best_time": 67.8
    }
  ]
}
```

### 2. 리플레이 녹화 및 재생 시스템

#### 2.1 녹화 시스템

**녹화 데이터 구조**:
```python
class GameRecording:
    def __init__(self):
        self.metadata = {
            'version': '5.0',
            'timestamp': None,  # 녹화 시작 시간
            'duration': 0,  # 총 플레이 시간 (초)
            'stage': None,  # 스테이지 정보
            'player_name': 'Player',
            'final_score': 0,
            'game_result': None,  # 'win', 'lose', 'game_over'
        }
        self.initial_state = {
            'snake_position': [],
            'snake_direction': None,
            'food_position': None,
            'obstacles': [],
            'ai_snake_position': [],  # AI 대전인 경우
            'ai_snake_direction': None,
        }
        self.frames = []  # 각 프레임의 이벤트 기록
        
class FrameData:
    def __init__(self, frame_number, timestamp):
        self.frame_number = frame_number
        self.timestamp = timestamp  # 게임 시작 후 경과 시간
        self.events = []  # 이 프레임에서 발생한 이벤트들
        
class GameEvent:
    def __init__(self, event_type, data):
        self.event_type = event_type  # 'move', 'eat', 'collision', 'direction_change'
        self.data = data  # 이벤트별 데이터
```

**녹화 이벤트 타입**:
- `GAME_START`: 게임 시작
- `DIRECTION_CHANGE`: 방향 전환 (플레이어/AI)
- `SNAKE_MOVE`: 뱀 이동 (위치 업데이트)
- `FOOD_EATEN`: 먹이 섭취
- `FOOD_SPAWN`: 새 먹이 생성
- `ITEM_SPAWN`: 아이템 생성 (있는 경우)
- `ITEM_COLLECTED`: 아이템 획득
- `COLLISION`: 충돌 발생
- `SCORE_UPDATE`: 점수 업데이트
- `GAME_OVER`: 게임 오버
- `STAGE_CLEAR`: 스테이지 클리어

**녹화 파일 형식**:
- 파일 형식: JSON (압축: gzip)
- 파일명 규칙: `replay_YYYYMMDD_HHMMSS_stage{N}.json.gz`
- 저장 경로: `./replays/`

**자동 녹화 설정**:
- 모든 게임 플레이 자동 녹화
- 설정에서 녹화 ON/OFF 가능
- 녹화 파일 최대 개수 설정 (기본: 100개)
- 오래된 녹화 파일 자동 삭제

#### 2.2 리플레이 재생 시스템

**재생 기능**:
- **재생 컨트롤**:
  - SPACE: 재생/일시정지
  - 좌우 화살표: 5초 전/후 이동
  - 1, 2, 3 키: 재생 속도 조절 (0.5x, 1x, 2x)
  - R: 처음부터 다시 재생
  - ESC: 재생 종료
  
- **재생 UI**:
  - 하단에 타임라인 바 표시
  - 현재 재생 위치 표시
  - 재생 속도 표시
  - 현재 점수 및 시간 표시
  - 일시정지 아이콘 표시

- **재생 모드**:
  - 일반 재생: 실제 속도로 재생
  - 빠른 재생: 2배속 재생
  - 느린 재생: 0.5배속 재생
  - 프레임별 재생: 한 프레임씩 이동 (디버깅용)

#### 2.3 리플레이 관리 화면

**리플레이 목록**:
- 저장된 리플레이 파일 목록 표시
- 각 리플레이 정보:
  - 날짜 및 시간
  - 스테이지 번호 및 이름
  - 최종 점수
  - 플레이 시간
  - 결과 (클리어/실패)
  - 썸네일 이미지 (선택사항)

**리플레이 조작**:
- 클릭하여 리플레이 재생
- 우클릭 메뉴:
  - 재생
  - 이름 변경
  - 즐겨찾기 추가/제거
  - 삭제
  - 내보내기 (파일로 저장)
  
**필터 및 정렬**:
- 스테이지별 필터
- 날짜별 정렬
- 점수별 정렬
- 즐겨찾기 필터

#### 2.4 리플레이 데이터 예시
```json
{
  "metadata": {
    "version": "5.0",
    "timestamp": "2026-01-13T14:30:00",
    "duration": 123.5,
    "stage": {
      "stage_number": 5,
      "name": "Maze Master"
    },
    "player_name": "Player",
    "final_score": 280,
    "game_result": "stage_clear"
  },
  "initial_state": {
    "snake_position": [[15, 15], [14, 15], [13, 15]],
    "snake_direction": "RIGHT",
    "food_position": [20, 10],
    "obstacles": [
      {"x": 10, "y": 10, "width": 2, "height": 5},
      {"x": 20, "y": 15, "width": 3, "height": 3}
    ]
  },
  "frames": [
    {
      "frame_number": 0,
      "timestamp": 0.0,
      "events": [
        {"type": "GAME_START", "data": {}}
      ]
    },
    {
      "frame_number": 10,
      "timestamp": 1.0,
      "events": [
        {
          "type": "DIRECTION_CHANGE",
          "data": {
            "entity": "player",
            "old_direction": "RIGHT",
            "new_direction": "UP"
          }
        }
      ]
    },
    {
      "frame_number": 15,
      "timestamp": 1.5,
      "events": [
        {
          "type": "FOOD_EATEN",
          "data": {
            "position": [20, 10],
            "score_gained": 10
          }
        },
        {
          "type": "FOOD_SPAWN",
          "data": {
            "position": [8, 22]
          }
        },
        {
          "type": "SCORE_UPDATE",
          "data": {
            "old_score": 0,
            "new_score": 10
          }
        }
      ]
    }
  ]
}
```

#### 2.5 리플레이 공유 기능 (선택사항)

**내보내기**:
- 리플레이 파일을 외부로 내보내기
- 파일명 지정 가능
- 메타데이터 포함

**불러오기**:
- 외부 리플레이 파일 불러오기
- 파일 유효성 검증
- 호환되지 않는 버전 감지

**온라인 공유** (고급 기능, 선택사항):
- 리플레이를 온라인 플랫폼에 업로드
- 다른 플레이어의 리플레이 다운로드 및 시청
- 리더보드와 연동

### 3. 메뉴 시스템 확장

#### 3.1 메인 메뉴 업데이트
기존 메뉴에 추가:
- **Stage Mode**: 스테이지 선택 화면으로 이동
- **Replays**: 리플레이 목록 화면으로 이동
- **Free Play**: 자유 모드 (기존 플레이)
- **VS AI**: AI 대전 모드
- **Settings**: 설정
- **Quit**: 종료

#### 3.2 설정 화면 추가 옵션
- **Recording Settings**:
  - Auto Record: ON/OFF
  - Max Replay Files: 50/100/200/무제한
  - Replay Quality: 저/중/고 (프레임 기록 간격)
  
- **Stage Settings**:
  - Reset Progress: 진행 상황 초기화 버튼
  - Unlock All Stages: 모든 스테이지 잠금 해제 (치트)

### 4. 파일 구조

```
snake/
├── main.py                      # 게임 실행 파일
├── snake.py                     # Snake 클래스
├── food.py                      # Food 클래스
├── game.py                      # Game 로직 관리
├── constants.py                 # 상수 정의
├── ai/                          # AI 관련 (Version 4)
│   ├── __init__.py
│   ├── base_ai.py
│   ├── beginner_ai.py
│   ├── intermediate_ai.py
│   ├── advanced_ai.py
│   └── expert_ai.py
├── stages/                      # 스테이지 관련 (NEW)
│   ├── __init__.py
│   ├── stage_manager.py        # 스테이지 관리
│   ├── stage_config.py         # 스테이지 설정
│   ├── stage_data.py           # 스테이지 데이터 정의
│   └── stage_ui.py             # 스테이지 선택 UI
├── replay/                      # 리플레이 관련 (NEW)
│   ├── __init__.py
│   ├── recorder.py             # 게임 녹화
│   ├── player.py               # 리플레이 재생
│   ├── replay_manager.py       # 리플레이 파일 관리
│   └── replay_ui.py            # 리플레이 UI
├── ui/                          # UI 관련
│   ├── __init__.py
│   ├── menu.py
│   ├── hud.py
│   └── settings.py
├── utils/                       # 유틸리티
│   ├── __init__.py
│   ├── file_handler.py         # 파일 입출력
│   └── compression.py          # 압축/해제
├── data/                        # 데이터 저장
│   ├── stage_progress.json     # 스테이지 진행 상황
│   └── settings.json           # 게임 설정
├── replays/                     # 리플레이 파일 저장 (NEW)
│   └── .gitkeep
├── requirements.txt
└── README.md
```

### 5. 구현 우선순위

#### Phase 1: 스테이지 시스템 기본 구현 (1-2주)
1. 스테이지 데이터 구조 설계
2. 10개 스테이지 디자인 및 데이터 정의
3. 스테이지 선택 화면 UI 구현
4. 스테이지 진행 저장/로드 시스템
5. 스테이지 클리어/실패 화면

#### Phase 2: 리플레이 녹화 시스템 (1주)
1. 게임 이벤트 기록 시스템
2. 리플레이 데이터 구조 설계
3. 자동 녹화 기능 구현
4. 리플레이 파일 저장 (압축)
5. 리플레이 파일 관리 (삭제, 정리)

#### Phase 3: 리플레이 재생 시스템 (1주)
1. 리플레이 파일 로드
2. 프레임별 재생 엔진
3. 재생 컨트롤 (재생/일시정지/속도 조절)
4. 재생 UI (타임라인, 정보 표시)

#### Phase 4: 리플레이 관리 화면 (1주)
1. 리플레이 목록 UI
2. 필터 및 정렬 기능
3. 리플레이 관리 기능 (삭제, 이름 변경)
4. 리플레이 내보내기/불러오기

#### Phase 5: 통합 및 테스트 (1주)
1. 메뉴 시스템 업데이트
2. 설정 화면 확장
3. 전체 시스템 통합 테스트
4. 버그 수정 및 최적화
5. 사용자 테스트 및 피드백 반영

### 6. 새로운 의존성

```txt
# 기존 requirements.txt에 추가
gzip  # 표준 라이브러리, 명시적 설치 불필요
```

### 7. 테스트 계획

#### 7.1 스테이지 시스템 테스트
```python
# test/test_stage.py
- test_stage_unlock(): 스테이지 잠금 해제 로직
- test_stage_clear(): 스테이지 클리어 조건 달성
- test_stage_save_load(): 진행 상황 저장/로드
- test_stage_star_rating(): 별 등급 계산
- test_stage_progression(): 스테이지 순차 진행
```

#### 7.2 리플레이 시스템 테스트
```python
# test/test_replay.py
- test_record_game(): 게임 녹화 기능
- test_save_replay(): 리플레이 파일 저장
- test_load_replay(): 리플레이 파일 로드
- test_replay_playback(): 리플레이 재생 정확도
- test_replay_compression(): 파일 압축/해제
- test_replay_events(): 이벤트 기록 정확도
```

### 8. 성능 고려사항

#### 8.1 리플레이 파일 크기 최적화
- 이벤트 기반 녹화로 불필요한 데이터 최소화
- 변경사항만 기록 (델타 인코딩)
- gzip 압축 적용
- 예상 파일 크기: 1분당 10-50KB (압축 후)

#### 8.2 리플레이 재생 성능
- 프레임 캐싱으로 부드러운 재생
- 필요시 프레임 스킵으로 빠른 재생
- 메모리 효율적인 데이터 구조 사용

#### 8.3 스테이지 데이터 로딩
- 필요한 스테이지만 메모리에 로드
- 스테이지 전환 시 비동기 로딩
- 리소스 사전 로드로 끊김 없는 플레이

### 9. 사용자 경험 개선

#### 9.1 스테이지 모드
- 명확한 진행 상황 표시
- 도전적이지만 공평한 난이도 곡선
- 스테이지 클리어 시 성취감 제공
- 다양한 플레이 스타일 지원

#### 9.2 리플레이 기능
- 자신의 플레이 복기 가능
- 실수 분석 및 학습 도구
- 베스트 플레이 저장 및 공유
- 직관적인 재생 컨트롤

### 10. 향후 확장 가능성

#### 10.1 추가 스테이지
- 커뮤니티 스테이지 제작 도구
- 스테이지 에디터
- 사용자 제작 스테이지 공유

#### 10.2 고급 리플레이 기능
- 리플레이 편집 기능
- 하이라이트 클립 제작
- 비디오 내보내기 (MP4)
- 온라인 리더보드와 연동

#### 10.3 통계 시스템
- 스테이지별 통계
- 전체 플레이 통계
- 개인 최고 기록
- 달성 과제 시스템

## 요약

Version 5는 다음 두 가지 핵심 기능을 추가합니다:

1. **스테이지 시스템**: 10개의 다양한 스테이지를 통한 순차적 게임 진행, 명확한 목표와 달성감 제공
2. **리플레이 시스템**: 모든 게임 플레이를 녹화하고 나중에 다시 볼 수 있는 기능, 플레이 복기 및 학습 도구

이 두 기능은 게임의 재플레이 가치를 크게 향상시키고, 플레이어가 자신의 실력을 향상시킬 수 있는 도구를 제공합니다. 또한 스테이지 시스템은 명확한 진행 구조를 제공하여 게임의 목표의식을 강화하고, 리플레이 시스템은 플레이어의 성취를 기록하고 공유할 수 있게 합니다.
