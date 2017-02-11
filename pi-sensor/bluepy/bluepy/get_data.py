import time

## Import the bluepy librarylmao 
from bluepy.bluepy import sensortag

tag = sensortag.SensorTag('C4:BE:84:72:67:86')

time.sleep(1.0)
tag.IRtemperature.enable()
for i in range(5):
    tag.waitForNotifications(1.0)
    print tag.IRtemperature.read()

tag.disconnect()
del tag


def enableAllSensors(sensor_id):
    sensor_id.IRtemperature.enable()
    sensor_id.IRtemperature.enable()
def getData():
    
