# iot-roomie

This repo contains source code for a project Internet of Things module at UCL.

We aim to use environmental data of rooms to help students find a room to work,
which at UCL is not an easy task.

This repo is split into different folders which are separate components of our
system.




## Server

In `roomie-server`, you'll find a NodeJS/Express/MongoDB application. It acts
like an API to store data into a Mongo database and retrieve data. The app
would be deployed onto the cloud.

### Uses & Examples

Assuming the app has been deployed, you can make use of these endpoints

#### Inserting Data

The Mongo schema assumes a room is a collection, identified by a "room name".

You need to a send a HTTP POST request to: `/insert/roomdata`

The POST request should have the following data.

| Field | Type | Comments |
|-------|------|----------|
| room  | String| Unique Identifier, can be agreed upon later |
| heat  | Int | |
| noise | Int | |
| light | Int | |
| people | Int |  |

This server should handle the rest! All records are
auto timestamped when they are created

#### Retrieving Data

### Setup & Development

You need to install Node and npm.

```shell
cd roomie-server
npm install
```
You may have to install other dependencies (which I'll update in a bit!)

To start the server, run `npm start` which will start the Express application.

You also need to start the MongdoDB .. using ... [ to be added]

## Pi with SensorTag

_not fully finished, but will be very soon!_

In `pi-sensor`, you'll find code to set up the environment for the Pi. You'll have to run it on a Pi to set it up.

Credits to IanHarvey for his library which can be found [here](https://github.com/IanHarvey/bluepy)

To set up the library on the Pi, open terminal and run:

```shell
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip install bluepy
```

Once that's setup, go into `/pi-sensor/` and run `python get_data.py`

This Python script can do several things and has several modes which can be activated using flags.

Single Data Retrieval -- given an address of a SensorTag, it'll show the data associated with it.

Multiple Sensor Tag -- You have to have a list of addresses and know which tag is which. The script will poll it periodically and show the data for each of them

Send to server -- will post this to a server online s
