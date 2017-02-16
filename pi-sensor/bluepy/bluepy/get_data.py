import time
import requests # remember to pip install this!

## Import the bluepy library
from bluepy.bluepy import sensortag

## Hold list of sensors!
sensors_list = []

sensors_list.append( sensortag.SensorTag('C4:BE:84:72:67:86'))

def enable_all_sensors(sensor_tag):
    sensor_tag.IRtemperature.enable()
    sensor_tag.humidity.enable()
    sensor_tag.lightmeter.enable()

def disconnect_from_all_sensors(sensor_tag):
    sensor_tag.disconnect()

def poll_sensor_tag(sensor_tag):

    # to be changed to something more specific later
    for(i in range(5)):
        sensor_tag.waitForNotifications(1.0)
        temp = sensor_tag.IRtemperature.read()
        humidity = sensor_tag.humidity.read()
        light = sensor_tag.lightmeter.read()
        send_data_via_post(temp, humidity,light)

def send_data_via_post(temp, humidity, light):
    payload = { 'temp':temp, 'humidity': humidity, 'light': light}
    r = requests.post("..", data=payload)

def run():

    ## enable Sensors
    for( sensor_tag in sensors_list):
        enable_all_sensors(sensor_tag)

    ## sleep for a bit to allow for sensors to be initiatlised
    time.sleep(1.0)

    for(sensor_tag in sensors_list):
        poll_sensor_tag(sensor_tag)

    for( sensor_tag in sensors_list):
        disconnect_from_all_sensors(sensor_tag)





def __main__():
    def run()
