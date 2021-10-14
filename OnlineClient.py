# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 16:26:22 2021

@author: jchen3031
"""

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
# import socket
import pickle
import Animals
from Net import NetWork
# import time
import gc
"""
Path Note 1.1 Season 1
Client
"""
"""
鲸鱼克猪
猪克猴
猴克马
马克驴
驴克鹅
鹅克鸡
鸡克金鱼
假猴 = 1
金鱼 = 2
鸡 = 3 # 鸡直接秒杀最后一人 C
鹅 = 4 # 飞！# 15回合飞河 C
驴 = 5 # 9空格 C
马 = 6 # 1234512345 C
猴 = 7#分身 选地点， 5回合cd C
猪 = 8#10回合飞任何地方， 下回合直接移动，休息10回合# C
鲸鱼 = 9 #1
"""
Server = 'OIT-C0LLYD3'
d = {1:'猴',2:'金鱼',3:'鸡',4:'鹅',5:'驴',6:'马', 7:'猴',8:'猪',9:'鲸鱼'}
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
input_box2 = Rect(600, 150, 800, 150)
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
m1 = None
m2 = None
CreatFake = False
hp = False
monkey1 = False
monkey2 = False
fly1 = 0
fly2 = 0
auto1 = False
auto2 = False
net = NetWork(server = Server)
GarbageCollection = 0
# s = socket.socket()
# # s.connect(('128.61.16.1', 6666))
# soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# # 绑定本机ip和端口号
# soc.connect(('128.61.17.249', 8089))

# print(soc.recv(40960).decode('utf-8'))
# for data in [b'mich',b'trac']:
#     soc.send(data)
#     print(soc.recv(1024).decode('utf-8'))
# soc.send(b'exit')
# b = Board.Animal()

while True:
    #print(clock.get_fps())
    size = 64#*1.5
    if player:
        #net.send(b'0')
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if str(event.key) == '100': # 按 D 键（键码100）会立即退出
                    print('get key ', str(event.key))
                    running = False
                    print('quit game. Thanks for playing!')
                    exit()
                if str(event.key) == '101': # 按 D 键（键码100）会立即退出
                    print('get key ', str(event.key))
                    animal = net.getData()
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
            if CreatFake:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print('here')
                        x,y = pygame.mouse.get_pos()
                        ls = [32+i*size for i in range(10)]
                        i1 = 0
                        j1 = 0
                        for n in range(len(ls)):
                            if abs(ls[n]-x) < 32:
                                j1 = n
                            if abs(ls[n]-y) < 32:
                                i1 = n
                        if (i1,j1) == m1:
                            animal.put(m1, animal.get(m2))
                            Fmonkey = Animals.FakeMonkey(selectAnimal.player)
                            animal.put(m2, Fmonkey)
                            hp = True
                        elif (i1,j1)==m2:
                            Fmonkey = Animals.FakeMonkey(selectAnimal.player)
                            animal.put(m1, Fmonkey)
                            hp = True
                if event.type == pygame.MOUSEBUTTONUP and hp:
                    #print('yeah')
                    CreatFake = False
                    hp = False
                    selectAnimal.cd = 5
                    player = not player  
                    select = not select
                    util.passOneRound(animal)
                    net.update(animal)
                    print('one round')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1 and not win:
                    move = False
                    x,y = pygame.mouse.get_pos()
                    ls = [32+i*size for i in range(10)]
                    i = 0
                    j = 0
                    for n in range(len(ls)):
                        if abs(ls[n]-x) < 32:
                            j = n
                        if abs(ls[n]-y) < 32:
                            i = n
                    if select:
                        if mark == (i,j) and selectAnimal.V!=9:
                            move = False
                            continue
                        if b.get((i,j)) == 1 and (animal.get(mark).V != 2 and animal.get(mark).V!=9):
                            text = 'you cannot move your stone to here'
                            move = False
                        elif selectAnimal.V == 8 and (selectAnimal.evolution):
                            if selectAnimal.player:
                                auto1 = True
                                fly1 = [mark,(i,j)]
                            else:
                                auto2 = True
                                fly2 = [mark,(i,j)]
                            animal.put(mark, None)
                            move = True
                        else:
                            position =animal.get((i,j))
                            if (i,j) not in possibleWay:
                                #print('you cannot move your stone to here')
                                text = 'you cannot move your stone to here'
                                move = False
                                #select = not select
                                continue
                            # if selectAnimal.V == 8 and selectAnimal.eat>=0:
                            #     print('evolution')
                            #     animal.put((i,j), animal.get(mark))
                            #     animal.put(mark, None)
                            #     mark = (i,j)
                            #     animal.board = util.pigEvolution(mark, animal.board,selectAnimal.player)
                            elif (position !=None):
                                # print('here')
                                if position.player != animal.get(mark).player:
                                    if util.eat(animal.get(mark),position) or b.board[i][j] == 3 or b.board[i][j] == 4 or b.board[i][j] == 5:
                                        if selectAnimal.V == 2 and position.V == 9:
                                            if len(position.filling)!=0:
                                                animal.put((i,j), selectAnimal)
                                                animal.put(mark, None)
                                                whaleFilling = position.filling
                                                possibleLoad = []
                                                for legalPos in [(i+1,j),(i-1,j),(i,j-1),(i,j+1)]: 
                                                    if util.exist(legalPos, animal.board,b.board):
                                                        possibleLoad.append(legalPos)
                                                for idx in range(len(whaleFilling)):
                                                    whaleFilling[idx].round+=2
                                                    animal.put(possibleLoad[idx],whaleFilling[idx])
                                                mark = (i,j)
                                        elif position.V == 1:
                                            monkeyPlayer = position.player
                                            eater = animal.get(mark)
                                            eater.round += 3
                                            animal.put((i,j), eater)
                                            animal.put(mark, None)
                                            mark = (i,j)
                                            if monkeyPlayer:
                                                monkey1 = True
                                            else:
                                                monkey2 = True
                                        else:
                                            animal.put((i,j), animal.get(mark))
                                            animal.put(mark, None)
                                            mark = (i,j)
                                        if animal.get(mark).V == 8:
                                            animal.get(mark).eat+=1
                                        print('eat')
                                    else:
                                        animal.put(mark,None)
                                        print('died')
                                elif selectAnimal.V == 9:
                                    #print("skill",position)
                                    if position.player == selectAnimal.player:
                                        if position.V!=9:
                                            if len(selectAnimal.filling) <=2:
                                                selectAnimal.filling.append(position)
                                                animal.put((i,j), animal.get(mark))
                                                animal.put(mark, None)
                                            else:
                                                move = False
                                                continue
                                            print(selectAnimal.filling)
                                        elif position.V==9:
                                            #print('out')
                                            if len(selectAnimal.filling)!=0:
                                                possibleLoad = []
                                                for legalPos in [(i+1,j),(i-1,j),(i,j-1),(i,j+1)]: 
                                                    if util.exist(legalPos, animal.board,b.board):
                                                        possibleLoad.append(legalPos)
                                                for idx in range(len(selectAnimal.filling)):
                                                    animal.put(possibleLoad[idx],selectAnimal.filling[idx])
                                                selectAnimal.filling = []
                                            else:
                                                move = False
                                                continue
                            else:                   
                                
                                if selectAnimal.V == 7 and selectAnimal.cd==0:
                                     print('create the fake monkey')
                                     print((i,j),mark)
                                     CreatFake = True
                                     m1 = (i,j)
                                     m2 = mark
                                else:
                                    animal.put((i,j), animal.get(mark))
                                    animal.put(mark, None)
                                    mark = (i,j)
                            move = True
                        if selectAnimal.V == 6:
                            selectAnimal.step= (selectAnimal.step+1)%5
                        elif selectAnimal.V == 8:
                            if selectAnimal.evolution == None:
                                print('pig')
                                selectAnimal.evolution = True
                                selectAnimal.sleep = 5
                                if selectAnimal.player:     
                                    p1pig = selectAnimal
                                else:
                                    p2pig = selectAnimal
                            elif selectAnimal.evolution:
                                selectAnimal.sleep = 1
                                selectAnimal.evolution = False
                                print(selectAnimal.evolution)
                                if selectAnimal.player:     
                                    p1pig = selectAnimal
                                else:
                                    p2pig = selectAnimal
                            elif not selectAnimal.evolution:
                                selectAnimal.sleep = 5
                                print('not evolution')
                                selectAnimal.evolution = True
                                if selectAnimal.player:
                                    p1pig = selectAnimal
                                else:
                                    p2pig = selectAnimal
                            # msg = pickle.dumps(animal)
                            # soc.send(msg)
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
                        elif animal.get(mark).round != 0:
                            print('your animal is sleeping', animal.get(mark).round)
                            move = False
                            select = not select
                        else:
                            #animal.get(mark).select = True
                            selectAnimal = animal.get(mark)
                            selectAnimal.setPos(mark)
                            selectAnimal.setBoard(animal.board)
                            if selectAnimal.V == 8:
                                if selectAnimal.sleep != 0:
                                    print('your pig is sleeping', selectAnimal.sleep)
                                    text = 'your pig is sleeping! Wake up pig!'
                                    move = False
                                    select = not select
                                    possibleWay = None
                                    continue
                            if selectAnimal.V == 1:
                                print('it is fake monkey')
                            possibleWay = selectAnimal.possibleWay()
                            for i in [0,4,8]:
                                home = (3,i)
                                if animal.get(home) !=None:
                                    if (home in possibleWay):                                   
                                        possibleWay.remove(home)
                            text ='%s %s'%(selectAnimal.name(), str(possibleWay))
                            print(text)
                            print(selectAnimal.round)
            elif event.type == pygame.MOUSEBUTTONUP and not hp:
                if select and move:        
                    player = not player
                    util.passOneRound(animal)
                    player1Goose = util.find(animal,4,True)
                    player2Goose = util.find(animal,4,False)
                    if player1Goose!=None and player1Goose.evolution!=0:
                        player1Goose.evolution-=1
                    if player2Goose!=None and player2Goose.evolution!=0:
                        player2Goose.evolution-=1
                    print('one round')
                    player1Monkey = util.find(animal,7,True)
                    player2Monkey = util.find(animal,7,False)
                    if player1Monkey!= None and util.find(animal,1,True)==None and player1Monkey.cd!=0:
                            player1Monkey.cd-=1                             
                    if player2Monkey!= None and util.find(animal,1,False)==None and player2Monkey.cd!=0:
                            player2Monkey.cd-=1
                    if player and auto1:
                        newP = animal.get(fly1[1])
                        if p1pig.eat>3:
                                print('complete evolution')
                                animal.put(fly1[1],p1pig)
                                animal.board = util.pigEvolution(fly1[1], animal.board,p1pig.player)
                        elif newP == None:
                            animal.put(fly1[1],p1pig)
                        elif newP.V!=9:
                            p1pig.eat+=1
                            animal.put(fly1[1],p1pig)
                        else:
                            animal.put(fly1[0],p1pig)
                        player = not player
                        auto1 = False
                    if not player and auto2:
                        newP = animal.get(fly2[1])
                        #print(p2pig)
                        if p2pig.eat>3:
                            print('evolution')
                            animal.put(fly1[1],p2pig)
                            animal.board = util.pigEvolution(fly2[1], animal.board,p2pig.player)
                        elif newP == None:
                            animal.put(fly2[1],p2pig)
                        elif newP.V!=9:
                            p2pig.eat+=1
                            animal.put(fly2[1],p2pig)
                        else:
                            animal.put(fly2[0],p2pig)
                        player = not player
                        auto2 = False
                #n = Learning3.NetWork()
                # data = net.update(animal)
                net.update(animal)
                #n.close()
                #net.send(b'Hello')
                #print(data)
                #print(net.get())
                select = not select
    else:
        getdata = net.client.recv(40960)
        text = 'Waitting'
        if getdata != 0:
            loads = pickle.loads(getdata)
            if not animal.equal(loads):
                animal = loads
                player = not player
                text = 'Your turn'
    #print(getdata)
    #player = True
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
    p.drawBack(screen,'gold',(size/2+8*size,size/2+3*size),size/2-4,'家')
    p.drawBack(screen,'gold',(size/2+0*size,size/2+3*size),size/2-4,'家')
    p.drawBack(screen,'gold',(size/2+4*size,size/2+3*size),size/2-4,'家')
    for i in range(b.x):
        for j in range(b.y):
            if animal.board[i][j] != None:
                p.draw(screen,(255,255,255),(size/2+j*size,size/2+i*size),size/2-4,d[animal.board[i][j].V],animal.board[i][j].player)
    txt_surface = f.render(text, True, 'black')
    width = max(800, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, 'black', input_box, 2)
    
    # txt_surface2 = f.render('skill', True, 'black')
    # width = max(200, txt_surface2.get_width()+10)
    # input_box2.w = width
    # screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
    # pygame.draw.rect(screen, 'black', input_box2, 2)
    
    if select:
        if possibleWay !=None:
            p.drawPossibleWay(screen,possibleWay)
    Stoneplayer1 = util.countBoard(animal,True)
    Stoneplayer2 = util.countBoard(animal,False)
    # print(Stoneplayer1,Stoneplayer2)
    if Stoneplayer1 == 0:
        text = 'Player 0 win the game'
        win = True
        possibleWay = None
    elif Stoneplayer2 == 0:
        text = 'Player 1 win the game'
        win = True
        possibleWay = None
    elif Stoneplayer1 == 1 and Stoneplayer2 == 1:
        p1chick = util.find(animal,3,True)
        p2chick = util.find(animal,3,False)
        if p1chick!=None and p2chick!=None:
            win = True
            text = 'Tie'
            possibleWay = None
        elif p1chick!=None:
            text = 'Player 1 win the game'
            win = True
            possibleWay = None
        elif p2chick!=None:
            text = 'Player 2 win the game'
            win = True
            possibleWay = None
        #pause = True
    #print(select)
    GarbageCollection+=1
    if GarbageCollection == 20:
        GarbageCollection = 0
        gc.collect()
    if not pause:
        pygame.display.update()
# soc.close()
if __name__ == '__main__':
    pass
