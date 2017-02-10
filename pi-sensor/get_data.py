import time

## Import the bluepy library
from . import *
from bluepy.bluepy import sensortag


tag = sensortag.SensorTag('BC:6A:29:AC:53:D1')


### Connect to a tag

### Get data

### Send data to a sever

### Disconnect

time.sleep(1.0)
tag.IRtemperature.enable()
for i in range(5):
    tag.waitForNotifications(1.0)
    print tag.IRtemperature.read()
tag.disconnect()
del tag
