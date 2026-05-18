# 1_pygame.py
import pygame
import sys
#1. 초기화
pygame.init()
#2. 화면설정
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))#800x600크기의 윈도우생성
pygame.display.set_caption("Circle") #화면제목설정
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#3.메인 루프
running = True
while running:
    for event in pygame.event.get(): #이벤트처리
        if event.type == pygame.QUIT:
            running = False
    #화면그리기
    screen.fill(WHITE) #이전화면지우기(배경흰색) #전체 칠하기 #이것도 메모리
    pygame.draw.circle(screen, BLUE, (400, 300), 50) #원그림(메모리)
    pygame.display.flip() #메모리에 있는 걸 실제로 화면에 그림
#4.종료
pygame.quit()
sys.exit()

