# Snake Game - Version 1

Python과 Pygame으로 구현한 클래식 스네이크 게임입니다.

## 기능

- ✅ 2D 그리드 기반 게임
- ✅ 방향키로 뱀 조종
- ✅ 먹이를 먹으면 뱀이 성장
- ✅ 벽 충돌 시 게임 오버
- ✅ 자기 몸통 충돌 시 게임 오버

## 요구사항

- Python 3.8+
- Pygame 2.0+

## 설치 방법

1. Conda 환경 활성화:
```bash
conda activate pygame
```

2. Pygame 설치 (아직 설치하지 않았다면):
```bash
pip install pygame
```

## 실행 방법

```bash
python main.py
```

또는 conda 환경을 사용하는 경우:
```bash
conda run -n pygame python main.py
```

## 조작 방법

- **↑** : 위로 이동
- **↓** : 아래로 이동
- **←** : 왼쪽으로 이동
- **→** : 오른쪽으로 이동

## 테스트

자동화된 테스트를 실행하려면:

```bash
# 모든 테스트 실행
python test/run_tests.py

# 또는 conda 환경 사용
conda run -n pygame python test/run_tests.py

# pytest를 직접 사용
pytest test/

# 개별 테스트 파일 실행
pytest test/test_snake.py
pytest test/test_food.py
pytest test/test_game.py

# 더 자세한 출력
pytest test/ -v

# 특정 테스트만 실행
pytest test/test_snake.py::test_initial_position_and_length
```

**테스트 커버리지:**
- ✅ Snake 클래스 단위 테스트 (13개)
- ✅ Food 클래스 단위 테스트 (7개)
- ✅ Game 통합 테스트 (9개)
- **총 29개 테스트**
- **프레임워크: pytest**

## 게임 규칙

1. 뱀은 계속 움직입니다
2. 빨간색 먹이를 먹으면 뱀이 1칸 길어집니다
3. 벽에 부딪히면 게임이 끝납니다
4. 자신의 몸통에 부딪혀도 게임이 끝납니다
5. 게임 오버 후 2초 뒤에 자동으로 종료됩니다

## 파일 구조

```
snake/
├── main.py          # 게임 실행 파일
├── game.py          # 게임 로직 관리
├── snake.py         # Snake 클래스
├── food.py          # Food 클래스
├── constants.py     # 상수 정의
└── README.md        # 이 파일
```

## 게임 설정

`constants.py` 파일에서 다음 설정을 변경할 수 있습니다:

- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: 화면 크기
- `GRID_SIZE`: 블록 크기
- `FPS`: 게임 속도 (기본값: 10)
- `GREEN`, `RED`: 뱀과 먹이 색상

## 다음 버전 계획

- Version 2: 점수 시스템, UI 개선, 속도 조절
- Version 3: 메뉴 시스템, 게임 모드, 고급 기능
- Version 4: AI 대전 모드

## 라이센스

MIT License
