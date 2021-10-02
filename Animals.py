# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 06:07:50 2021

@author: jchen3031
"""
import numpy as np
import copy
import util
class animal(object):
    def __init__(self, player):
        self.player = player
        self.V = 0
        self.select = False
        b = np.zeros((7,9))
        for i in range(3,6):
            for j in range(0,6):
                if (j!= 0 and j!=3 and j!=6):
                    b[j][i] = 1
        b[3][0] = 4
        b[3][8] = 5
        b[3][1] = 2
        b[4][0] = 2
        b[2][0] = 2
        b[3][7] = 3
        b[4][8] = 3
        b[2][8] = 3
        self.background = b
    def __str__(self):
        return str(self.V) +' ' +str(self.player)
    def __repr__(self):
        return str(self.V) +' ' +str(self.player)
    def clone(self):
        return copy.deepcopy(self)
    def setPos(self, pos):
        self.x,self.y = pos
    def setBoard(self,board):
        self.b = board
    def possibleWay(self):
        return None
    def name(self):
        return type(self).__name__
class GoldFish(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 2
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,0)
        for i in range(bk.shape[0]):
            for j in range(bk.shape[1]):
                if bk[i][j]==1 and (i != x or y!=j):
                    probState.append((i,j))
        return probState
class Chick(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 3
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,0)
        return probState
class Goose(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 4
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,0)
        return probState
class Donkey(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 5
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,0)
        for x,y in probState.copy():
            probState2 = util.basicMove(x,y,b,bk,self.player,1)
            probState+=probState2
        return probState
class Horse(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 6
        self.step = 0
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,self.step)
        return probState
class Monkey(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 7
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,9)
        for x,y in probState.copy():
            probState2 = util.basicMove(x,y,b,bk,self.player,0)
            probState+=probState2
        return probState
class Pig(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 8
        self.sleep = False
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = []
        probState = util.basicMove(x,y,b,bk,self.player,9)
        return probState
class Whale(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 9
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        player = self.player
        step = 3
        probState = []
        jg1 = False
        c = 0
        for i in range(x,b.shape[0]):
            jg = ((bk[i][y] == 3 and player) or (bk[i][y] == 2 and not player)) and i !=x
            if bk[i][y] == 1 or jg:
                if abs(x-i)==1 and bk[i][y] != 1:
                    probState.append((i,y))
                if bk[i][y] == 1:
                    jg1 = True
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
                if bk[i][y] == 1:
                    jg1 = True
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
                if bk[x][i] == 1:
                    jg1 = True
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
                if bk[x][i] == 1:
                    jg1 = True
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
        if jg1:
            #print('here')
            for i in range(x,b.shape[0]):
                if bk[i][y] == 0 and i!=x:
                    if b[i][y] == None:
                        probState.append((i,y))
                    elif b[i][y].player!=self.player:
                        probState.append((i,y))
                    break
                if bk[i][y] == 1 and b[i][y] == None:
                    probState.append((i,y))
                elif i!=x:
                    if b[i][y].player!=self.player:
                        probState.append((i,y))
                    break
            for i in range(x,-1,-1):
                if bk[i][y] == 0 and i!=x:
                    if b[i][y] == None:
                        probState.append((i,y))
                    elif b[i][y].player!=self.player:
                        probState.append((i,y))
                    break
                if bk[i][y] == 1 and b[i][y] == None:
                    probState.append((i,y))
                elif i!=x:
                    if b[i][y].player!=self.player:
                        probState.append((i,y))
                    break
            for i in range(y,-1,-1):
                if bk[x][i] == 0 and i!=y:
                    if b[x][i] == None:
                        probState.append((x,i))
                    elif b[x][i].player!=self.player:
                        probState.append((x,i))
                    break
                if bk[x][i] == 1 and b[x][i] == None:
                    probState.append((x,i))
                elif i!=y:
                    if b[x][i].player!=self.player:
                        probState.append((x,i))
                    break
            for i in range(y,b.shape[1]):
                if bk[x][i] == 0 and i!=y:
                    if b[x][i] == None:
                        probState.append((x,i))
                    elif b[x][i].player!=self.player:
                        probState.append((x,i))
                    break
                if bk[x][i] == 1 and b[x][i] == None:
                    probState.append((x,i))
                elif i!=y:
                    if b[x][i].player!=self.player:
                        probState.append((x,i))
                    break
        return probState
# horse = Horse(True)
# print(horse)
# #a = [[0]*3]*3
# a = np.ndarray((3,3), dtype = object)
# print(a)
# a[0][0] = horse
# print(a)