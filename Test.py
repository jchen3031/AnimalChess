# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 03:40:35 2021

@author: jchen3031
"""
import numpy as np
x = np.zeros((7,9,2))
x[0][0] = [9,True]
x[1][1] = [6,True]
x[6][0] = [8,True]
x[5][1] = [7,True]
x[0][2] = [5,True]
x[2][2] = [4,True]
x[4][2] = [2,True]
x[6][2] = [3,True]
def reflect(x):
    m,n,z = x.shape
    for i in range(m):
        for j in range(n):
            if x[i][j][0]!=0:
                x[m-1-i][n-1-j] = x[i,j]
    return x
# print(reflect(x))