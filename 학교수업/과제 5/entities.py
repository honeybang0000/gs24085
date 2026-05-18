# =============================================
# entities.py - 객체 정의
# Snake(뱀)와 Food(먹이) 클래스를 정의합니다.
# =============================================

import random
from settings import GRID_COUNT, UP, DOWN, LEFT, RIGHT


class Snake:
    """
    뱀 객체 (has-a 관계: Snake는 body(위치 리스트)를 가진다)
    - body: 뱀의 몸 위치 리스트. body[0]이 머리
    - direction: 현재 이동 방향
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """뱀을 초기 상태(맵 중앙, 길이 3)로 초기화"""
        cx, cy = GRID_COUNT // 2, GRID_COUNT // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.grew = False  # 이번 스텝에 성장했는지 여부

    def get_head(self):
        """머리 위치 반환"""
        return self.body[0]

    def move(self, action):
        """
        action에 따라 방향 변경 후 이동
        - 반대 방향으로는 전환 불가 (현재 방향 유지)
        """
        # 반대 방향 전환 방지
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if action != opposites.get(self.direction):
            self.direction = action

        # 방향에 따른 이동량
        dx, dy = 0, 0
        if self.direction == UP:    dy = -1
        elif self.direction == DOWN: dy = 1
        elif self.direction == LEFT: dx = -1
        elif self.direction == RIGHT: dx = 1

        hx, hy = self.get_head()
        new_head = (hx + dx, hy + dy)

        # 새 머리를 앞에 추가
        self.body.insert(0, new_head)

        # 성장하지 않은 경우 꼬리 제거
        if not self.grew:
            self.body.pop()
        else:
            self.grew = False

    def grow(self):
        """다음 이동 시 몸이 길어지도록 표시"""
        self.grew = True

    def check_collision(self):
        """벽 또는 자기 몸과 충돌 여부 반환"""
        hx, hy = self.get_head()
        # 벽 충돌
        if not (0 <= hx < GRID_COUNT and 0 <= hy < GRID_COUNT):
            return True
        # 자기 몸 충돌 (머리 제외)
        if (hx, hy) in self.body[1:]:
            return True
        return False

    def get_length(self):
        return len(self.body)


class Food:
    """
    먹이 객체
    - position: 현재 먹이 위치
    """

    def __init__(self):
        self.position = (0, 0)

    def respawn(self, snake_body):
        """뱀 몸통을 피해 빈 칸에 먹이를 새로 생성"""
        all_cells = [(x, y) for x in range(GRID_COUNT) for y in range(GRID_COUNT)]
        empty_cells = [c for c in all_cells if c not in snake_body]
        if empty_cells:
            self.position = random.choice(empty_cells)

    def get_position(self):
        return self.position
