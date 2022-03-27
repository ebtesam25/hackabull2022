import time
import busio
import board
import adafruit_bme680
from adafruit_bme280 import basic as adafruit_bme280
from analogio import AnalogIn
from secrets import secrets 
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=118)
an3 = AnalogIn(board.A3)
an2 = AnalogIn(board.A2)

samples = [0] * 10
hsamples = [0] * 10
datas = []

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])

while True:
    #print((sensor.temperature,sensor.humidity))
    #print((bme280.temperature, bme280.humidity))
    #print("BME688(Top): {}, BME280(Bottom): {}".format(sensor.humidity,bme280.humidity))
    #print(sensor.humidity-bme280.humidity)
    for i in range(10):
        os = 0
        hos = 0
        for e in range(5):
            dh = sensor.humidity-bme280.humidity
            skin = an3.value-an2.value
            hos += float(dh)
            os += float(skin)
        samples[i] = os/5
        hsamples[i] = hos/5
        mean = sum(samples) / float(len(samples))
        hean = sum(hsamples) / float(len(hsamples))
        data = [mean,hean, bme280.temperature]
        datas.append(data)
        if len(datas) == 5:
            print(datas)
            datas = []
        time.sleep(0.5)
        #print(datas)

