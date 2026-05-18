# =============================================
# env.py - 강화학습 환경 (Q-learning / DQN 공통)
# - get_state()     : Q-learning용 (튜플, 11개 이진값)
# - get_dqn_state() : DQN용 (numpy array, 16개 실수값)
# =============================================

import numpy as np
from entities import Snake, Food
from settings import (
    GRID_COUNT, UP, DOWN, LEFT, RIGHT,
    REWARD_FOOD, REWARD_COLLISION,
    REWARD_CLOSER, REWARD_FARTHER, REWARD_STEP
)


class SnakeEnv:
    """
    Snake 환경 - Q-learning과 DQN이 함께 사용
    step()의 반환값은 동일하지만
    상태 표현 방식이 다름
    """

    def __init__(self, mode='ql'):
        """
        mode: 'ql' = Q-learning, 'dqn' = DQN
        모드에 따라 reset/step이 다른 상태를 반환
        """
        self.mode = mode
        self.snake = Snake()
        self.food  = Food()
        self.score = 0
        self.steps = 0
        self.food.respawn(self.snake.body)

    def reset(self):
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.score = 0
        self.steps = 0
        return self._get_state()

    def step(self, action):
        self.steps += 1
        prev_dist = self._dist_to_food()

        self.snake.move(action)

        if self.snake.check_collision():
            return self._get_state(), REWARD_COLLISION, True

        curr_dist = self._dist_to_food()

        if self.snake.get_head() == self.food.get_position():
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1
            reward = REWARD_FOOD
        else:
            reward = REWARD_CLOSER if curr_dist < prev_dist else REWARD_FARTHER
            reward += REWARD_STEP

        return self._get_state(), reward, False

    def _get_state(self):
        """모드에 따라 다른 상태 반환"""
        if self.mode == 'dqn':
            return self._get_dqn_state()
        return self._get_ql_state()

    # ─── Q-learning 상태 ─────────────────────────────
    def _get_ql_state(self):
        """
        11개 이진값 튜플
        [위험_직진, 위험_좌, 위험_우,
         먹이_위, 먹이_아래, 먹이_왼, 먹이_오른,
         방향_상, 방향_하, 방향_좌, 방향_우]
        """
        head = self.snake.get_head()
        direction = self.snake.direction

        dir_s, dir_l, dir_r = self._get_relative_dirs(direction)

        danger_s = self._is_danger(head, dir_s)
        danger_l = self._is_danger(head, dir_l)
        danger_r = self._is_danger(head, dir_r)

        hx, hy = head
        fx, fy = self.food.get_position()

        return (
            int(danger_s), int(danger_l), int(danger_r),
            int(fy < hy), int(fy > hy), int(fx < hx), int(fx > hx),
            int(direction == UP), int(direction == DOWN),
            int(direction == LEFT), int(direction == RIGHT)
        )

    # ─── DQN 상태 ────────────────────────────────────
    def _get_dqn_state(self):
        """
        16개 실수값 numpy array
        Q-learning보다 훨씬 풍부한 상태 정보

        [주변 8칸 위험(몸+벽),   ← Q-learning은 3방향만 봤음
         먹이 방향 4개,
         현재 방향 4개]

        주변 8칸:
          ul  u  ur
          l   H   r
          dl  d  dr
        """
        hx, hy = self.snake.get_head()
        body_set = set(self.snake.body[1:])

        def is_blocked(x, y):
            if not (0 <= x < GRID_COUNT and 0 <= y < GRID_COUNT):
                return 1.0   # 벽
            if (x, y) in body_set:
                return 1.0   # 몸통
            return 0.0

        # 주변 8칸 위험 감지 (상단부터 시계방향)
        danger_u  = is_blocked(hx,   hy-1)
        danger_ur = is_blocked(hx+1, hy-1)
        danger_r  = is_blocked(hx+1, hy  )
        danger_dr = is_blocked(hx+1, hy+1)
        danger_d  = is_blocked(hx,   hy+1)
        danger_dl = is_blocked(hx-1, hy+1)
        danger_l  = is_blocked(hx-1, hy  )
        danger_ul = is_blocked(hx-1, hy-1)

        # 먹이 방향 (4개)
        fx, fy = self.food.get_position()
        food_u = float(fy < hy)
        food_d = float(fy > hy)
        food_l = float(fx < hx)
        food_r = float(fx > hx)

        # 현재 방향 (4개)
        d = self.snake.direction
        dir_u = float(d == UP)
        dir_d = float(d == DOWN)
        dir_l = float(d == LEFT)
        dir_r = float(d == RIGHT)

        state = np.array([
            danger_u, danger_ur, danger_r, danger_dr,
            danger_d, danger_dl, danger_l, danger_ul,  # 8개
            food_u, food_d, food_l, food_r,            # 4개
            dir_u, dir_d, dir_l, dir_r                 # 4개
        ], dtype=np.float32)                           # 총 16개

        return state

    # ─── 공통 유틸 ───────────────────────────────────
    def _dist_to_food(self):
        hx, hy = self.snake.get_head()
        fx, fy = self.food.get_position()
        return abs(hx - fx) + abs(hy - fy)

    def _get_relative_dirs(self, direction):
        dir_map = {
            UP:    ((0,-1), (-1,0), (1,0)),
            DOWN:  ((0,1),  (1,0),  (-1,0)),
            LEFT:  ((-1,0), (0,1),  (0,-1)),
            RIGHT: ((1,0),  (0,-1), (0,1)),
        }
        return dir_map[direction]

    def _is_danger(self, head, delta):
        hx, hy = head
        dx, dy = delta
        nx, ny = hx+dx, hy+dy
        if not (0 <= nx < GRID_COUNT and 0 <= ny < GRID_COUNT):
            return True
        if (nx, ny) in self.snake.body[1:]:
            return True
        return False

    def get_snake(self):  return self.snake
    def get_food(self):   return self.food
    def get_score(self):  return self.score
