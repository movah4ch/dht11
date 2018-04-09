#!usr/bin/env python3
# coding = utf-8

import RPi.GPIO as gpio
import time

PORT = 4  # GPIO.7的BCM编码为4

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
time.sleep(1)


# 将二进制转化为10进制
def binToInt(lst_data):
    int_data = 0
    if len(lst_data) is not 8:
        print('data error')
    else:
        for n in range(0, 8):
            int_data = lst_data[n] * 2**(7 - n) + int_data
    return int_data


# start work
def initGPIO():
    gpio.setup(PORT, gpio.OUT)
    gpio.output(PORT, gpio.LOW)
    time.sleep(0.02)
    gpio.output(PORT, gpio.HIGH)


# wait to response
def waitResponse():
    gpio.setup(PORT, gpio.IN)
    while gpio.input(PORT) == 1:
        continue

    while gpio.input(PORT) == 0:
        continue

    while gpio.input(PORT) == 1:
        continue


# get data
def getData(data):
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
    return data


# get temperature and humidity
def dataHandler(data):
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    print(data)

    humidity = binToInt(humidity_bit)
    oohumidity = binToInt(humidity_point_bit)
    temperature = binToInt(temperature_bit)
    ootemperature = binToInt(temperature_point_bit)
    check_date = binToInt(check_bit)

    if check_date == humidity + temperature + oohumidity + ootemperature:
        print("temperature: {}".format(temperature))
        print("humidity:{}".format(humidity))
    else:
        print("get data error")


def main():
    data = []
    initGPIO()
    waitResponse()
    re_data = getData(data)
    dataHandler(re_data)


if __name__ == '__main__':
    main()
