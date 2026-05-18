import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("클래스 생성 예제")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 20)

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BLUE = (80, 80, 255)
RED = (230, 90, 90)
GREEN = (80, 255, 80)

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.size = 50
        self.speed = 4
        self.color = BLUE

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.size > WIDTH:
            self.x = WIDTH - self.size
        if self.y + self.size > HEIGHT:
            self.y = HEIGHT - self.size

    def draw(self, surface):
        #파란색 사각형 그리기
        pygame.draw.rect(surface, self.color,
                         (int(self.x), int(self.y), self.size, self.size))
        #Player라는 텍스트를 이미지로 만드기
        text = font.render("Player", True, BLACK)
        #surface에 text 이미지를 붙여넣기
        surface.blit(text, (int(self.x), int(self.y) - 28))

class Enemy:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.size = 50
        self.speed = 2
        self.color = RED

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.size > WIDTH:
            self.x = WIDTH - self.size
        if self.y + self.size > HEIGHT:
            self.y = HEIGHT - self.size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (int(self.x), int(self.y), self.size, self.size))

        text = font.render("Enemy", True, BLACK)
        surface.blit(text, (int(self.x), int(self.y) - 28))

class NPC:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.size = 50
        self.speed = 2
        self.color = GREEN

        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.size > WIDTH:
            self.x = WIDTH - self.size
        if self.y + self.size > HEIGHT:
            self.y = HEIGHT - self.size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
        text = font.render("NPC", True, BLACK)
        surface.blit(text, (int(self.x), int(self.y) - 28))


    #Add code here
    #method 추가해보자
    # 1. 초록색 사각형 그리기
    # 2. NPC 텍스트를 이미지로 만들기
    # 3. 사각형 위에 텍스트 보이기(이미지를 surface에 붙여넣기)

#player, enemy, npc를 관리하는 클래스
class Game:
    def __init__(self):
        self.player = Player(100, 250)
        self.enemy = Enemy(700, 100)
        self.npc = NPC(500, 400)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def update(self):
        # 방향키로 Player 이동
        keys = pygame.key.get_pressed()
        p_dx, p_dy = 0, 0

        if keys[pygame.K_LEFT]:
            p_dx = -1
        if keys[pygame.K_RIGHT]:
            p_dx = 1
        if keys[pygame.K_UP]:
            p_dy = -1
        if keys[pygame.K_DOWN]:
            p_dy = 1
        # 객체간 메시지 교환(메서드 호출)으로 상호작용.
        self.player.move(p_dx, p_dy)

        # Enemy는 Player를 따라가게~
        e_dx, e_dy = 0, 0
        if self.enemy.x < self.player.x:
            e_dx = 1
        elif self.enemy.x > self.player.x:
            e_dx = -1
        if self.enemy.y < self.player.y:
            e_dy = 1
        elif self.enemy.y > self.player.y:
            e_dy = -1
        # 객체간 메시지 교환(메서드 호출)으로 상호작용.
        self.enemy.move(e_dx, e_dy)

        # NPC는 랜덤 이동
        if random.random() < 0.02:
            self.npc.dx = random.choice([-1, 0, 1])
            self.npc.dy = random.choice([-1, 0, 1])
        # 객체간 메시지 교환(메서드 호출)으로 상호작용.
        self.npc.move(self.npc.dx, self.npc.dy)

    def draw(self, surface):
        surface.fill(WHITE)
        self.player.draw(surface)
        self.enemy.draw(surface)
        self.npc.draw(surface)
        #Add code here
        #NPC 클래스에 추가한 Method 호출

        info1 = font.render("Player: 방향키로 이동", True, BLACK)
        info2 = font.render("Enemy: 플레이어 추적 / NPC: 랜덤 이동", True, BLACK)

        surface.blit(info1, (20, 20))
        surface.blit(info2, (20, 55))

# 관리하는 객체 생성
game = Game()
while True:
    for event in pygame.event.get():
        game.handle_event(event)
    #관리하는 객체에게 메모리에 상태를 업데이트하고 화면에 그리도록 요청
    game.update()
    game.draw(screen)

    pygame.display.flip()
    clock.tick(60)