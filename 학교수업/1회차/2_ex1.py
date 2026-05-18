# 1. 단순 공 움직이기
# 2. 반복문을 통한 2개의 공 움직이기 -> 서로 부딛치면 반사
#2_ex1.py
import pygame, sys

pygame.init()
W, H = 640, 360
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.display.set_caption("Moving Circle") #화면제목설정

# 전역 상태(절차지향의 전형)
x1, y1 = 120.0, 120.0
x2, y2 = 100.0, 100.0
vx1, vy1 = 4.0, 2.5
vx2, vy2 = -3.0, -2.5
r = 30  #18
color = (220, 50, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 업데이트(계산)
    x1 += vx1
    y1 += vy1
    x2 += vx2
    y2 += vy2

    # 충돌(벽)
    if x1 - r <= 0 or x1 + r >= W:
        vx1 *= -1
    if y1 - r <= 0 or y1 + r >= H:
        vy1 *= -1
    if x2 - r <= 0 or x2 + r >= W:
        vx2 *= -1
    if y2 - r <= 0 or y2 + r >= H:
        vy2 *= -1
    if (x1-x2)**2+(y1-y2)**2 <= r**2:
        vx1 *= -1
        vy1 *= -1
        vx2 *= -1
        vy2 *= -1
    # 그리기(출력)
    screen.fill((245, 245, 245))
    pygame.draw.circle(screen, color, (int(x1), int(y1)), r)
    pygame.draw.circle(screen, color, (int(x2), int(y2)), r)
    pygame.display.flip()
    clock.tick(60)