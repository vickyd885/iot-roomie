import time

## Import the bluepy librarylmao 
from bluepy.bluepy import btle, sensortag


tag = sensortag.SensorTag('C4:BE:84:72:67:86')


time.sleep(1.0)
tag.IRtemperature.enable()
for i in range(5):
    tag.waitForNotifications(1.0)
    print tag.IRtemperature.read()


tag.disconnect()
del tag
