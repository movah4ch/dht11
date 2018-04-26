#!usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import time
import saveTempHumd
import getdhtData

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
            # 获取最新的数据
            self.saveDataToDB()
            # 将温湿度发送给客户端
            msg = self.getTempHumdData()
            clientsocket.send(msg.encode('UTF-8'))
            clientsocket.close()
            print('client socket closed')
            time.sleep(0.5)

    # 取出数据库存入的最新的数据, 温度，湿度和存入的时间
    def getTempHumdData(self):
        msg_tup = saveTempHumd.saveTempHumd.readData(self)
        # 将元组中的数据全部转化为string类型，并保存在list中
        msg_lst = [str(i) for i in msg_tup]
        msg_str = " ".join(msg_lst)
        return msg_str

    # 客户端发送refresh时，将读取的温湿度保存在数据库中
    def saveDataToDB(self):
        dht = getdhtData.dhtTempHumd()
        temp, humd = dht.getTempHumd()
        svt = saveTempHumd.saveTempHumd()
        svt.saveDate(temp, humd)


def main():
    cresoc = creatSocket()
    cresoc.creat_socket()


if __name__ == '__main__':
    main()
