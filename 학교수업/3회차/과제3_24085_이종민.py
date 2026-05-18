import pygame
import random
import math
from abc import ABC, abstractmethod

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polymorphism Practice")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 32)

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BLUE = (70, 130, 255)
RED = (220, 70, 70)
GREEN = (80, 200, 120)
GOLD = (255, 200, 0)
PURPLE = (170, 90, 220)

#Add to code hear
#GameObject 추상 클래스를 추가하시오.

class GameObject(ABC):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.alive = True
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def draw(self):
        pass
    @abstractmethod
    def interact(self):
        pass
    def collides_with(self, other):
        if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= (self.radius+other.radius) ** 2:
            return True
        return False

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 22, BLUE)
        self.speed = 5
        self.hp = 30
        self.score = 0

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
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 3)
        # 눈 추가!!
        pygame.draw.circle(surface, BLACK, (int(self.x) - 5, int(self.y) - 4), 2)
        pygame.draw.circle(surface, BLACK, (int(self.x) + 5, int(self.y) - 4), 2)

    def interact(self, player):
        pass

    def __add__(self, other):
        if isinstance(other, Coin):
            self.score += other.value
            other.alive = False
            return f"Coin +{other.value}"
        elif isinstance(other, Power):
            self.hp += other.heal_amount
            other.alive = False
            return f"HP +{other.heal_amount}"
        return None


class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 6, BLACK)
        self.speed = 8
        self.damage = 1

    def update(self):
        self.y -= self.speed
        if self.y < -10:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def interact(self, player):
        pass

    def __add__(self, other):
        if isinstance(other, Enemy):
            other.hp -= self.damage
            self.alive = False
            return f"Hit! Enemy HP: {max(0, other.hp)}"
        return None

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 18, RED)
        self.speed = random.uniform(1.5, 3.0)
        self.direction = random.choice([-1, 1])
        self.hp = 3

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.direction *= -1
        if self.hp <= 0:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        hp_text = font.render(str(self.hp), True, WHITE)
        hp_rect = hp_text.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(hp_text, hp_rect)

    def interact(self, player):
        player.hp -= 1
        return "Ouch! HP -1"

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 12, GOLD)
        self.value = 10
        self.angle = 0

    def update(self):
        self.angle += 0.08

    def draw(self, surface):
        animated_radius = self.radius + int(2 * math.sin(self.angle))
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            max(6, animated_radius)
        )
        pygame.draw.circle(surface, WHITE, (int(self.x) - 3, int(self.y) - 3), 3)

    def interact(self, player):
        return player + self

class Power(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 14, GREEN)
        self.heal_amount = 1
        self.dy = 1
        self.base_y = y

    def update(self):
        self.y += self.dy
        if self.y > self.base_y + 10 or self.y < self.base_y - 10:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(surface, WHITE, (int(self.x), int(self.y - 6)), (int(self.x), int(self.y + 6)), 2)
        pygame.draw.line(surface, WHITE, (int(self.x - 6), int(self.y)), (int(self.x + 6), int(self.y)), 2)

    def interact(self, player):
        return player + self


class MessageBox:
    def __init__(self):
        self.text = "Arrow keys: Move | Spacebar: Shoot"
        self.timer = 0

    def set_message(self, text):
        if text:
            self.text = text
            self.timer = 120

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, surface):
        color = PURPLE if self.timer > 0 else BLACK
        text_img = font.render(self.text, True, color)
        surface.blit(text_img, (20, 20))

player = Player(WIDTH // 2, HEIGHT // 2)
message_box = MessageBox()

objects = []
bullets = []

for _ in range(5):
    objects.append(Enemy(random.randint(60, WIDTH - 60), random.randint(100, HEIGHT - 60)))

for _ in range(6):
    objects.append(Coin(random.randint(60, WIDTH - 60), random.randint(100, HEIGHT - 60)))

for _ in range(3):
    objects.append(Power(random.randint(60, WIDTH - 60), random.randint(100, HEIGHT - 60)))

running = True
game_over = False

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x, player.y - player.radius))
                message_box.set_message("Bullet fired!")

    if not game_over:
        player.update()
        for obj in objects:
            obj.update()
        for bullet in bullets:
            bullet.update()

        message_box.update()

        for obj in objects:
            if obj.alive and player.collides_with(obj):
                result = obj.interact(player)
                message_box.set_message(result)

        for bullet in bullets:
            if not bullet.alive:
                continue

            for obj in objects:
                if isinstance(obj, Enemy) and obj.alive and bullet.collides_with(obj):
                    result = bullet + obj
                    message_box.set_message(result)
                    break

        # 죽은 객체 제거
        objects = [obj for obj in objects if obj.alive]
        bullets = [bullet for bullet in bullets if bullet.alive]

        if player.hp <= 0:
            game_over = True
            message_box.set_message("Game Over")

    else:
        message_box.update()

    drawables = [player] + objects + bullets + [message_box]

    for obj in drawables:
        obj.draw(screen)

    hp_text = font.render(f"HP: {player.hp}", True, BLACK)
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    enemy_count = sum(1 for obj in objects if isinstance(obj, Enemy))
    enemy_text = font.render(f"Enemies: {enemy_count}", True, BLACK)

    screen.blit(hp_text, (20, 55))
    screen.blit(score_text, (20, 85))
    screen.blit(enemy_text, (20, 115))

    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, over_rect)

    pygame.display.flip()

pygame.quit()

# 1.  메인 루프(while문) 안의 result = obj.interact(player) 코드에서 어떤 일이 일어나는지 작성하고
# Enemy, Coin, Power의 interact()는 모두 같은 이름인데 왜 다른 동작을 하는지 쓰시오.

# 이 코드는 obj 객체가 player와 상호작용을 수행하도록 요청하는 것이다. 즉, 플레이어와 충돌한 객체가 자신의 interact() 메서드를 실행한다.
# 여기서 중요한 점은 obj가 무엇인지에 따라 실행되는 함수가 달라진다는 것이다.
# Enemy → 플레이어 체력 감소 (hp -= 1)
# Coin → 점수 증가 (player + coin)
# Power → 체력 증가 (player + power)
# 이처럼 interact()라는 같은 이름의 메서드를 사용하지만 각 클래스에서 다르게 구현되어 있기 때문에 서로 다른 동작이 수행된다.
# 이는 오버라이딩에 의한 다형성이며, 실행 시점에 어떤 객체인지에 따라 메서드가 결정되는 동적 바인딩이 일어난다.

# 2.  덕 타이핑이 구현된 클래스와 메인 루프에서 덕타이핑을 이용한 다형성이 구현된 코드를 찾아 작성하고 덕타이핑과 오버라이딩의 차이점을 설명하시오.

# 덕 타이핑이 구현된 부분
# drawables = [player] + objects + bullets + [message_box]
#
# for obj in drawables:
#     obj.draw(screen)

# ✔ 참여 클래스
# Player, Enemy, Coin, Power, Bullet, MessageBox
# ✔ 설명
# 이 코드에서는 객체의 타입을 확인하지 않고 단순히 draw() 메서드가 있으면 호출한다.
# 즉, MessageBox는 GameObject를 상속하지 않았지만 draw() 메서드가 있기 때문에 동일하게 처리된다.
# 👉 이것이 **덕 타이핑 (Duck Typing)**이다 ("오리처럼 걷고 울면 오리다")
#
# ✔ 덕 타이핑 vs 오버라이딩
# 구분	덕 타이핑	오버라이딩
# 기준	메서드 존재 여부	상속 관계
# 필요 조건	같은 이름의 메서드만 있으면 됨	부모 클래스 필요
# 예시	MessageBox.draw()	Player.draw(), Enemy.draw()
# 특징	더 유연함	구조적으로 안전함
#
# 👉 핵심:
# 오버라이딩 = 상속 기반
# 덕 타이핑 = 형태만 맞으면 OK

# 3.  메인루프의 result = bullet + obj 코드에서 실제로 호출되는 것은 어느 클래스의 무엇인지 쓰시오

# 이 코드는 다음을 호출한다:
# 👉 Bullet 클래스의 __add__() 메서드
# 즉, bullet.__add__(obj)가 실행된다.

# 4.   메인루프의 result = bullet + obj 에서 obj가 enemy일 때 이 코드가 의미하는 동작을 설명하시오.

# result = bullet + obj 에서 obj가 Enemy이면:
# Enemy의 hp 감소 (other.hp -= self.damage)
# Bullet 제거 (self.alive = False)
# 메시지 반환 ("Hit! Enemy HP: ...")
#
# 즉, 이 코드는 👉 총알이 적을 맞춰 데미지를 입히는 공격 처리를 의미한다.

# 5. 메인 루프에서 발생하는 다형성(polymorphism) 사례를 모두 찾아 각각 다음을 포함하여 설명하시오.
# 1. 해당 코드(구체적인 코드 형태로 제시)
# 2. 어떤 객체들이 참여하는지
# 3. 어떤 방식의 다형성인지 구분할 것
# - Abstract Class 기반 다형성
# - 덕 타이핑 기반 다형성
# - 메서드 오버라이딩 기반 다형성
# -연산자 오버로딩 기반 다형성
# 4. 왜 다형성이라고 볼 수 있는지 설명하시오

# ① Abstract Class 기반 다형성
#
# 코드
#
# for obj in objects:
#     obj.update()
#
# 참여 객체
#
# Enemy, Coin, Power
#
# 방식
#
# Abstract Class 기반 다형성
#
# 설명
# GameObject에서 update()를 추상 메서드로 정의하고 각 자식 클래스가 이를 구현한다. 같은 update() 호출이지만 객체마다 다르게 동작하므로 다형성이다.
#
# ② 메서드 오버라이딩 기반 다형성
#
# 코드
#
# obj.draw(screen)
#
# 참여 객체
#
# Player, Enemy, Coin, Power, Bullet
#
# 방식
#
# 오버라이딩 기반 다형성
#
# 설명
# 모든 클래스가 draw()를 각자 다르게 구현하였다.
# 같은 메서드 호출이지만 객체마다 다른 그림을 그리므로 다형성이다.
#
# ③ 덕 타이핑 기반 다형성
#
# 코드
#
# for obj in drawables:
#     obj.draw(screen)
#
# 참여 객체
#
# GameObject 계열 + MessageBox
#
# 방식
#
# 덕 타이핑
#
# 설명
# MessageBox는 상속 관계가 없지만 draw()가 존재하므로 같이 처리된다. 타입이 아니라 "행동" 기준으로 동작하므로 다형성이다.
#
# ④ 오버라이딩 기반 다형성 (interact)
#
# 코드
#
# result = obj.interact(player)
#
# 참여 객체
#
# Enemy, Coin, Power
#
# 방식
#
# 메서드 오버라이딩
#
# 설명
# 각 클래스가 interact()를 다르게 구현하여
# 충돌 시 서로 다른 결과를 만든다.
#
# ⑤ 연산자 오버로딩 기반 다형성
#
# 코드
#
# result = bullet + obj
#
# 참여 객체
#
# Bullet, Enemy
#
# 방식
#
# 연산자 오버로딩
#
# 설명
# + 연산자가 숫자가 아니라 객체 간 상호작용으로 사용된다. 객체에 따라 다른 의미를 가지므로 다형성이다.
