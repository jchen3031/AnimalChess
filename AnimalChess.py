# background_image_filename = 'C:\\Users\\cjy\\Desktop\\backgound.jpg'
# mouse_image_filename = 'C:\\Users\\cjy\\Desktop\\mouse.png'
# animal9_filename = 'C:\\Users\\cjy\\Desktop\\animal9.png'
# -*- coding: UTF-8 -*-
# coding=utf-8

#import os
import pygame
#import numpy as np
#from pygame.locals import *
from sys import exit
from pygame.locals import KEYDOWN
from pygame.locals import QUIT
from pygame.locals import Rect
import Board
import util
"""
鲸鱼克猪
猪克猴
猴克马
马克驴
驴克鹅
鹅克鸡
鸡克金鱼
金鱼 = 2
鸡 = 3
鹅 = 4
驴 = 5
马 = 6
猴 = 7
猪 = 8
鲸鱼 = 9
"""
d = {2:'金鱼',3:'鸡',4:'鹅',5:'驴',6:'马', 7:'猴',8:'猪',9:'鲸鱼'}
p = util.Painting()
screen = pygame.display.set_mode((960, 640), 0, 64)
pygame.init()
pygame.display.list_modes()
pygame.display.set_caption("AnimalChess")
clock = pygame.time.Clock()
f = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',int(40))
b = Board.Board()
text = 'Hello'
input_box = Rect(50, 450, 800, 150)
animal= Board.Animal()
player = True
select = False
move = False
mark = (0,0)
selectAnimal = None
possibleWay = None
p1pig = None
p2pig = None
pause = False
win = False
while True:

    #print(clock.get_fps())
    size = 64#*1.5
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if str(event.key) == '100': # 按 D 键（键码100）会立即退出
                print('get key ', str(event.key))
                running = False
                print('quit game. Thanks for playing!')
                exit()
            if str(event.key) == '119': # 按 w 键（键码119）
                print('get key ', str(event.key)) 
                #print('reset the game!!!')
                text = 'reset the game!!!'
                animal.reset()
                player = True
                select = False
                move = False
                mark = (0,0)
                selectAnimal = None
                possibleWay = None
                p1pig = None
                p2pig = None
                pause = False
                win = False
                print(animal.board)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not win:
                move = False
                x,y = pygame.mouse.get_pos()
                ls = [32+i*size for i in range(10)]
                i = 0
                j = 0
                # print(x,y)
                for n in range(len(ls)):
                    if abs(ls[n]-x) < 32:
                        j = n
                    if abs(ls[n]-y) < 32:
                        i = n
                if select:
                    if mark == (i,j):
                        move = False
                        continue
                    if b.get((i,j)) == 1 and (animal.get(mark).V != 2 and animal.get(mark).V!=9):
                        #print('not a good move')
                        text = 'you cannot move your stone to here'
                        move = False
                    # elif b.get((i,j)) == 0 and animal.get(mark).V == 2:
                    #     print('not a good move')
                    #     move = False
                    else:
                        position =animal.get((i,j))
                        if ((i,j) not in selectAnimal.possibleWay()):
                            #print('you cannot move your stone to here')
                            text = 'you cannot move your stone to here'
                            move = False
                            #select = not select
                            continue
                        if (position !=None):
                            # print('here')
                            if position.player != animal.get(mark).player:
                                if util.eat(animal.get(mark),position):
                                    animal.put((i,j), animal.get(mark))
                                    animal.put(mark, None)
                                    mark = (i,j)
                                    print('eat')
                                else:
                                    animal.put(mark,None)
                                    print('died')
                        else:
                            animal.put((i,j), animal.get(mark))
                            animal.put(mark, None)
                            mark = (i,j)
                        move = True
                        if selectAnimal.V == 8:
                            if selectAnimal.player:
                                p1pig = selectAnimal
                            else:
                                p2pig = selectAnimal
                            selectAnimal.sleep = True
                        else:
                            if player:
                                if p1pig!=None:
                                    p1pig.sleep = False
                            else:
                                if p2pig!=None:    
                                    p2pig.sleep = False
                        #print(animal.board)
                else:
                    mark = (i,j)
                    if animal.get(mark) == None:
                        #print('no stone')
                        text = 'no stone'
                        move = False
                        select = not select
                        continue
                    if animal.get(mark).player != player:
                        #print('not your stone')
                        text = 'not your stone'
                        move = False
                        select = not select
                    else:
                        #animal.get(mark).select = True
                        selectAnimal = animal.get(mark)
                        selectAnimal.setPos(mark)
                        selectAnimal.setBoard(animal.board)
                        if selectAnimal.V == 8:
                            if selectAnimal.sleep:
                                print('your pig is sleeping')
                                text = 'your pig is sleeping! Wake up pig!'
                                move = False
                                select = not select
                                possibleWay = None
                                continue
                        possibleWay = selectAnimal.possibleWay()
                        if selectAnimal.V == 6:
                            if selectAnimal.step == 0:
                                selectAnimal.step =1
                            else:
                                selectAnimal.step=2*selectAnimal.step+1
                        text ='%s %s'%(selectAnimal.name(), str(possibleWay))
                        print(text)
        if event.type == pygame.MOUSEBUTTONUP:
            if select and move:        
                player = not player  
            select = not select
    screen.fill((255,255,255))
    for i in range(b.x):
        for j in range(b.y):
            a = '#008000'
            rp = (j*size,i*size)
            rs = (size, size)
            if b.board[i][j] == 1:
                a = '#0000FF'
            else:
                a = '#008000'
            pygame.draw.rect(screen, a, Rect(rp,rs))
    for i in range (1,b.y+1):
        pygame.draw.line(screen, (0, 0, 0), (i*size, 0), (i*size, 7*size))
    for j in range (1,b.x+1):
        pygame.draw.line(screen, (0, 0, 0), (0, j*size), (9*size, j*size))
    p.drawBack(screen,'brown',(size/2,size/2+4*size),size/2-4)
    p.drawBack(screen,'brown',(size/2,size/2+2*size),size/2-4)
    p.drawBack(screen,'brown',(size/2+1*size,size/2+3*size),size/2-4)
    p.drawBack(screen,'brown',(size/2+8*size,size/2+4*size),size/2-4)
    p.drawBack(screen,'brown',(size/2+8*size,size/2+2*size),size/2-4)
    p.drawBack(screen,'brown',(size/2+7*size,size/2+3*size),size/2-4)
    p.drawBack(screen,'green',(size/2+8*size,size/2+3*size),size/2-4,'家')
    p.drawBack(screen,'green',(size/2+0*size,size/2+3*size),size/2-4,'家')
    for i in range(b.x):
        for j in range(b.y):
            if animal.board[i][j] != None:
                #pygame.draw.circle(screen,(255,255,255),(32+i*size,32+j*size),size/2-4)
                p.draw(screen,(255,255,255),(size/2+j*size,size/2+i*size),size/2-4,d[animal.board[i][j].V],animal.board[i][j].player)
    txt_surface = f.render(text, True, 'black')
    width = max(800, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, 'black', input_box, 2)
    if select:
        if possibleWay !=None:
            p.drawPossibleWay(screen,possibleWay)
    if animal.board[3][0] !=None:
        if not animal.board[3][0].player:
            text = 'Player 2 win the game'
            win = True
            possibleWay = None
    if animal.board[3][8] !=None:
        if animal.board[3][8].player:
            text = 'Player 1 win the game'
            win = True
            possibleWay = None
        #pause = True
    #print(select)
    if not pause:
        pygame.display.update()
if __name__ == '__main__':
    pass