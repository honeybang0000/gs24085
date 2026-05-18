# =============================================
# settings.py - 공통 설정 관리
# 모든 상수와 설정값을 한 곳에서 관리합니다.
# =============================================

# --- 화면 / 맵 설정 ---
GRID_SIZE = 20          # 격자 한 칸의 픽셀 크기
GRID_COUNT = 20         # 격자 개수 (20x20 맵)
SCREEN_WIDTH = GRID_SIZE * GRID_COUNT       # 400
SCREEN_HEIGHT = GRID_SIZE * GRID_COUNT      # 400
FPS_TRAINING = 60       # 학습 중 속도 (빠르게)
FPS_DISPLAY = 10        # 결과 시연 속도 (눈에 보이게)

# --- 색상 ---
COLOR_BG        = (15, 15, 25)
COLOR_GRID      = (25, 25, 40)
COLOR_SNAKE     = (50, 220, 100)
COLOR_SNAKE_HEAD= (100, 255, 150)
COLOR_FOOD      = (255, 80, 80)
COLOR_TEXT      = (200, 200, 200)
COLOR_UI_BG     = (20, 20, 35)

# --- Q-learning 하이퍼파라미터 ---
ALPHA   = 0.1       # 학습률 (얼마나 빠르게 배울까)
GAMMA   = 0.95      # 할인율 (미래 보상을 얼마나 중요하게 볼까)
EPSILON_START   = 1.0   # 초기 탐험율 (처음엔 무작위)
EPSILON_MIN     = 0.01  # 최소 탐험율
EPSILON_DECAY   = 0.995 # 탐험율 감소 속도

# --- 학습 설정 ---
EPISODES        = 1000  # 총 학습 에피소드 수
MAX_STEPS       = 1000  # 한 에피소드 최대 스텝
SHOW_EVERY      = 100   # N 에피소드마다 시각화

# --- 보상 설계 ---
REWARD_FOOD     =  50   # 먹이 먹었을 때
REWARD_COLLISION= -100  # 벽 or 자기 몸 충돌
REWARD_CLOSER   =   1   # 먹이에 가까워짐
REWARD_FARTHER  =  -1.5 # 먹이에서 멀어짐
REWARD_STEP     =  -0.1 # 매 스텝 패널티 (빙빙 도는 것 방지)

# --- 방향 정의 ---
UP    = 0
DOWN  = 1
LEFT  = 2
RIGHT = 3
ACTIONS = [UP, DOWN, LEFT, RIGHT]
