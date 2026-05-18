import pygame, sys, random
# -----------------------------
# 1. pygame 초기화
# -----------------------------
pygame.init()
W, H = 640, 360
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("OOP")
# FPS(프레임 속도) 제어용 Clock 객체
clock = pygame.time.Clock()

# -----------------------------
# 무작위 색상 생성 함수
# -----------------------------
def rand_color():
    #RGB 값을 40~230 사이에서 랜덤 생성
    return (random.randint(40, 230), random.randint(40, 230), random.randint(40, 230))

def rand_q():
    return random.randint(-5,5)


class Ball:
    # 객체 생성 시 실행되는 생성자
    def __init__(self, x, y, r=16):
        #공의 위치
        self.x = float(x)
        self.y = float(y)
        #공의 반지름
        self.r = int(r)
        #공의 전하량
        self.q = rand_q()
        #공의 색
        self.color = rand_color()
        #x 방향 속도
        self.vx = random.choice([-1, 1]) * random.uniform(2.0, 5.0)
        #y방향 속도
        self.vy = random.choice([-1, 1]) * random.uniform(2.0, 5.0)

    def update(self, w, h):
        omega = self.q * 1/5 / (self.r) # a = qvB/m # 대충 m r과 같다 가정. B는 1/5로 가정
        self.vx += omega * self.vy * 1 - self.q* 1/50 # 전기장은 1/50로 가정
        self.vy += -omega * self.vx * 1
        self.x += self.vx * 1
        self.y += self.vy * 1

        #좌우 벽 충돌 검사
        if self.x - self.r <= 0 or self.x + self.r >= w:
            self.vx *= -1
        #상하 벽 충돌 검사
        if self.y - self.r <= 0 or self.y + self.r >= h:
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.r)

class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.t = 0
        # 공 객체 리스트
        self.balls = [
            Ball(120, 120, 18),
            Ball(260, 160, 14),
            Ball(420, 220, 22),
        ]

# -----------------------------
# 이벤트 처리
# -----------------------------
    def handle_event(self, event):
        # 메시지 기반 상호작용: "공 추가"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos #클릭 위치 얻기
            self.balls.append(Ball(mx, my, random.randint(12, 24))) # 해당 위치에 새로운 공 생성

# -----------------------------
# 게임 상태 업데이트
# -----------------------------
    def update(self):
        # Game은 '세계'로서 업데이트 흐름만 관리
        for b in self.balls:
            b.update(self.w, self.h)

# -----------------------------
# 화면 그리기
# -----------------------------
    def draw(self, surface):
        surface.fill((245, 245, 245))
        for b in self.balls:
            b.draw(surface)

        font = pygame.font.SysFont(None, 22)
        text = font.render(f"Balls: {len(self.balls)}  |  Left click: add ball", True, (30, 30, 30))
        surface.blit(text, (10, 10))

game = Game(W, H)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Game 객체에 이벤트 전달
        game.handle_event(event)

    ##### Add code Here!.
    game.update()
    game.draw(screen)

    pygame.display.flip()
    clock.tick(60) # FPS 제한 (60프레임)



# 3. while문 안에서 직접 공을 움직이지 않고 game.update()를 호출하는 이유는 무엇인지 작성하시오.

# while문에서 공의 위치를 직접 변경하지 않고 game.update()를 호출하는 이유는 역할(책임)을 분리하고 코드 구조를 명확하게 유지하기 위해서이다.
# Game 객체는 전체 게임의 흐름을 관리하는 역할을 가지고 있고, 각 Ball 객체는 자신의 상태(위치, 속도 등)를 스스로 업데이트하는 책임을 가진다.
# 따라서 while문에서 직접 공을 움직이면 코드가 분산되고 유지보수가 어려워지며 객체지향의 캡슐화 원칙이 깨진다.
# game.update()를 통해 모든 객체의 업데이트를 한 곳에서 관리하면 구조가 깔끔해지고, 확장성과 재사용성이 높아진다.

# 4. 1주차 수업의 실습 2는 "상태+행동"을 묶기 위해 Ball 클래스를 추가하였고, 실습 3은  "책임 분산" 을  통해 "메시지"를 주고받는 협력 시스템을 만들었다.
# Ball 과 Game의 책임이 무엇인지 서술해 보자.(5줄이상)

# Ball 클래스의 책임은 하나의 공 객체에 대한 상태와 행동을 관리하는 것이다.
# 즉, 공의 위치(x, y), 속도(vx, vy), 반지름, 색상, 전하량 같은 상태를 가지고 있으며, update()를 통해 자신의 움직임을 계산하고, draw()를 통해 화면에 자신을 그리는 행동을 수행한다.
# 즉, Ball은 “자기 자신을 어떻게 움직이고 표현할지”를 책임진다.

# 반면 Game 클래스는 전체 게임 세계를 관리하는 역할을 한다. 여러 개의 Ball 객체를 리스트로 관리하며, 이벤트 처리(handle_event)를 통해 새로운 공을 생성하거나 사용자 입력을 처리한다.
# 또한 update()에서 모든 공의 업데이트를 호출하고, draw()에서 전체 화면을 구성하는 등 전체 흐름을 제어하는 책임을 가진다.

# 즉, Ball은 “개별 객체의 행동”, Game은 “전체 시스템의 조율”을 담당하며 서로 메시지를 주고받으며 협력하는 구조를 만든다.