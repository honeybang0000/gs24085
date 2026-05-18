# =============================================
# entities.py - 객체 정의 (Q-learning / DQN 공통 재사용)
# Snake, Food 클래스
# =============================================

import random
from settings import GRID_COUNT, UP, DOWN, LEFT, RIGHT


class Snake:
    """
    뱀 객체
    - body[0] = 머리
    - Q-learning, DQN 모두 이 클래스를 그대로 사용
    """

    def __init__(self):
        self.reset()

    def reset(self):
        cx, cy = GRID_COUNT // 2, GRID_COUNT // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.grew = False

    def get_head(self):
        return self.body[0]

    def move(self, action):
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if action != opposites.get(self.direction):
            self.direction = action

        dx, dy = 0, 0
        if self.direction == UP:     dy = -1
        elif self.direction == DOWN: dy =  1
        elif self.direction == LEFT: dx = -1
        elif self.direction == RIGHT:dx =  1

        hx, hy = self.get_head()
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)

        if not self.grew:
            self.body.pop()
        else:
            self.grew = False

    def grow(self):
        self.grew = True

    def check_collision(self):
        hx, hy = self.get_head()
        if not (0 <= hx < GRID_COUNT and 0 <= hy < GRID_COUNT):
            return True
        if (hx, hy) in self.body[1:]:
            return True
        return False

    def get_length(self):
        return len(self.body)


class Food:
    """먹이 객체 - Q-learning / DQN 공통 재사용"""

    def __init__(self):
        self.position = (0, 0)

    def respawn(self, snake_body):
        all_cells = [(x, y) for x in range(GRID_COUNT) for y in range(GRID_COUNT)]
        empty_cells = [c for c in all_cells if c not in snake_body]
        if empty_cells:
            self.position = random.choice(empty_cells)

    def get_position(self):
        return self.position
