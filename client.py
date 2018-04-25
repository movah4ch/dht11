#!usr/bin/env python3
# coding=utf-8

import socket

HOST = '192.168.191.3'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

msg = s.recv(1024)
s.close()
print(msg.decode('utf-8'))
