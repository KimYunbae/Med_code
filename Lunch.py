import _thread
from machine import Pin, SoftI2C
from bh1750 import BH1750
import time
from umqtt.simple import MQTTClient
import json

def read_luminance(sensor, label):
    start_time = time.time()
    values = []
    
    while time.time() - start_time <= 4:
        value = sensor.luminance(BH1750.ONCE_HIRES_1)
        rounded_value = round(value)
        print(label + ":", str(rounded_value))
        values.append(rounded_value)
        time.sleep(0.5)
       
    if values:
        average_value = round(sum(values) / len(values))
        print(label + " 평균:", str(average_value))
        message = {"Lunch": average_value}
        mqtt.publish(topic_pub, json.dumps(message))
        
scl = Pin(21)
sda = Pin(22)
i2c = SoftI2C(scl,sda)

meal = BH1750(i2c)


labels = ["아침", "점심", "저녁"]

_thread.start_new_thread(read_luminance, (meal, labels[1]))

while True:
    time.sleep(5)
    exec(open("main.py").read())
    
