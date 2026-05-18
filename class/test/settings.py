# =============================================
# settings.py - 공통 설정 관리
# Q-learning + DQN 공통 설정값
# =============================================

# --- 화면 / 맵 설정 ---
GRID_SIZE   = 20
GRID_COUNT  = 20
SCREEN_WIDTH  = GRID_SIZE * GRID_COUNT   # 400
SCREEN_HEIGHT = GRID_SIZE * GRID_COUNT   # 400
FPS_TRAINING  = 0    # 0 = 최대 속도
FPS_DISPLAY   = 10   # 시연 속도

# --- 색상 ---
COLOR_BG         = (15, 15, 25)
COLOR_GRID       = (25, 25, 40)
COLOR_SNAKE      = (50, 220, 100)
COLOR_SNAKE_HEAD = (100, 255, 150)
COLOR_FOOD       = (255, 80, 80)
COLOR_TEXT       = (200, 200, 200)
COLOR_UI_BG      = (20, 20, 35)
COLOR_MENU_BG    = (10, 10, 20)
COLOR_HIGHLIGHT  = (100, 255, 150)
COLOR_DQN        = (80, 160, 255)
COLOR_QL         = (255, 180, 50)

# --- 방향 정의 ---
UP    = 0
DOWN  = 1
LEFT  = 2
RIGHT = 3
ACTIONS = [UP, DOWN, LEFT, RIGHT]

# --- 보상 설계 (공통) ---
REWARD_FOOD      =  50
REWARD_COLLISION = -100
REWARD_CLOSER    =   1.0
REWARD_FARTHER   =  -1.5
REWARD_STEP      =  -0.1

# =============================================
# Q-learning 전용 설정
# =============================================
QL_ALPHA          = 0.1
QL_GAMMA          = 0.95
QL_EPSILON_START  = 1.0
QL_EPSILON_MIN    = 0.01
QL_EPSILON_DECAY  = 0.995
QL_EPISODES       = 1000
QL_MAX_STEPS      = 500
QL_SHOW_EVERY     = 100

# =============================================
# DQN 전용 설정
# =============================================
DQN_GAMMA          = 0.95
DQN_LR             = 0.001       # 학습률 (신경망 optimizer)
DQN_EPSILON_START  = 1.0
DQN_EPSILON_MIN    = 0.01
DQN_EPSILON_DECAY  = 0.997
DQN_EPISODES       = 1000
DQN_MAX_STEPS      = 500
DQN_SHOW_EVERY     = 100
DQN_BATCH_SIZE     = 64          # 한 번에 학습할 샘플 수
DQN_MEMORY_SIZE    = 100_000     # 경험 버퍼 최대 크기
DQN_TARGET_UPDATE  = 500         # N 스텝마다 타겟 네트워크 갱신
DQN_STATE_SIZE     = 16          # 입력 상태 크기 (아래 참고)
DQN_ACTION_SIZE    = 4           # 출력 행동 수
