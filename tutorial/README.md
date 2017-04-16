# Documentation and Tutorial

This documentation contains two tutorials that are based off the application, Pulse, that we built as part of the Internet of Things module. First, we will **walk through building a NodeJs application** as well as **interfacing a Pi with a SensorTag.** These tutorials assume that you have some working knowledge with programming languages, websites and electronics.

## Interfacing a SensorTag on a Raspberry Pi

Ensure you have a Raspberry Pi with an operating system reading and working. _Python_ comes preinstalled and ready to go on the Raspberry Pi.
If you need to install an OS, instructions can be found [here](https://www.raspberrypi.org/documentation/installation/noobs.md).

We will be interfacing the SensorTag using the [bluepy](https://github.com/IanHarvey/bluepy) library over _bluetooth_.

The code needs an executable bluepy-helper to be compiled from C source. This is done automatically if you use the recommended pip installation method (see below). Otherwise, you can rebuild it using the Makefile in the bluepy directory.

To set up the library on the Pi, open _terminal_ and run:

```shell
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip install bluepy
```

### Finding Sensor Tags

Turn on your sensor tag and restart the bluetooth service

```
sudo service bluetooth restart
```

Scan for bluetooth devices
```
sudo hcitool lescan

BC:6A:29:AC:53:D1 SensorTag
```

This is the _Mac address_ of the SensorTag near by, remember to record as you'll need it.

### A basic script

Once that's setup, `cd` into the folder `bluepy/bluepy`

Create a file `get_data.py` in `bluepy/bluepy`

```python
import time
import sensortag

tag = sensortag.SensorTag('BC:6A:29:AC:53:D1') # Your mac address goes here

time.sleep(1.0)
tag.IRtemperature.enable() # Enable the temp sensor
for i in range(5):
  tag.waitForNotifications(1.0) # Sleep for a bit
  print tag.IRtemperature.read()
tag.disconnect()
del tag
```

You can run this by `python get_data.py`

### Reading Sensor Tag Data

The sensor tag provides the following information that can be captured:

- IR Temperature, both object and ambient temperature
- Accelerometer, 3 axis
- Humidity, both relative humidity and temperature
- Magnetometer, 3 axis
- Barometer, both pressure and temperature
- Gyroscope, 3 axis


### A more advanced script

```python
import time
import requests # remember to pip install this!

## Import the bluepy library
import sensortag

## Define server address!
server = "http://iotucl.cloudapp.net:3000/insertDB/roomdata/" ## This address accesses our database.

## Hold list of sensors!
sensors_list = []

sensors_list.append(sensortag.SensorTag('C4:BE:84:72:67:86'))

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

def run(): # Main Function
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
```

This is an example of what you can do by reading the documentation and connecting multiple sensor tags. Here we are not only getting data from the sensor tag, we are posting to a server which is saving these into a database. This is explained in the next bit.

## Building a webapp with NodeJs

Let's a build a [NodeJS](https://nodejs.org/en/) app that takes data from our earlier script when it's running on a server and inserts it into a [NoSQL](http://nosql-database.org/) database.

### Setup

To start creating the application, first make sure to have [node installed](https://nodejs.org/en/download/) and then install the Express framework globally using NPM so that it can be used to create a web application using node terminal.

```
$ npm install express --save
```

To create the project folder, run the following command which is is going to auto-generate a website skeleton in a new directory called roomie-server

```
express roomie-server
```

And install the dependencies by running:

```
npm install
```

Create a directory called data that will store all the database files:

```
mkdir data
```
Open your project folder in an editor and check the bin/www file which starts the server and listens on port 3000 for connection. The port can be changed if it’s already in use by another process:

```js
var app = require('../app');
var debug = require('debug')('roomie-server:server');
var http = require('http');

var port = normalizePort(process.env.PORT || '3000');
app.set('port', port);

var server = http.createServer(app);

server.listen(port);
server.on('error', onError);
server.on('listening', onListening);
```

For a more detailed tutorial, follow this [link](http://cwbuecheler.com/web/tutorials/2013/node-express-mongo/)

### Inserting Data

Now we will start building a result. Express application uses a callback function whose parameters are request and response objects. A request object represents the HTTP request and has properties for the request query string, parameters, body, HTTP headers, and so on. A response object represents the HTTP response that an Express app sends when it gets an HTTP request.

```js
app.get('/', function (req, res) {
   // --
})
```
To insert new data into MongoDB, we need to have a look at how basic routing works. Routing refers to determining how an application responds to a client request to a particular endpoint, which is a URI (or path) and a specific HTTP request method (GET, POST, and so on).

```js
router.post('/roomdata', function(req, res, next) {
  var data = {
    "roomName": req.body.room,
    "heat": req.body.heat,
    "noise": req.body.noise,
    "lighting": req.body.light,
    "peopleCount": req.body.people
  }
  MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    insertDocument(db, data, function() {
        db.close();
        res.send("Accepted!");
    });
  });
});
```

Where the url variable holds the connection to the database, specifying the port and database name:

`var url = 'mongodb://localhost:27017/roomsdb';`
`
The insertDocument method will insert the values as a new record to an existing MongoDB collection (reminder: each room is represented by a collection) or will create a new one if it doesn’t exist one with the specified name (if the room doesn’t exist yet in the database):

```js
var insertDocument = function(db, data, callback) {
   console.log(String(data['roomName']));
   db.collection( String(data['roomName']) ).insertOne(
     {
       data: [
         {
           timeStamp: new Date(),
           heat: data['heat'],
           noise: data['noise'],
           lighting: data['lighting'],
           peopleCount: data['peopleCount']
         }
       ]
     }, function(err, result) {
    assert.equal(err, null);
    console.log("Inserted data for the room.");
    callback();
  });
};
```
The new `Date()` method has been used to get the current time when the data is saved.

### Retrieving

Get all the rooms’data
Each of the methods provided above will be implemented as an express request as follows:

```js
router.get('/roomdata/:name', function(req, res, next) {
  MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    roomInfo(db, req.params.name, null, function(data) {
        console.log("heard request for room: "+req.params.name);
        db.close();
        res.send(data);
    });
  });
});
```

The main function here is `roomInfo()` which queries the MongoDb like this: You can build your own handlers

```js

var roomInfo = function(db, name, time, callback) {
  var cursor;

  var today = moment();
  if(time == "month"){
    cursor = db.collection(name ).find({
      "created_at": { $gte: new Date( today.subtract(1, "months").toString() )}});

   }else if(time == "day"){
     cursor = db.collection(name ).find({
       "created_at": { $gte: new Date( today.subtract(1, "day").toString() )}});
   } else{
     cursor = db.collection(name).find( );
   }
   var listOfRooms = [];
   cursor.each(function(err, doc) {
      assert.equal(err, null);
      if (doc != null) {
         listOfRooms.push(doc);
      } else {
         callback(listOfRooms);
      }
   });

};
```

These are of course just the basic, you can add much more functionality by building of the tutorials we used here, as we have done for our project. If you want more information, feel free to use these refernces:

[NodeJs](https://nodejs.org/en/)
[Express](https://expressjs.com/) 
[Restful APIs](https://en.wikipedia.org/wiki/Representational_state_transfer)
[MongoDB](https://docs.mongodb.com/manual/installation/)
[Sensor Tag Data](http://processors.wiki.ti.com/index.php/SensorTag_User_Guide#IR_Temperature_Sensor)
[Setting Up NodeJs and Express Server](http://cwbuecheler.com/web/tutorials/2013/node-express-mongo/)
[Bluepy library](http://ianharvey.github.io/bluepy-doc/) - github library provided by [IanHarvey](https://github.com/IanHarvey/bluepy)


