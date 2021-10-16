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
        self.round = 0
        self.sleep = 0
        b = np.zeros((7,9))
        for i in range(3,6):
            for j in range(0,6):
                if (j!= 0 and j!=3 and j!=6):
                    b[j][i] = 1
        b[3][0] = 4
        b[3][8] = 4
        b[3][4] = 4
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
        probState = util.basicMove(x,y,b,bk,self.player,self.V,0,2)
        for i in range(bk.shape[0]):
            for j in range(bk.shape[1]):
                if bk[i][j]== 1 and (i != x or y!=j):
                    if b[i,j] !=None and b[i,j].V == 2:
                        continue
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
        probState = util.basicMove(x,y,b,bk,self.player,self.V,0)
        return probState
class Goose(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 4
        self.evolution = 10
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = []
        if self.evolution==0:
            #print('here')
            for i in range(x,b.shape[0]):
                if bk[i][y] == 1 or i == x:
                    continue
                if b[i][y] == None:
                    probState.append((i,y))
                elif b[i][y].player!=self.player and b[i][y].V<self.V:
                    probState.append((i,y))
                break
            for i in range(x,-1,-1):
                if bk[i][y] == 1 or i == x:
                    continue
                if b[i][y] == None:
                    probState.append((i,y))
                elif b[i][y].player!=self.player and b[i][y].V<self.V:
                    probState.append((i,y))
                break
            for i in range(y,-1,-1):
                if bk[x][i] == 1 or i==y:
                    continue
                if b[x][i] == None:
                    probState.append((x,i))
                elif b[x][i].player!=self.player and b[x,i].V<self.V:
                    probState.append((x,i))
                break
            for i in range(y,b.shape[1]):
                if bk[x][i] == 1 or i==y:
                    continue
                if b[x][i] == None:
                    probState.append((x,i))
                elif b[x][i].player!=self.player and b[x,i].V<self.V:
                    probState.append((x,i))
                break
        else:
            probState = util.basicMove(x,y,b,bk,self.player,self.V,0)
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
        probState = util.basicMove(x,y,b,bk,self.player,self.V)
        ls = [(x+1,y+1),(x+1,y-1),(x-1,y-1),(x-1,y+1)]
        for x,y in ls:
            if util.exist((x,y),b,bk):
                if b[x,y] == None or (b[x,y].V<self.V and b[x,y].player!=self.player):
                    probState.append((x,y))
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
        probState = util.basicMove(x,y,b,bk,self.player,self.V,self.step)
        return probState
class FakeMonkey(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 1
        #self.cd = 0
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,1)          
        return probState
class Monkey(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 7
        self.cd = 0
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,self.V)          
        return probState
class Pig(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 8
        self.sleep = 0
        self.evolution = None
        self.eat = 0
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = []
        if self.eat >= 3:
            print('complete evolution. Game Over!')
            for x in range(b.shape[0]):
                for y in range(b.shape[1]):
                    if (b[x,y]!=None and (b[x,y].player == self.player or  b[x,y].V >= self.V))\
                        or bk[x,y] == 1 or bk[x,y] == 4:
                        continue
                    probState.append((x,y))
        elif self.evolution == None:
            probState = util.basicMove(x,y,b,bk,self.player,self.V,0)
        elif self.evolution:
            #over power
            print('evolution')
            for x in range(b.shape[0]):
                for y in range(b.shape[1]):
                    if (b[x,y]!=None and (b[x,y].player == self.player or  b[x,y].V >= self.V))\
                        or bk[x,y] == 1 or bk[x,y] == 4:
                        continue
                    probState.append((x,y))
        elif not self.evolution:
            print('not evolution')
            for x in range(b.shape[0]):
                for y in range(b.shape[1]):
                    if b[x,y]!=None or bk[x,y] == 1 or bk[x,y] == 4:
                        continue
                    probState.append((x,y))
        return probState
class Whale(animal):
    def __init__(self, player):
        animal.__init__(self,player)
        self.V = 9
        self.filling = []
    def possibleWay(self):
        x = self.x
        y = self.y
        b = self.b
        bk = self.background
        probState = util.basicMove(x,y,b,bk,self.player,self.V,0,2)
        for i in range(b.shape[0]):
                for j in range(b.shape[1]):
                    if b[i,j]!=None and b[i,j].player == self.player and\
                    abs(x-i) <=1 and abs(y-j)<=1 and (abs(x-i),abs(y-j))!=(1,1):
                        probState.append((i,j))
        return probState
