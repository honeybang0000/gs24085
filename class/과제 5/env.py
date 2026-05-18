# =============================================
# env.py - 강화학습 환경 (Environment)
# 상태 생성, 보상 계산, 종료 판단을 담당합니다.
# =============================================

import math
from entities import Snake, Food
from settings import (
    GRID_COUNT, UP, DOWN, LEFT, RIGHT,
    REWARD_FOOD, REWARD_COLLISION, REWARD_CLOSER,
    REWARD_FARTHER, REWARD_STEP
)


class SnakeEnv:
    """
    Snake 강화학습 환경
    - Agent(rl_agent.py)가 이 환경과 상호작용함
    - step() 호출 → (다음상태, 보상, 종료여부) 반환
    """

    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.steps = 0
        self.food.respawn(self.snake.body)

    def reset(self):
        """환경 초기화, 초기 상태 반환"""
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.score = 0
        self.steps = 0
        return self._get_state()

    def step(self, action):
        """
        행동(action)을 수행하고 결과 반환
        Returns: (next_state, reward, done)
        """
        self.steps += 1

        # 이동 전 먹이까지 거리
        prev_dist = self._dist_to_food()

        # 뱀 이동
        self.snake.move(action)

        # 충돌 체크
        if self.snake.check_collision():
            return self._get_state(), REWARD_COLLISION, True

        # 이동 후 먹이까지 거리
        curr_dist = self._dist_to_food()

        # 먹이 먹기 체크
        if self.snake.get_head() == self.food.get_position():
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1
            reward = REWARD_FOOD
        else:
            # 거리 기반 보상
            if curr_dist < prev_dist:
                reward = REWARD_CLOSER
            else:
                reward = REWARD_FARTHER
            reward += REWARD_STEP  # 매 스텝 패널티

        return self._get_state(), reward, False

    def _dist_to_food(self):
        """머리와 먹이 사이의 맨해튼 거리"""
        hx, hy = self.snake.get_head()
        fx, fy = self.food.get_position()
        return abs(hx - fx) + abs(hy - fy)

    def _get_state(self):
        """
        상태(State) 계산 - Q-table 인덱스로 사용할 튜플 반환

        상태 구성 (11개 이진 값):
        [위험_직진, 위험_좌회전, 위험_우회전,
         먹이_위, 먹이_아래, 먹이_왼쪽, 먹이_오른쪽,
         방향_상, 방향_하, 방향_좌, 방향_우]
        """
        head = self.snake.get_head()
        direction = self.snake.direction

        # 현재 방향 기준으로 직진/좌/우 방향 계산
        dir_straight, dir_left, dir_right = self._get_relative_directions(direction)

        # 각 방향의 위험 여부
        danger_straight = self._is_danger(head, dir_straight)
        danger_left     = self._is_danger(head, dir_left)
        danger_right    = self._is_danger(head, dir_right)

        # 먹이 방향
        hx, hy = head
        fx, fy = self.food.get_position()
        food_up    = int(fy < hy)
        food_down  = int(fy > hy)
        food_left  = int(fx < hx)
        food_right = int(fx > hx)

        # 현재 이동 방향 (원핫)
        dir_up    = int(direction == UP)
        dir_down  = int(direction == DOWN)
        dir_left  = int(direction == LEFT)
        dir_right = int(direction == RIGHT)

        return (
            int(danger_straight), int(danger_left), int(danger_right),
            food_up, food_down, food_left, food_right,
            dir_up, dir_down, dir_left, dir_right
        )

    def _get_relative_directions(self, direction):
        """현재 방향 기준 직진/좌/우 방향 벡터 반환"""
        # (dx, dy) 형태로 반환
        dir_map = {
            UP:    ((0, -1), (-1, 0), (1, 0)),   # 직진=위, 좌=왼, 우=오른
            DOWN:  ((0, 1),  (1, 0),  (-1, 0)),
            LEFT:  ((-1, 0), (0, 1),  (0, -1)),
            RIGHT: ((1, 0),  (0, -1), (0, 1)),
        }
        return dir_map[direction]

    def _is_danger(self, head, delta):
        """head에서 delta 방향 한 칸이 위험(벽 or 몸)한지 판단"""
        hx, hy = head
        dx, dy = delta
        nx, ny = hx + dx, hy + dy
        if not (0 <= nx < GRID_COUNT and 0 <= ny < GRID_COUNT):
            return True
        if (nx, ny) in self.snake.body[1:]:
            return True
        return False

    def get_snake(self):
        return self.snake

    def get_food(self):
        return self.food

    def get_score(self):
        return self.score
