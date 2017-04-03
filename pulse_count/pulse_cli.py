import subprocess as sub
import threading
import sys
import csv
import re
import manuf
from prettytable import PrettyTable
import os
import time
import json
import datetime
import io
import picamera
import requests
import base64
import httplib
import numpy as np
import warnings


# Normalizes Data for Camera
def reject_outliers(data):
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    return filtered

# Takes Photo with pi camera
def smile(wd):
    with picamera.PiCamera() as camera:
        camera.hflip = True
        camera.vflip = True
        camera.capture(wd+'/image.jpg')
    #time.sleep(3)

# Generates People Count Data
def sendPicture(wd, cameraTime): 
    try:
        peopleCountResults = readPeopleCount(wd)
    except:
        peopleCountResults = {}
    if cameraTime == None:
        cameraTime = 5
    while 1:
        total = []
        with open(wd+'/peopleCountRaw.text', 'a') as f:
                f.write("Data stream starting at "+str(datetime.datetime.now())+"\n\n")
        for i in range(0,(cameraTime*60)/3):
            smile(wd)
            base64_image = base64.b64encode(open(wd+'/image.jpg').read())
            params = json.dumps({"image": base64_image})
            headers = {"Content-type": "application/json",
                       "X-Access-Token": "Se1cbirNqW0qNRKHIFvfVVUSVdeIqf0mdGUR"}
            r = requests.post("https://dev.sighthoundapi.com/v1/detections?type=person",data=params, headers=headers)
            personCount = r.content.count('person')
            with open(wd+'/peopleCountRaw.text', 'a') as f:
                f.write(str(datetime.datetime.now()) + " : " + str(personCount)+"\n")
        filtered_total = reject_outliers(total)
        averagePersonCount = sum(i for i in filtered_total)/float((cameraTime*60)/3)
        peopleCountResults.update({str(datetime.datetime.now()):averagePersonCount})       
        writePeopleCount(peopleCountResults, wd)
        #upload people count: 

# Manipulate peopleCount File
def readPeopleCount(wd):
    with open(wd+'/peopleCount.json', 'r') as f:
        try:
            peopleCountResults = json.load(f)
        except ValueError:
            peopleCountResults = {}
    return peopleCountResults
def writePeopleCount(peopleCountResults, wd):
    with open(wd+'/peopleCount.json', 'w') as f:
        json.dump(peopleCountResults, f)
def printPeopleCount(wd):
    peopleCountResults = readPeopleCount(wd)
    tableOutput = PrettyTable(['Time Recorded', 'People Count'])
    for time in sorted(peopleCountResults.iterkeys(), reverse=True):
        tableOutput.add_row([time, peopleCountResults[time]])
    print tableOutput

# Reads raw CSV and filters stations and clients
def csv2blob(filename):
    with open(filename,'rb') as f:
        z = f.read()
    #replace any null characters with string repr
    z = z.replace('\x00', 'NULL')
    # Split into two parts: stations (APs) and clients
    parts = z.split('\r\n\r\n')    
    clients = parts[1]
    if sys.version_info[0] < 3:
        from StringIO import StringIO
    else:
        from io import StringIO
    clients_str  = StringIO(clients)
    r = csv.reader(clients_str)
    i = list(r)

    z = [k for k in i if k <> []]
    clients_list = z
    return clients_list

# Reads CSV for dataCollect and csvScan and filters columns
def startCSV(csvfile):
    p = manuf.MacParser()
    clientList = []
    clients_list = csv2blob(csvfile)
    for client in clients_list:
        if client[0] != "Station MAC":
            clientList.append( [ p.get_manuf(str(client[0])), client[0], client[3], p.get_comment(str(client[0])), client[2]] )
    return clientList

# Get's wireless system name ie wlan0 from given mac address
def getMac(monitorMac):
    if os.path.exists('/sys/class/net/mon0'):
        return None
    else:
        i = 0
        try:
            while 1:
                mac = open('/sys/class/net/wlan'+str(i)+'/address').readline()
                if monitorMac in mac:
                    return i
                else:
                    i += 1
        except Exception as e:
            print "Error: "+str(e)+"\n"
            print "Monitor Wireless Device Not Found\nExiting Program"
            exit()

# Scan: Initates the set up of monitor mode, then removes existing wireless csv files and begins scan.                
def Scan(monitorMac, wd):      
    if monitorMac != "" and monitorMac != None:
        wlanValue = getMac(monitorMac)
    else:
        wlanValue = 0 #Default to wlan0
    if wlanValue != None:
        try:
            sub.Popen("sudo airmon-ng start wlan%s  > /dev/null 2>&1"%wlanValue, shell=True, stdout=open(os.devnull, 'wb'))
            print "wlan%s now in monitor mode"%wlanValue
        except:
            print "Error unable to put wlan%s into monitor mode\n Exiting Program"%wlanValue
            exit()
    try:
        os.system('sudo rm %s/wirelessCapture*'%wd)
    except:
        print "wirelessCapture File does not exist creating one"
    time.sleep(1)
    sub.Popen("sudo airodump-ng --ignore-negative-one --output-format csv --write %s/wirelessCapture mon0 --channel [1,2,3,4,5,6,7,8,9,10,11,12,13,36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,151,153,155,157,161,165] > /dev/null 2>&1 &"%wd, shell=True, stdout=open(os.devnull, 'wb'))
    print "Scan Initiated in background."
# Part of Scan: NeverEnding While loop to read wireless collection and upload        
def dataCollect(blacklistPercent, uploadTime, wd):
    if blacklistPercent == None:
        blacklistPercent = 80
    if uploadTime == None:
        uploadTime = 5
    blacklist = readBlacklist(wd)
    while(1):
        positives = {}
        time.sleep(uploadTime*60)
        for i in range(0,(24*60)/uploadTime):
            clientList = startCSV(wd+'/wirelessCapture-01.csv')
            for filteredClientList in clientList:
                datetime_object = datetime.datetime.strptime(filteredClientList[4], ' %Y-%m-%d %H:%M:%S')
                if int(filteredClientList[2]) > -25 and filteredClientList[1] not in blacklist and datetime_object > (datetime.datetime.now() - datetime.timedelta(minutes = int(uploadTime))):
                    if filteredClientList[1] in positives:
                        if positives[filteredClientList[1]] > (((24*60)/uploadTime)/100)*blacklistPercent:
                            del positives[filteredClientList[1]]
                            blacklist.update({filteredClientList[1]:str(datetime.datetime.now())})
                            #Update upload remove
                        else:
                            positives[filteredClientList[1]] += 1
                            #Update upload
                    else:
                        positives.update({filteredClientList[1]:1})
                        #Update upload
            writeBlacklist(blacklist, wd)

# Prints out client list or all    
def csvScan(key, wd):
    try:
        clientList = startCSV(wd+'/wirelessCapture-01.csv')
        cleintList = clientList.sort(key=lambda x: x[4], reverse=True)
        tableOutput = PrettyTable(['Vendor', 'MAC Address', 'Power', 'Comment', 'Last Seen'])
        for filteredClientList in clientList:
            if key != "all":
                datetime_object = datetime.datetime.strptime(filteredClientList[4], ' %Y-%m-%d %H:%M:%S')
                if int(filteredClientList[2]) > -25 and datetime_object > (datetime.datetime.now() - datetime.timedelta(minutes = 5)):
                    tableOutput.add_row(filteredClientList)
            else:
                tableOutput.add_row(filteredClientList)
        print tableOutput
    except Exception as e:
        print e
        
# Manipulate Blacklist File
def readBlacklist(wd):
    with open(wd+'/blacklist.json', 'r') as f:
        try:
            blacklist = json.load(f)
        except ValueError:
            blacklist = {}
    return blacklist
def writeBlacklist(blacklist, wd):
    with open(wd+'/blacklist.json', 'w') as f:
        json.dump(blacklist, f)
def printBlacklist(wd):
    blacklist = readBlacklist(wd)
    p = manuf.MacParser()
    tableOutput = PrettyTable(['Vendor', 'MAC Address', 'Date Added', 'Comment'])
    for macAddress, dateAdded in blacklist.items():
        tableOutput.add_row([p.get_manuf(str(macAddress)), macAddress, dateAdded, p.get_comment(str(macAddress))])
    print tableOutput
    
# Read in Variables
def readVariables(wd):
    with open(wd+'/variables.txt') as variableFile:
        for line in variableFile:
            fields = line.strip().split('=')
            if fields[0] == 'monitorMac':
                if fields[1] != "None":
                    monitorMac = fields[1]
                else:
                    monitorMac = None
            elif fields[0] == 'uploadTime':
                if fields[1] != "None":
                    uploadTime = fields[1]
                else:
                    uploadTime = None
            elif fields[0] == 'blacklistPercent':
                if fields[1] != "None":
                    blacklistPercent = fields[1]
                else:
                    blacklistPercent = None
            elif fields[0] == 'cameraTime':
                if fields[1] != "None":
                    cameraTime = fields[1]
                else:
                    cameraTime = None
    return monitorMac, uploadTime, blacklistPercent, cameraTime

# Reassign Variable Values
def editVariable(variableName, newValue, monitorMac, uploadTime, blacklistPercent, cameraTime, wd):
    with open(wd+'/variables.txt', 'w') as variableFile:
        if variableName == 'monitormac':
            monitorMac = newValue
            variableFile.write("monitorMac=%s\nuploadTime=%s\nblacklistPercent=%s\ncameraTime=%s"%(newValue,uploadTime,blacklistPercent,cameraTime))
        elif variableName == 'uploadtime':
            uploadTime = newValue
            variableFile.write("monitorMac=%s\nuploadTime=%s\nblacklistPercent=%s\ncameraTime=%s"%(monitorMac,newValue,blacklistPercent,cameraTime))
        elif variableName == 'blacklistpercent':
            blacklistPercent = newValue
            variableFile.write("monitorMac=%s\nuploadTime=%s\nblacklistPercent=%s\ncameraTime=%s"%(monitorMac,uploadTime,newValue,cameraTime))
        elif variableName == 'cameratime':
            cameraTime = newValue
            variableFile.write("monitorMac=%s\nuploadTime=%s\nblacklistPercent=%s\ncameraTime=%s"%(monitorMac,uploadTime,blacklistPercent,newValue))
        return monitorMac, uploadTime, blacklistPercent, cameraTime

# Cli Menu
def menu(monitorMac, uploadTime, blacklistPercent, cameraTime, wd):
        try:
            #Get raw input from user
            command = raw_input("Pulse>")
            command = command.lower().split()
            # display information
            if command[0] == "show":
                try:
                    if command[1] == "monitormac":
                        print "monitorMac = " + str(monitorMac)
                    elif command[1] == "blacklistpercent":
                        print "blacklistPercent = " + str(blacklistPercent)
                    elif command[1] == "uploadtime":
                        print "uploadTime = " + str(uploadTime)
                    elif command[1] == "cameraTime":
                        print "cameraTime = " + str(cameraTime)
                    elif command[1] == "blacklist":
                        printBlacklist(wd)
                    elif command[1] == "clientlist":
                        csvScan(None, wd)
                    elif command[1] == "all":
                        csvScan("all", wd)
                    elif command[1] == "peoplecount":
                        printPeopleCount(wd)
                    elif command[1] == "?" or command[1] == "help" or command[1] == "-h":
                        print "\nOptions for show command:\nmonitor-mac    : displays the current set mac address of registered wlan device.\nblacklistPercent    : displays the current set value for blacklistPercent.\nuploadTime    : displays the current set value for uploadTime.\ncameraTime    : displays the current set value for cameraTime.\nblacklist    : display all mac addresses in blacklist\nclientlist    : display filtered captured mac addresses.\nall    : display ALL captured mac addresses.\nhelp    : display help information\n"
                    else:
                        print "Error with '%s', use 'show help' to see options."%command[1]
                except:
                    print "show command not recognised, use 'show help' to see options."
            # manipulate blacklist                   
            elif command[0] == "blacklist":
                try:
                    if command[1] == "remove" or command[1] == "add":
                        try:
                            blacklist = readBlacklist(wd)
                            command[2] = command[2].upper()
                            if command[1] == "remove":
                                del blacklist[command[2]]
                                writeBlacklist(blacklist, wd)
                            elif command[1] == "add" and re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", command[2].lower()):
                                command[2].upper()
                                blacklist.update({command[2]:str(datetime.datetime.now())})
                                writeBlacklist(blacklist, wd)
                            elif command[2] == "?" or command[2] == "help" or command[2] == "-h":
                                print "\n Format for blacklist remove|add command:\nMAC_Address Format    : aa:aa:aa:aa:aa:aa\nRemove example    : blacklist remove aa:aa:aa:aa:aa:aa\nAdd example    : blacklist add aa:aa:aa:aa:aa:aa\n"
                            else:
                                print "Error with blacklist %s '%s', format to use 'blacklist %s aa:aa:aa:aa:aa:aa'."%(command[1], command[2], command[1])
                        except Exception as e:
                            print e
                            print "blacklist %s '%s' command not recognised, use 'blacklist %s help' to see options."%(command[1], command[2], command[1])
                    elif command[1] == "?" or command[1] == "help" or command[1] == "-h":
                        print "\nOptions for blacklist command:\nremove [MAC_Address]   : remove MAC_Address from blacklist\nadd [MAC_Address]    :  add MAC_Address to blacklist\nhelp    : display help information\n"
                    else:
                       print "Error with '%s', use 'blacklist help' to see options."%command[1]
                except:
                    print "blacklist command not recognised, use 'blacklist help' to see options."
            # Begin scan and create upload daemon                    
            elif command[0] == "scan":
                Scan(monitorMac, wd)           
                thread = threading.Thread(target = dataCollect, args = (blacklistPercent, uploadTime,wd))
                thread.daemon = True
                thread.start()
                if uploadTime == None:
                    printUploadTime = 5
                else:
                    printUploadTime = uploadTime
                if blacklistPercent == None:
                    printBlacklistPercent = 80
                else:
                    printBlacklistPercent = blacklistPercent
                print "Collecting Data and uploading data every %s minutes. Blacklist Percent Threshold set to %s%%"%(printUploadTime,printBlacklistPercent)
            elif command[0] == "peoplecount":
                if cameraTime == None:
                    printCameraTime = 5
                else:
                    printCameraTime = cameraTime
                print "People Count Initiated in background.\nUploading data every %s minutes."%printCameraTime 
                thread = threading.Thread(target = sendPicture, args = (wd,None))
                thread.daemon = True
                thread.start()
            # Set Variable Values            
            elif command[0] == "set":
                if command[1] == "monitormac" or command[1] == "uploadtime" or command[1] == "blacklistpercent" or command[1] == "cameratime":
                    try:
                        command[2] = command[2]
                        monitorMac, uploadTime, blacklistPercent, cameraTime = editVariable(command[1], command[2], monitorMac, uploadTime, blacklistPercent, wd)
                    except:
                        print "Error with set %s '%s', use 'set %s help' to see options."%(command[1], command[2], command[1])
                elif command[1] == "?" or command[1] == "help" or command[1] == "-h":
                    print "\nOptions for set command:\nmonitorMac    : hardware mac address of wireless device used for monitoring. Defaults to Mac address of wlan0.\nblacklistPercent    : percentage value for total occurance of a device in one cycle [(24*60)/uploadTime] to mark blacklisted. Default 80\nuploadTime    : how often should data be uploaded in MINUTES. Default 5\cameraTime    : how many picture camera should take before average result is uploaded. Default 120\nhelp    : display help information\n"
                else:
                    print "set command not recognised, use 'set help' to see options."
            # Exit Program               
            elif command[0] == "exit":
                sys.exit(1)
            # Help 
            elif command[0] == "?" or command[0] == "help" or command[0] == "-h":
                print "\nOptions:\nset    : set variables\nshow    : display information\npeoplecount   : start camera peoplecount to collect data and upload.\nscan    : start wireless scan to collect data and upload.\nblacklist    : edit data stored in blacklist.\nexit    : Stop wireless scan and shutdown program.\nhelp    : display help information\n"
            else:
                print "\nOptions:\nset   : set variables\nshow    : display information\npeoplecount   : start camera peoplecount to collect data and upload.\nscan    : start wireless scan to collect data and upload.\nblacklist    : edit data stored in blacklist.\nexit    : Stop wireless scan and shutdown program.\nhelp    : display help information\n"
        # Ctr-C exit
        except KeyboardInterrupt:
            print "\nNextime please use 'exit' to shutdown program safely."
            sys.exit(1)
        # return - Help
        except Exception as e:
            print e
            print "\nUse 'exit' to shutdown program or 'help' or '-h' or '?' to see options."

try:
    wd = os.path.dirname(os.path.realpath(__file__))
    monitorMac, uploadTime, blacklistPercent, cameraTime = readVariables(wd)
    warnings.filterwarnings("ignore")
    print '''
    ____________________________________________________                                                
     __________________________________________________ 

      /$$$$$$$  /$$   /$$ /$$        /$$$$$$  /$$$$$$$$
     | $$__  $$| $$  | $$| $$       /$$__  $$| $$_____/
     | $$  \ $$| $$  | $$| $$      | $$  \__/| $$      
     | $$$$$$$/| $$  | $$| $$      |  $$$$$$ | $$$$$   
     | $$____/ | $$  | $$| $$       \____  $$| $$__/   
     | $$      | $$  | $$| $$       /$$  \ $$| $$      
     | $$      |  $$$$$$/| $$$$$$$$|  $$$$$$/| $$$$$$$$
     |__/       \______/ |________/ \______/ |________/

     __________________________________________________                                                
    ____________________________________________________

    Welcome  to the Pulse CLI:
    Use \'help\' to see options.
                                                      
    '''
    while True:
        menu(monitorMac, uploadTime, blacklistPercent,cameraTime, wd)
except Exception as e:
    print e
    



        

