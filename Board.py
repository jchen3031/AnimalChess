# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 02:27:17 2021

@author: jchen3031
"""
import Animals
import numpy as np
class Board:
    def __init__(self):
        self.reset()
        # print(self.board)
    def getBoard(self):
        return self.board
    def reset(self):
        x = np.zeros((7,9))
        for i in range(3,6):
            for j in range(0,6):
                if (j!= 0 and j!=3 and j!=6):
                    x[j][i] = 1
        x[3][0] = 4
        x[3][8] = 4
        x[3][4] = 4
        # x[3][1] = 3
        # x[4][0] = 3
        # x[2][0] = 3
        # x[3][7] = 3
        # x[4][8] = 3
        # x[2][8] = 3
        self.board = x
        self.x,self.y = x.shape
    def put(self, pos, n):
        self.board[pos[0]][pos[1]] = n
    def get(self, pos):
        return self.board[pos[0]][pos[1]]
class Animal:
    def __init__(self):
        self.reset()
        # print(self.board)
    def getBoard(self):
        return self.board
    def reset(self):
        x = np.ndarray((7,9), dtype = object)#np.zeros((7,9,2))
        x[0][0] = Animals.Whale(True)
        x[1][1] = Animals.Horse(True)
        x[6][0] = Animals.Pig(True)
        x[5][1] = Animals.Monkey(True)
        x[0][2] = Animals.Donkey(True)
        x[2][2] = Animals.Goose(True)
        x[4][2] = Animals.GoldFish(True)
        x[6][2] = Animals.Chick(True)
        # x[6][2] = Animals.Chick(True)
        # x[0][2] = Animals.Donkey(True)
        self.board = x.copy()
        self.reflect()
        self.x,self.y = x.shape
    def put(self, pos, n):
        self.board[pos[0]][pos[1]] = n
    def get(self, pos):
        return self.board[pos[0]][pos[1]]
    def reflect(self):
        m,n = self.board.shape
        #print(self.board)
        for i in range(m):
            for j in range(n):
                if self.board[i][j]!=None:
                    self.board[m-1-i][n-1-j] = self.board[i,j].clone()
                    self.board[m-1-i][n-1-j].player = not self.board[i,j].player
    def __str__(self):
        return str(self.board)
    def __repr__(self):
        return self.board
    def __iter__(self):
        self.ix = 0
        self.iy = 0
        return self
    def __next__(self):
        if self.ix <= self.x-1:
            i = self.ix
            self.ix += 1
            return self.board[i,self.iy]
        elif self.iy < self.y-1:
            self.ix = 0
            i = self.ix
            self.ix += 1
            self.iy += 1
            return self.board[i,self.iy]
        else:
            raise StopIteration
    def equal(self,b):
        return self.__str__()==b.__str__()
