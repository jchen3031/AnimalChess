# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 02:42:11 2021

@author: jchen3031
"""
import pygame
class Painting:
    def drawBack(self,screen,color,pos,size, word = '陷阱'):
        pygame.draw.circle(screen,color,pos,size)
        text = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',int(size))
        wordC = 'black'
        x,y = pos
        if len(word) == 2:
            x -= 31*size/32
        else:
            x -= size/2
        y -= size/2
        t = text.render(word, 1, wordC)
        screen.blit(t, (x,y))
    def draw(self,screen,color,pos,size, animal,wordColor = True):
        pygame.draw.circle(screen,color,pos,size)
        text = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',int(size))
        wordC = 'red' if wordColor else 'black'
        t = text.render(animal, 1, wordC)
        x,y = pos
        if len(animal) == 2:
            x -= 31*size/32
        else:
            x -= size/2
        y -= size/2
        screen.blit(t, (x,y))
    def drawPossibleWay(self,screen, ls):
        size = 64
        for i,j in ls:
            pygame.draw.circle(screen,'black',(32+j*size,32+i*size),size/16)
        return 0
def eat(p1,p2):
    print(p1,p2)
    if p1.V == 2 and p2.V == 9:
        return True
    if p1.V == 9 and p2.V == 2:
        return False
    # if p2.V == 1:
    #     p1.round+=2
    #     print('fake monkey')
    #     return True
    else:
        return p1.V>p2.V
def domain(pos):
    if pos[0] <0 or pos[0]>6 or pos[1]<0 or pos[1]>8:
        return False
    return True
def basicMove(x,y,b,bk,player,v=1, step = 0, unlegal = 1):
    probState = []
    c = 0
    for i in range(x,b.shape[0]):
        jg = ((bk[i][y] == 3 and player) or (bk[i][y] == 2 and not player)) and i !=x
        if bk[i][y] == unlegal or jg:
            if abs(x-i)==1 and bk[i][y] != unlegal:
                probState.append((i,y))
            break
        if b[i][y] == None:
            probState.append((i,y))
            c+=1
            if c>step:
                break
        elif i!=x:
            if b[i][y].player!=player and b[i][y].V<v or (v==2 and b[i][y].V==9):
                probState.append((i,y))
            break
    c = 0
    for i in range(x,-1,-1):
        jg = ((bk[i][y] == 3 and player) or (bk[i][y] == 2 and not player)) and i !=x
        if bk[i][y] == unlegal or jg:
            if abs(x-i)==1 and bk[i][y] != unlegal:
                probState.append((i,y))
            break
        if b[i][y] == None:
            probState.append((i,y))
            c+=1
            if c>step:
                break
        elif i!=x:
            if b[i][y].player!=player and b[i][y].V<v or (v==2 and b[i][y].V==9):         
                probState.append((i,y))
            break
    c = 0
    for i in range(y,-1,-1):
        jg = ((bk[x][i] == 3 and player) or (bk[x][i] == 2 and not player)) and i !=y
        if bk[x][i] == unlegal or jg:
            if abs(y-i)==1 and bk[x][i] != unlegal:
                probState.append((x,i))
            break
        if b[x][i] == None:
            probState.append((x,i))
            c+=1
            if c>step:
                break
        elif i!=y:
            if b[x][i].player!=player and b[x][i].V<v or (v==2 and b[x][i].V==9):
                probState.append((x,i))
            break
    c = 0
    for i in range(y,b.shape[1]):
        jg = ((bk[x][i] == 3 and player) or (bk[x][i] == 2 and not player)) and i !=y
        if bk[x][i] == unlegal or jg:
            if abs(y-i)==1 and bk[x][i] != unlegal:
                probState.append((x,i))
            break
        if b[x][i] == None:
            probState.append((x,i))
            c+=1
            if c>step:
                break
        elif i!=y:
            if b[x][i].player!=player and (b[x][i].V<v or (v==2 and b[x,i].V==9)):
                probState.append((x,i))
            break
    return probState
def passOneRound(b):
    # x,y = b.shape
    # for i in range(x):
    #     for j in range(y):
    for i in b:
            if i !=None:
                if i.round > 0:
                    i.round -= 1
                if i.sleep>0:
                    i.sleep-=1
    return b
def countBoard(b, player = None):
    # x,y = b.shape
    count = 0
    # for i in range(x):
    #     for j in range(y):
    for i in b:
            if i !=None:
                if player == None:
                    count += 1
                elif i.player == player:
                    count += 1
    return count
def find(b, v, player):
    for i in b:
            if i !=None:
                if i.player == player and i.V == v:
                    return i
    else:
        return None
def exist(pos,b,bk = None,river = True):
    x,y = pos
    if x<0 or x>=b.shape[0] or y<0 or y >=b.shape[1]:
        return False
    if river:
        return bk[x,y] != 1
    return True
def pigEvolution(pos,b,player):
    x,y = pos
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if exist((i,j),b,None,False):
                if b[i,j]!=None and b[i,j].player!=player:
                    b[i,j] = None
    return b
