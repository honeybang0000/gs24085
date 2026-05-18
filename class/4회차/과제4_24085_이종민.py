#  새로운 아이템/Enemy를 설계하여 추가하세요.
#조건
#1. GameObject를 상속받아 새 클래스를 만들것
#2. 기존 objects 리스트를 그대로 활용할 것
#3. 새로 만들 클래스의 인스턴스의 상태를 __변수와  @property 또는 메서드로 관리할 것(중요!!)
import pygame
import random
import sys
from abc import ABC, abstractmethod
import math

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Encapsulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 24)
big_font = pygame.font.SysFont("malgungothic", 40)

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BLUE = (70, 130, 255)
RED = (220, 80, 80)
GOLD = (255, 210, 0)
GREEN = (80, 200, 120)
GRAY = (180, 180, 180)

class GameObject(ABC):
    def __init__(self):
        self.__alive = True

    @property
    def is_alive(self):
        return self.__alive

    def destroy(self):
        self.__alive = False

    @property
    def can_collide_with_player(self):
        return False

    @property
    def can_collide_with_bullet(self):
        return False

    @property
    def is_bullet(self):
        return False

    @property
    @abstractmethod
    def rect(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def on_player_collision(self, player):
        pass

    def on_bullet_collision(self, bullet, player):
        pass

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.__x = 100
        self.__y = 300
        self.__size = 40
        self.__speed = 5

        self.__max_hp = 100
        self.__hp = 100
        self.__score = 0
        self.__points = 0

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if isinstance(value, (int, float)):
            self.__x = max(0, min(WIDTH - self.__size, value))

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if isinstance(value, (int, float)):
            self.__y = max(0, min(HEIGHT - self.__size, value))

    @property
    def hp(self):
        return self.__hp

    @property
    def points(self):
        return self.__points

    @hp.setter
    def hp(self, value):
        if isinstance(value, (int, float)):
            self.__hp = max(0, min(self.__max_hp, int(value)))

    @property
    def max_hp(self):
        return self.__max_hp

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if isinstance(value, (int, float)):
            self.__score = max(0, int(value))
    @points.setter
    def points(self, value):
        if isinstance(value, (int, float)):
            self.__points = max(0, int(value))
    @property
    def is_dead(self):
        return not self.is_alive

    @property
    def rect(self):
        return pygame.Rect(int(self.__x), int(self.__y), self.__size, self.__size)

    def shoot(self):
        return Bullet(self.__x + self.__size, self.__y + self.__size // 2)

    def take_damage(self, amount):
        if amount >= 0 and self.is_alive:
            self.hp -= amount
            if self.__hp <= 0:
                self.destroy()

    def add_score(self, amount):
        if amount >= 0:
            self.score += amount

    def add_hp(self, amount):
        if amount >= 0:
            self.hp += amount
    def add_points(self, amount):
        if amount >=0:
            self.points += amount

    def update(self):
        if not self.is_alive:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.__speed
        if keys[pygame.K_RIGHT]:
            self.x += self.__speed
        if keys[pygame.K_UP]:
            self.y -= self.__speed
        if keys[pygame.K_DOWN]:
            self.y += self.__speed

    def draw(self, surface):
        color = GRAY if self.is_dead else BLUE
        pygame.draw.rect(surface, color, self.rect)


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.__radius = 20
        self.__speed = random.choice([3, 4, 5])
        self.reset()
        self.__speed_multiplier = 1.0

    @property
    def speed_multiplier(self):
        return self.__speed_multiplier

    @speed_multiplier.setter
    def speed_multiplier(self, value):
        self.__speed_multiplier = min(value, 3.0)

    @property
    def current_speed(self):
        return self.__speed * self.__speed_multiplier

    @property
    def can_collide_with_player(self):
        return True

    @property
    def can_collide_with_bullet(self):
        return True

    @property
    def rect(self):
        return pygame.Rect(
            int(self.__x - self.__radius),
            int(self.__y - self.__radius),
            self.__radius * 2,
            self.__radius * 2
        )

    def reset(self):
        self.__y = self.__radius
        self.__x = random.randint(50, WIDTH - 50)

    def update(self):
        self.__y += self.current_speed
        if self.__y > HEIGHT+self.__radius:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.__x), int(self.__y)), self.__radius)

    def on_player_collision(self, player):
        player.take_damage(1)

    def on_bullet_collision(self, bullet, player):
        if self.is_alive and bullet.is_alive:
            player.add_score(20)
            player.add_points(10)
            self.reset()
            bullet.destroy()
    @property # homing bullet에서 접근할 수 있게 getter 설정
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

class Coin(GameObject):
    def __init__(self):
        super().__init__()
        self.__radius = 12
        self.__dy = 2
        self.__direction = 1
        self.reset()
    @property
    def can_collide_with_player(self):
        return True

    @property
    def can_collide_with_bullet(self):
        return True

    @property
    def rect(self):
        return pygame.Rect(
            int(self.__x - self.__radius),
            int(self.__y - self.__radius),
            self.__radius * 2,
            self.__radius * 2
        )

    def reset(self):
        self.__x = random.randint(100, WIDTH - 50)
        self.__y = self.__radius

    def update(self):
        self.__y += self.__dy * self.__direction
        if self.__y > HEIGHT + self.__radius:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, GOLD, (int(self.__x), int(self.__y)), self.__radius)
        pygame.draw.circle(surface, BLACK, (int(self.__x), int(self.__y)), self.__radius, 2)

    def on_player_collision(self, player):
        player.add_score(10)
        self.reset()

    def on_bullet_collision(self, bullet, player):
        if self.is_alive and bullet.is_alive:
            player.add_score(50)
            self.reset()
            bullet.destroy()


class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        self.__speed = 10
        self.__radius = 5

    @property
    def is_bullet(self):
        return True

    @property
    def rect(self):
        return pygame.Rect(
            int(self.__x - self.__radius),
            int(self.__y - self.__radius),
            self.__radius * 2,
            self.__radius * 2
        )

    def update(self):
        self.__y -= self.__speed
        if self.__y < self.__radius:
            self.destroy()

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.__x), int(self.__y)), self.__radius)

class HomingBullet(GameObject): # 새로 만든 클래스, 유도탄 (궁극기 느낌)
    def __init__(self, x, y):
        super().__init__() # 상속
        self.__x=x # 네임 맹글링
        self.__y=y
        self.__speed=6
        self.__radius=6
    @property # 캡슐화 getter 설정, setter는 따로 없음.
    def is_bullet(self):
        return True
    @property
    def rect(self): # 추상클래스 상속, 오버라이딩
        return pygame.Rect(
            int(self.__x - self.__radius),
            int(self.__y - self.__radius),
            self.__radius * 2,
            self.__radius * 2
        )
    def update(self): # 추상클래스 상속, 오버라이딩
        target = None
        min_dist = float('inf')
        for obj in objects:
            if isinstance(obj, Enemy) and obj.is_alive: #obj가 적인지 판단
                dx = obj.x-self.__x
                dy = obj.y-self.__y
                dist=math.hypot(dx,dy) #obj가 적이면 적까지 거리 구하기
                if dist < min_dist:
                    min_dist = dist # 가장 가까운 적을 고른다.
                    target = obj # 가장 가까운 적을 고른다.
        if target: # 가장 가까운 적에 대해
            dx = target.x - self.__x # 거리 산정
            dy = target.y - self.__y # 거리 산정
            dist = math.hypot(dx, dy) # 거리 산정
            if dist != 0: # 만약 아직 적에 도달하지 않았다면
                self.__x += self.__speed * dx/dist # 그 쪽으로 이동 --> 유도탄
                self.__y += self.__speed * dy/dist # 그 쪽으로 이동 --> 유도탄
            if self.__x <0 or self.__x>WIDTH or self.__y<0 or self.__y>HEIGHT:
                self.destroy() # 밖으로 나가면 사망
    def draw(self, surface): # 추상 클래스 상속, 오버라이딩
        pygame.draw.circle(surface, (150,0,200), (int(self.__x), int(self.__y)), self.__radius)

class Heal(GameObject):

    def __init__(self):
        super().__init__() # 상속
        self.__radius = 50 # 네임 맹글링
        self.reset()
        self.__time = 50 # 회복할 수 있는 시간
        self.__realtime = 200 # 같은 위치에 남아 있는 시간

    @property # 캡슐화 getter 설정
    def can_collide_with_player(self):
        return True

    @property # 캡슐화 getter 설정, 추상메서드 상속, 오버라이딩
    def rect(self):
        return pygame.Rect(
            int(self.__x - self.__radius),
            int(self.__y - self.__radius),
            self.__radius * 2,
            self.__radius * 2
        )

    def reset(self): # 추상 메서드 상속, 오버라이딩
        self.__x = random.randint(self.__radius, WIDTH - self.__radius)
        self.__y = random.randint(self.__radius, HEIGHT - self.__radius)
        self.__time = 50
        self.__radius = 50
        self.__realtime = 200

    def update(self): # 추상 메서드 상속, 오버라이딩
        self.__realtime -= 1
        if self.__realtime <=0: # 200 프레임 지나면 다른 위치에 생성되게 설정
            self.reset()
        pass

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (int(self.__x), int(self.__y)), self.__radius)
        pygame.draw.circle(surface, BLACK, (int(self.__x), int(self.__y)), self.__radius, 2)

    def on_player_collision(self, player):
        self.__time -= 1
        self.__radius -= 1 # 회복 장판에 있으면 동그라미 크기 줄어들게 설정
        player.add_hp(1) # 회복 장판에 있으면 프래임당 생명 1회복
        if self.__time <= 0: # 만약 50HP 이미 먹었으면 다른 위치에 생기게 설정
            self.reset()

def draw_ui(surface, player):
    bar_x, bar_y = 20, 20
    bar_w, bar_h = 220, 24

    pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_w, bar_h))
    current_w = bar_w * (player.hp / player.max_hp)
    pygame.draw.rect(surface, GREEN, (bar_x, bar_y, current_w, bar_h))
    pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_w, bar_h), 2)
    pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_w, bar_h), 2)

    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, BLACK)
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    info_text = font.render("SPACE: Shoot   R: Restart   ESC: Quit", True, BLACK)
    points_text = font.render(f"Points: {player.points}", True, BLACK)

    surface.blit(hp_text, (20, 50))
    surface.blit(score_text, (20, 85))
    surface.blit(info_text, (20, 120))
    surface.blit(points_text, (20,155))

def draw_game_over(surface, player):
    msg1 = big_font.render("GAME OVER", True, RED)
    msg2 = font.render(f"Final Score: {player.score}", True, BLACK)
    msg3 = font.render("R: Restart   ESC: Quit", True, BLACK)

    surface.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, 220))
    surface.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, 280))
    surface.blit(msg3, (WIDTH // 2 - msg3.get_width() // 2, 320))

def create_objects():
    player = Player()
    objects = [player]

    for _ in range(6):
        objects.append(Enemy())

    for _ in range(10):
        objects.append(Coin())

    objects.append(Heal()) # 하나만 (장판은 하나씩만 만들어지게 )

    return player, objects

start_ticks = pygame.time.get_ticks() # 게임 시작 시간 기록

player, objects = create_objects()


while True:
    clock.tick(60)

    elasped_time = pygame.time.get_ticks() - start_ticks
    current_difficulty = 1.0 + (elasped_time / 10000) * 0.2

    # 시간에 따라 적이 내려오는 속도를 증가시키기 위한 방안

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if not player.is_dead and event.key == pygame.K_SPACE:
                objects.append(player.shoot())
            if not player.is_dead and event.key == pygame.K_RETURN and player.points>=100:
                player.points -= 100
                for _ in range(6):
                    objects.append(HomingBullet(player.x, player.y)) # 궁극기 한번에 유도탄 6개 발사
            # 같은 위치에 생성되게 만들어서 6번 튕기는 효과 구현 (유도 탁구공 같은 느낌)
            if player.is_dead and event.key == pygame.K_r:
                player, objects = create_objects()

    if not player.is_dead:
        for obj in objects:
            if isinstance(obj, Enemy):
                obj.speed_multiplier = current_difficulty # 시간에 따라 내려오는 속도 증가하도록 설정
            obj.update()
        bullets = [obj for obj in objects if obj.is_bullet]
        player_targets = [
            obj for obj in objects
            if obj is not player and obj.can_collide_with_player
        ]
        bullet_targets = [
            obj for obj in objects
            if obj is not player and obj.can_collide_with_bullet
        ]

        for obj in player_targets:
            if obj.is_alive and player.rect.colliderect(obj.rect):
                obj.on_player_collision(player)

        for bullet in bullets:
            for obj in bullet_targets:
                if bullet.is_alive and obj.is_alive and bullet.rect.colliderect(obj.rect):
                    obj.on_bullet_collision(bullet, player)

        objects = [obj for obj in objects if obj.is_alive or obj is player]

    screen.fill(WHITE)

    for obj in objects:
        obj.draw(screen)

    draw_ui(screen, player)

    if player.is_dead:
        draw_game_over(screen, player)

    pygame.display.flip()

# 1.   player._hp -= 10 대신
# player.take_damage(10) 또는 player.hp -= 10을 사용해야 하는 이유를 설명하시오.

# player._hp처럼 내부 변수에 직접 접근하면 클래스 내부에서 설정한 규칙(예: 최소값, 최대값, 사망 처리 등)이 무시된다.
#
# 반면 player.take_damage(10)이나 player.hp -= 10을 사용하면 HP가 0 이하로 내려가지 않도록 제한되고
# HP가 0이 되면 destroy()가 호출되는 등 객체의 상태를 안전하게 유지할 수 있다
# 즉, 메서드나 property를 사용하면 객체의 일관성과 안정성을 보장할 수 있기 때문에 직접 접근하면 안 된다.

# 2.  player.hp = player.hp + 20 대신
# player._hp += 20을 사용하면 어떤 문제가 발생할 수 있는지 설명하시오.

# player._hp += 20처럼 직접 값을 변경하면 다음과 같은 문제가 발생한다:
#
# 최대 HP(100)를 초과할 수 있음
# 음수나 비정상적인 값이 들어갈 가능성 있음
# 체력 관련 로직(예: 사망 처리)이 제대로 작동하지 않을 수 있음
#
# 반면 player.hp = player.hp + 20은 setter를 거치기 때문에 자동으로 0 ~ max_hp 범위로 제한된다.
#
# 👉 즉, 직접 접근하면 게임 규칙이 깨질 수 있다

# 3.  player가 무적 상태일 때 데미지를 받지 않도록 구현하려고 한다. 이를 Enemy에서 처리하는 것과 Player에서 처리하는 것 중 어떤 것이 더 적절한지 설명하시오.

# 👉 Player에서 처리하는 것이 더 적절하다.
#
# 이유:
#
# “무적 상태”는 Player의 상태(속성)이기 때문. Enemy는 단순히 공격을 시도하는 역할만 해야 한다
# Player가 “나는 지금 데미지를 받을 수 있는 상태인가?”를 판단해야 한다
# 만약 Enemy에서 처리하면:
#
# 모든 Enemy 클래스에 무적 조건을 넣어야 함 (비효율적)
# 코드 중복 발생
# 확장성 떨어짐
#
# 👉 따라서
# 상태의 주인은 Player → Player에서 처리하는 것이 객체지향적으로 올바른 설계이다.


# 4.    현재 hp가 0~100 사이로 제한되어 있다.
# 만약 최대 HP를 200으로 변경하려면
# 캡슐화가 잘 된 코드와 그렇지 않은 코드에서 어떤 차이가 발생하는지 설명하시오.

# ✔ 캡슐화가 잘 된 코드
# __max_hp = 200 한 줄만 수정하면 됨 setter가 자동으로 새로운 범위 적용
# 다른 코드 수정 필요 없음
#
# 👉 유지보수 매우 쉬움
#
# ✔ 캡슐화가 안 된 코드
# 여러 곳에서 직접 _hp를 수정하고 있다면
# 모든 코드에서 조건을 직접 바꿔야 함 (ex: 100 → 200)
# 실수로 일부만 수정하면 버그 발생
#
# 👉 유지보수 매우 어려움 + 오류 가능성 높음

# 5. @property를 쓰는 것과 get_hp() / set_hp() 메서드를 쓰는 것의 차이를 설명하시오

# @property 방식
# player.hp = 50
# print(player.hp)
# 변수처럼 자연스럽게 사용 가능
# 코드가 간결하고 가독성이 좋음
# 내부에서는 getter/setter가 동작

# get/set 방식
# player.set_hp(50)
# print(player.get_hp())
# 함수 호출 형태라서 코드가 길어짐
# 직관성이 떨어짐

# 핵심 차이
# 구분	@property	get/set
# 사용 방식	변수처럼 사용	함수 호출
# 가독성	좋음	상대적으로 나쁨
# 내부 동작	getter/setter 동일	동일
#
# 👉 결론:
# 기능은 같지만 @property가 더 파이썬스럽고 깔끔하다.
