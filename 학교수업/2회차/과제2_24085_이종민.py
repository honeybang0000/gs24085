# 상속 적용
import pygame
import random
import math
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("상속")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 20)

# color
BLUE = (70, 70, 255)
RED = (230, 80, 80)
GOLD = (255, 200, 0)
GREEN = (80, 200, 120)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)

def random_position(margin=40):
    x = random.randint(margin, WIDTH - margin)
    y = random.randint(margin, HEIGHT - margin)
    return x, y

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Parent - 공통 데이터와 기능을 가지고 있음
class GameObject:
    def __init__(self, x, y, radius, color):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.color = color
        self.alive = True

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        # 자식클래스에서 필요한 대로 각기 구현됨 --> 오버라이딩
        pass

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def collides_with(self, other):
        return self.distance_to(other) < self.radius + other.radius

# Child  - Player, Enemy, Coin은 GameObject 클래스로부터 상속받음.
class Player(GameObject):
    def __init__(self, x, y):
        # 부모의 공통 초기화 재사용
        super().__init__(x, y, radius=20, color=BLUE)
        self.speed = 5
        self.score = 0
        self.hp = 3

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

        # 화면 밖으로 못 나가게 처리
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, surface):
        super().draw(surface)
        # 테두리 추가
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 3)
        # 눈추가
        pygame.draw.circle(surface, BLACK, (int(self.x) - 5, int(self.y) - 4), 2)
        pygame.draw.circle(surface, BLACK, (int(self.x) + 5, int(self.y) - 4), 2)


class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, radius=18, color=RED)
        self.speed = random.uniform(1.2, 2.0)

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, surface):
        super().draw(surface)
        # 눈 추가!!
        pygame.draw.circle(surface, BLACK, (int(self.x) - 5, int(self.y) - 4), 2)
        pygame.draw.circle(surface, BLACK, (int(self.x) + 5, int(self.y) - 4), 2)


class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, radius=12, color=GOLD)
        self.base_radius = 12
        self.t = 0

    def update(self):
        # 크기가 살짝 커졌다 작아졌다 하도록
        self.t += 0.12
        self.radius = int(self.base_radius + math.sin(self.t) * 2)

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.circle(surface, WHITE, (int(self.x) - 3, int(self.y) - 3), 3)


class Drug(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, radius=12, color=GREEN)
        self.base_radius = 12
        self.t = 0

    def update(self):
        # 크기가 살짝 커졌다 작아졌다 하도록
        self.t += 0.12
        self.radius = int(self.base_radius + math.sin(self.t) * 2)

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.circle(surface, WHITE, (int(self.x) - 3, int(self.y) - 3), 3)



class Game:

    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.coins = []
        self.drugs = []
        for _ in range(5):
            self.enemies.append(Enemy(*random_position()))
        for _ in range(8):
            self.coins.append(Coin(*random_position()))
        for _ in range(1):
            self.drugs.append(Drug(*random_position()))
        self.running = True
        self.game_over = False

    # 이벤트 처리
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # 게임 업데이트
    def update(self):
        if self.game_over:
            return
        self.player.update()
        for enemy in self.enemies:
            enemy.update(self.player)
        for coin in self.coins:
            coin.update()
        for drug in self.drugs:
            drug.update()
        self.check_collisions()

    # 충돌 처리
    def check_collisions(self):
        # 코인 먹기
        for coin in self.coins:
            if coin.alive and self.player.collides_with(coin):
                coin.alive = False
                self.player.score += 1
        #먹힌 코인 제거
        self.coins = [c for c in self.coins if c.alive]
        #코인이 다 없어지면 새로 생성하자
        if len(self.coins) == 0:
            for _ in range(8):
                self.coins.append(Coin(*random_position()))

        for drug in self.drugs:
            if drug.alive and self.player.collides_with(drug):
                drug.alive = False
                self.player.hp += 1
        self.drugs = [c for c in self.drugs if c.alive]
        if len(self.drugs) == 0:
            for _ in range(1):
                self.drugs.append(Drug(*random_position()))

        # 적 충돌
        for enemy in self.enemies:
            if self.player.collides_with(enemy):
                self.player.hp -= 1
                #player를 중앙으로 되돌리기
                self.player.x = WIDTH // 2
                self.player.y = HEIGHT // 2
                self.enemies = [Enemy(*random_position()) for _ in range(5)]
                if self.player.hp <= 0:
                    self.game_over = True
                break

    # 화면 그리기
    def draw(self):
        screen.fill(WHITE)
        # 공통 부모 덕분에 모든 객체를 같은 방식으로 다룰 수 있음
        all_objects = [self.player] + self.enemies + self.coins + self.drugs
        # 상속
        for obj in all_objects:
            obj.draw(screen)

        draw_text(f"점수: {self.player.score}", 20, 20)
        draw_text(f"체력(적과 충돌하면 줄어듬): {self.player.hp}", 20, 55)
        draw_text("방향키로 이동", 20, 90, RED)

        if self.game_over:
            draw_text("GAME OVER", WIDTH // 2 - 80, HEIGHT // 2 - 20, RED)
        pygame.display.flip()

    # 메인 루프를 메서드로 넣어보자.
    def run(self):
        while self.running:
            clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

game = Game()
game.run()

pygame.quit()
sys.exit()

# 1. GameObject 클래스는 부모클래스이다 distance_to()와 collides_with() 함수가 부모 클래스에 있는 것이 왜 좋은 설계인지 설명하고,
# GameObject가 없다면 어떻게 구현될지 서술하시오.(5줄이상)

# GameObject는 모든 객체(Player, Enemy, Coin, Drug)의 공통 부모 클래스이기 때문에 공통적으로 필요한 기능을 한 곳에 모아두는 것이 좋은 설계이다.
# distance_to()와 collides_with()는 모든 객체 간 거리 계산과 충돌 판정에 사용되므로
# 각 클래스에 따로 구현하는 것보다 부모 클래스에 두는 것이 코드 중복을 줄이고 유지보수를 쉽게 만든다.
# 이렇게 하면 어떤 객체든 collides_with()를 바로 사용할 수 있어 객체 간 상호작용을 일관되게 처리할 수 있다.
#
# 만약 GameObject가 없다면, Player, Enemy, Coin, Drug 각각의 클래스에 거리 계산과 충돌 판정 함수를 모두 따로 구현해야 한다.
# 이 경우 코드가 반복되고, 수정이 필요할 때 모든 클래스에서 각각 고쳐야 하므로 비효율적이고 오류 발생 가능성이 높아진다.

# 2.  아래 Player의 __init__함수에서 GameObject.__init__()을 직접 호출하지 않고 super().__init__를 사용한 이유를 설명하시오.
# class Player(GameObject):
#     def __init__(self, x, y):
#         super().__init__(x, y, radius=20, color=BLUE)

# super().__init__()를 사용하는 이유는 부모 클래스인 GameObject의 초기화 코드를 재사용하기 위해서이다.
# 직접 GameObject.__init__(self, ...)을 호출할 수도 있지만, super()를 사용하면 상속 구조가 변경되더라도 코드 수정 없이 자동으로
# 올바른 부모 클래스의 메서드를 호출할 수 있다.
# 또한 다중 상속 상황에서도 super()는 올바른 순서(MRO)에 따라 호출되므로 더 안전하고 유지보수에 유리하다.
# 즉, super()는 유연하고 확장 가능한 객체지향 설계를 가능하게 한다.


# 3. 과제2 제출 코드에서 오버라이딩 부분을 모두 찾아서 쓰고, 오버라이딩을 사용하는 이유를 서술하시오.

# 오버라이딩된 메서드
# 부모 클래스 GameObject의 메서드를 자식 클래스에서 재정의한 부분은 다음과 같다:
#
# update()
# Player.update()
# Enemy.update()
# Coin.update()
# Drug.update()
# draw()
# Player.draw()
# Enemy.draw()
# Coin.draw()
# Drug.draw()
# ✔ 오버라이딩을 사용하는 이유
#
# 오버라이딩은 부모 클래스의 메서드를 자식 클래스에서 자신의 역할에 맞게 다르게 동작하도록 수정하기 위해 사용된다.
# 예를 들어, Player는 키보드 입력으로 움직이고 Enemy는 플레이어를 따라 움직이며 Coin과 Drug은 크기가 변하는 애니메이션을 가진다
# 이처럼 같은 update() 메서드라도 각 객체마다 동작이 다르기 때문에 오버라이딩을 통해 각각의 행동을 정의한다.
# 또한 draw() 역시 기본 원 그리기는 같지만 눈이나 테두리 같은 추가 요소가 다르기 때문에 오버라이딩이 필요하다.
# 결과적으로 오버라이딩을 사용하면 같은 인터페이스(update, draw)를 유지하면서 객체마다 다른 행동을 구현할 수 있어 다형성(polymorphism)을 실현할 수 있다.


