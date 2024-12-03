import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient

wifi_ssid = ""
wifi_password = ""
aws_endpoint = 

thing_name = ""
client_id = ""
private_key = ""
private_cert = ""


with open(private_cert, 'rb') as f:
    cert = f.read()
with open(private_key, 'rb') as f:
    key = f.read()

topic_pub = "esp32/pub"
topic_sub = "esp32/sub"
ssl_params = {"key": key, "cert": cert, "server_side": False}

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass
    print('Connection successful')
    print('Network config:', wlan.ifconfig())

mqtt = None

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    global mqtt
    mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Connected")


def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(message)
    if 'message' in message:
        script_name = message['message']
        script_file = script_name + '.py'
        try:
            exec(open(script_file).read())
        except OSError as e:
            print("Error:", e)
            print("Script file not found:", script_file)




def mqtt_publish(topic, message):
    print("Publishing message to AWS IoT...")
    mqtt.publish(topic, message)
    print("Message published")




try:
    mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)
    mqtt.subscribe(topic_sub)
except Exception as e:
    print("Unable to connect to MQTT:", e)

while True:
    try:
        mqtt.check_msg()
    except Exception as e:
        print("Error checking message:", e)
    print("명령 대기중")
    time.sleep(5)


