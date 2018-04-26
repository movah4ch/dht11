#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time

PORT = 4


class dhtTempHumd(object):
    """
    变量定义：
    lst_data: 列表中的数据，用于表示二进制数据
    int_data: 十进制数据
    data[]: 从传感器获得的数据，长度为40
    humidity_bit, humidity_point_bit: 湿度的整数位和小数位的二进制数据
    temperature_bit, temperature_point_bit: 温度的整数和小数的二进制数据
    check_bit: 校验位的二进制数据
    """

    # 将二进制转化为10进制
    def binToInt(self, lst_data):
        int_data = 0
        if len(lst_data) is not 8:
            print('data error')
        else:
            for n in range(0, 8):
                int_data = lst_data[n] * 2**(7 - n) + int_data
        return int_data

    # 提供数据外部接口
    def getTempHumd(self):
        # 初始化参数
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        time.sleep(1)

        # start work
        gpio.setup(PORT, gpio.OUT)
        gpio.output(PORT, gpio.LOW)
        time.sleep(0.02)
        gpio.output(PORT, gpio.HIGH)
        # wait to response
        gpio.setup(PORT, gpio.IN)
        while gpio.input(PORT) == 1:
            continue

        while gpio.input(PORT) == 0:
            continue

        while gpio.input(PORT) == 1:
            continue
        # get data
        data = []
        for i in range(0, 40):
            k = 0
            while gpio.input(PORT) == 0:
                continue

            while gpio.input(PORT) == 1:
                k = k + 1
                if k > 100:
                    break

            if k < 8:
                data.append(0)
            else:
                data.append(1)
        # get temperature and humidity
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        # 将二进制数据转化成十进制
        humidity = self.binToInt(humidity_bit)
        oohumidity = self.binToInt(humidity_point_bit)
        temperature = self.binToInt(temperature_bit)
        ootemperature = self.binToInt(temperature_point_bit)
        check_date = self.binToInt(check_bit)
        if check_date == humidity + temperature + oohumidity + ootemperature:
            # print("temperature: {}".format(temperature))
            # print("humidity:{}".format(humidity))
            return temperature, humidity
        else:
            print("get data error")
            return False


def main():
    temphumd = dhtTempHumd()
    temp, humd = temphumd.getTempHumd()
    print("temperature:{}".format(temp))
    print("humidity:{}".format(humd))


if __name__ == "__main__":
    main()
