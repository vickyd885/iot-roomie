import time
import requests # remember to pip install this!

## Import the bluepy library
import sensortag

## Define server address!

server = "http://localhost:3000/insertData/roomdata"

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


    for i in range(5):
        sensor_tag.waitForNotifications(1.0)
        temp = sensor_tag.IRtemperature.read()
        humidity = sensor_tag.humidity.read()
        light = sensor_tag.lightmeter.read()
        print "got data:  ", temp, " ", humidity," ", light
        ppl_count = 1
        noise  = 0
        name = "vickys" 
        
        send_data_via_post(temp, humidity,light, name, ppl_count, noise)

def send_data_via_post(temp, humidity, light, name, ppl_count, noise):
    
    payload = { 'temp':temp, 'light': light, 'room': name, 'people': ppl_count}
    r = requests.post(server, data=payload)

def run():

    print "Hello!"
    print sensors_list

    ## enable Sensors
    for sensor_tag in sensors_list:
        enable_all_sensors(sensor_tag)

    print "Finished enabling all sensors"
    
    ## sleep for a bit to allow for sensors to be initiatlised
    time.sleep(1.0)

    
    for sensor_tag in sensors_list:
        poll_sensor_tag(sensor_tag)

    for sensor_tag in sensors_list:
        disconnect_from_all_sensors(sensor_tag)




run()
