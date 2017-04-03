import os
import sys
import picamera
import requests
import base64
import httplib
import json
import os
import sys
import io
from prettytable import PrettyTable
from time import gmtime, strftime, sleep, time
import numpy as np
averagePersonCount = 0
def getAverage():
    return averagePersonCount
def reject_outliers(data):
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    return filtered

def smile(cwd):
    with picamera.PiCamera() as camera:
        camera.capture(cwd+'/image.jpg')
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())
    sleep(3)
    
def sendPicture(cwd, cameraTime):
    if cameraTime == None:
        cameraTime = 120
    tableOutput = PrettyTable(['Total', 'Time Taken'])
    total = []
    for i in range(0,cameraTime):
        smileTime = smile(cwd)
        base64_image = base64.b64encode(open(cwd+'/image.jpg').read())
        params = json.dumps({"image": base64_image})
        headers = {"Content-type": "application/json",
                   "X-Access-Token": "Se1cbirNqW0qNRKHIFvfVVUSVdeIqf0mdGUR"}
        r = requests.post("https://dev.sighthoundapi.com/v1/detections?type=person",data=params, headers=headers)
        personCount = r.content.count('person')
        #tableOutput.add_row([personCount,smileTime])
        #total.append(personCount)
    #print tableOutput
    filtered_total = reject_outliers(total)
    averagePersonCount = sum(i for i in filtered_total)/float(cameraTime)
    #print "Count Average: %s"%averagePersonCount
    #return averagePersonCount

cwd = os.getcwd()
cameraTime = 120
sendPicture(cwd, cameraTime)
