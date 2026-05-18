# ============================================================
# 3주차 실습1: 적 피하기 게임 - SpiralEnemy 추가하기
# ============================================================
# 목표: 다형성(상속 + 오버라이딩)을 활용하여
#       나선형으로 움직이는 SpiralEnemy를 추가하세요!
#
# 규칙:
#   1. Enemy 클래스를 상속받아 SpiralEnemy를 만든다
#   2. update()를 오버라이딩하여 나선형 이동 구현
#   3. 메인 루프의 for문은 절대 수정하지 않는다! (다형성!)
# ============================================================

import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polymorphism Example")
clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
RED = (230, 80, 80)
GREEN = (30, 150, 100)
PURPLE = (150, 50, 200)
BLUE = (70, 130, 255)

font = pygame.font.SysFont("malgungothic", 22)


# ── 부모 클래스: Enemy ───────────────────────────────────────

class Enemy:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.radius = 18
        self.color = color

    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# ── 자식 클래스: StraightEnemy (직선 이동) ───────────────────

class StraightEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.speed = random.uniform(2, 4)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -20
            self.x = random.randint(20, WIDTH - 20)


# ── 자식 클래스: ZigzagEnemy (지그재그 이동) ─────────────────

class ZigzagEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, PURPLE)
        self.speed = 2.5
        self.angle = random.uniform(0, math.pi * 2)

    def update(self):
        self.y += self.speed
        self.angle += 0.1
        self.x += math.sin(self.angle) * 5
        if self.y > HEIGHT:
            self.y = -20
            self.x = random.randint(20, WIDTH - 20)


# ── TODO: SpiralEnemy 클래스를 작성하세요 ────────────────────
# 조건:
#   - Enemy 클래스를 상속받는다
#   - 색상은 GREEN을 사용한다
#   - __init__에서 필요한 속성을 추가한다:
#       self.speed = 1.5      (아래로 내려가는 속도)
#       self.angle = 0        (현재 각도)
#       self.angle_speed = 0.05  (각도 변화 속도)
#       self.spiral_radius = 3   (나선의 반지름, 점점 커짐)
#   - update()에서 나선형 이동을 구현한다:
#       1) self.angle을 self.angle_speed만큼 증가
#       2) self.spiral_radius를 0.02만큼 증가
#       3) self.x에 cos(angle) * spiral_radius 를 더한다
#       4) self.y에 self.speed를 더한다 (아래로 이동)
#       5) 화면 아래로 벗어나면 위로 리셋 (다른 적들처럼)
#          이때 spiral_radius도 3으로 리셋!

# 여기에 SpiralEnemy 클래스를 작성하세요 ↓↓↓




# ── 플레이어 ─────────────────────────────────────────────────

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.radius = 20
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 3)
        pygame.draw.circle(surface, BLACK, (int(self.x) - 5, int(self.y) - 4), 2)
        pygame.draw.circle(surface, BLACK, (int(self.x) + 5, int(self.y) - 4), 2)


# ── 객체 생성 ────────────────────────────────────────────────

player = Player()
enemies = []

for _ in range(4):
    enemies.append(StraightEnemy(random.randint(40, 860), random.randint(0, 200)))

for _ in range(3):
    enemies.append(ZigzagEnemy(random.randint(40, 860), random.randint(0, 200)))

# TODO: SpiralEnemy 객체 3개를 생성하여 enemies 리스트에 추가하세요 ↓↓↓



# ── 메인 루프 (수정하지 마세요!) ─────────────────────────────

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update()

    # ★ 다형성! 이 for문은 수정하지 않는다!
    for enemy in enemies:
        enemy.update()

    screen.fill(WHITE)

    player.draw(screen)

    # ★ 다형성! 이 for문도 수정하지 않는다!
    for enemy in enemies:
        enemy.draw(screen)

    text1 = font.render("red: straight / purple: zigzag / green: spiral", True, BLACK)
    screen.blit(text1, (20, 20))

    pygame.display.flip()
    clock.tick(60)
