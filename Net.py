# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 15:54:58 2021

@author: jchen3031
"""

import socket
import pickle
import Board
#import Animals
class NetWork:
    def __init__(self,data = Board.Animal()):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = socket.gethostname()
        self.port = 6666
        self.address = (self.server,self.port)
        self.data = data
        self.id = self.connect()
        #print(self.data)
        #print('connect:', self.id)
    def connect(self):
        try:
            self.client.connect(self.address)
            # senddata = pickle.dumps(self.data)
            # self.send(senddata)
            # # #self.send(bytes('yeah'))
            # m = self.client.recv(40960)
            # data = pickle.loads(m)
            # self.data = data
            # print(data)
            # print('yes')
            # print(self.client.recv(40960).decode('utf-8'))
            
            #return self.client.recv(40960).decode('utf-8')
        except:
            print('disconnect')
            pass
    def update(self,data):
        d = pickle.dumps(data)
        self.send(d)
        #self.send(b'hellow')
        # m = self.client.recv(40960)
        # data = pickle.loads(m)
        return data
    def getData(self):
        m = self.client.recv(40960)
        # if m == 0:
        #     return m
        # print(m)
        data = pickle.loads(m)
        return data
    def send(self,data):
        self.client.send(data)
    def close(self):
        #self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
    def get(self):
        return self.data
# n = NetWork()
# # n.get()
# b = Board.Animal()
# n.update(b)
# print(n.get())
# n.close()
