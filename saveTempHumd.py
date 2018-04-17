#!usr/bin/env python3
# -*- coding: UTF-8 -*-

import sqlite3


class saveTempHumd(object):
    """docstring for ClassName"""

    def __init__(self):
        pass

    # 创建一个数据库和表，如果有则不创建
    def createTable(self):
        conn = sqlite3.connect('TempHumd.db')
        try:
            cursor = conn.cursor()
            cursor.execute('''create table if not exists temphumd(
            [id] integer primary key autoincrement,
            [temperature]     int       not NULL,
            [humidity]        int       not NULL,
            [times] TimeStamp not NULL default (datetime('now', 'localtime'))
            )''')
        except Exception as e:
            print("create date error")
            print(e)
            return False
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    # 向数据库中保存温度和湿度时间等数据
    def saveDate(self, temp, humd):
        parmas = (temp, humd)
        try:
            conn = sqlite3.connect('TempHumd.db')
            cursor = conn.cursor()
            cursor.execute('insert into temphumd\
             ([temperature], [humidity]) values(?, ?)', parmas)
        except Exception as e:
            print("save data error")
            print(e)
            return False
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    # 读取数据库中的数据
    def readData(self):
        try:
            conn = sqlite3.connect('TempHumd.db')
            cursor = conn.cursor()
            cursor.execute('select * from temphumd')
            values = cursor.fetchall()
            print(values)
        except Exception as e:
            print("read data error")
            print(e)
            return False
        finally:
            cursor.close()
            conn.close()


def main():
    svt = saveTempHumd()
    svt.createTable()
    svt.saveDate(20, 50)
    svt.readData()


if __name__ == '__main__':
    main()
