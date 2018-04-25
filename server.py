#!usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import time
import saveTempHumd

# HOST = "192.168.191.3"
# PORT = 8001


class creatSocket(object):
    """docstring for creatSocket"""

    def creat_socket(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = '192.168.191.3'
        PORT = 8001
        serversocket.bind((HOST, PORT))
        serversocket.listen(5)

        while True:
            clientsocket, addr = serversocket.accept()
            print("连接地址：{}".format(addr))
            msg_tup = saveTempHumd.saveTempHumd.readData(self)
            msg_str = [str(i) for i in msg_tup]
            clientsocket.send(("".join(msg_str)).encode('UTF-8'))
            clientsocket.close()
            print('client socket closed')
            time.sleep(0.5)


def main():
    cresoc = creatSocket()
    cresoc.creat_socket()


if __name__ == '__main__':
    main()
