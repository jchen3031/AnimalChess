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
    else:
        return p1.V>=p2.V
def domain(pos):
    if pos[0] <0 or pos[0]>6 or pos[1]<0 or pos[1]>8:
        return False
    return True
def basicMove(x,y,b,bk,player, step = 0):
    probState = []
    c = 0
    for i in range(x,b.shape[0]):
        jg = ((bk[i][y] == 3 and player) or (bk[i][y] == 2 and not player)) and i !=x
        if bk[i][y] == 1 or jg:
            if abs(x-i)==1 and bk[i][y] != 1:
                probState.append((i,y))
            break
        if b[i][y] == None:
            probState.append((i,y))
            c+=1
            if c>step:
                break
        elif i!=x:
            if b[i][y].player!=player:                    
                probState.append((i,y))
            break
    c = 0
    for i in range(x,-1,-1):
        jg = ((bk[i][y] == 3 and player) or (bk[i][y] == 2 and not player)) and i !=x
        if bk[i][y] == 1 or jg:
            if abs(x-i)==1 and bk[i][y] != 1:
                probState.append((i,y))
            break
        if b[i][y] == None:
            probState.append((i,y))
            c+=1
            if c>step:
                break
        elif i!=x:
            if b[i][y].player!=player:         
                probState.append((i,y))
            break
    c = 0
    for i in range(y,-1,-1):
        jg = ((bk[x][i] == 3 and player) or (bk[x][i] == 2 and not player)) and i !=y
        if bk[x][i] == 1 or jg:
            if abs(y-i)==1 and bk[x][i] != 1:
                probState.append((x,i))
            break
        if b[x][i] == None:
            probState.append((x,i))
            c+=1
            if c>step:
                break
        elif i!=y:
            if b[x][i].player!=player:
                probState.append((x,i))
            break
    c = 0
    for i in range(y,b.shape[1]):
        jg = ((bk[x][i] == 3 and player) or (bk[x][i] == 2 and not player)) and i !=y
        if bk[x][i] == 1 or jg:
            if abs(y-i)==1 and bk[x][i] != 1:
                probState.append((x,i))
            break
        if b[x][i] == None:
            probState.append((x,i))
            c+=1
            if c>step:
                break
        elif i!=y:
            if b[x][i].player!=player:
                probState.append((x,i))
            break
    return probState
# print(len('猴子'))