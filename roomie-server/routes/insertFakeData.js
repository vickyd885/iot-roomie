var express = require('express');
var router = express.Router();

var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var url = 'mongodb://localhost:27017/roomsdb';

/*
UNITS USED
- temperature: celsius
- ligh levels: lux
- noise: db

1 lux = 1 lumen / sq meter = 0.0001 phot = 0.0929 foot candle (ftcd, fcd) 
1 phot = 1 lumen / sq centimeter = 10000 lumens / sq meter = 10000 lux
1 foot candle (ftcd, fcd)  = 1 lumen / sq ft = 10.752 lux
one foot candle = one lumen of light density per square foot

                         (ftcd) (lux)
Sunlight                 10000 107527
Full Daylight            1000  10752
Overcast Day             100 1075
Very Dark Day            10  107
Twilight                 1 10.8
Deep Twilight            0.1 1.08
Full Moon                0.01  0.108
Quarter Moon             0.001 0.0108
Starlight                0.0001  0.0011
Overcast Night           0.00001 0.0001

*/

var fakeData = function () {
    var arr = [];
    var data = {
    "roomName": 'Room 1.05',
    "timeStamp": new Date("2017-03-02 16:15:10"),
    "heat": 25,
    "noise": 40,
    "lighting": 18,
    "peopleCount": 19
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.06',
      "timeStamp": new Date("2017-03-02 15:15:10"),
      "heat": 30,
      "noise": 60,
      "lighting": 250,
      "peopleCount": 19
    }
    arr.push(data);

    data = {
    "roomName": 'Room 1.07',
    "timeStamp": new Date("2017-03-02 16:15:10"),
    "heat": 20,
    "noise": 60,
    "lighting": 300,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.08',
      "timeStamp": new Date("2017-03-02 15:15:10"),
      "heat": 15,
      "noise": 110,
      "lighting": 200,
      "peopleCount": 1
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.01',
    "timeStamp": new Date("2017-03-02 16:15:10"),
    "heat": 22,
    "noise": 100,
    "lighting": 170,
    "peopleCount": 10
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.02',
      "timeStamp": new Date("2017-03-02 15:15:10"),
      "heat": 23,
      "noise": 90,
      "lighting": 250,
      "peopleCount": 11
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.03',
    "timeStamp": new Date("2017-03-02 16:15:10"),
    "heat": 24,
    "noise": 80,
    "lighting": 270,
    "peopleCount": 7
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.04',
      "timeStamp": new Date("2017-03-02 15:15:10"),
      "heat": 25,
      "noise": 75,
      "lighting": 200,
      "peopleCount": 15
    }
    arr.push(data);

    var data = {
    "roomName": 'Room 1.05',
    "timeStamp": new Date("2017-03-02 17:15:10"),
    "heat": 26,
    "noise": 50,
    "lighting": 150,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.06',
      "timeStamp": new Date("2017-03-02 17:15:10"),
      "heat": 25,
      "noise": 70,
      "lighting": 200,
      "peopleCount": 7
    }
    arr.push(data);

    data = {
    "roomName": 'Room 1.07',
    "timeStamp": new Date("2017-03-02 17:15:10"),
    "heat": 22,
    "noise": 70,
    "lighting": 250,
    "peopleCount": 3
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.08',
      "timeStamp": new Date("2017-03-02 17:15:10"),
      "heat": 15,
      "noise": 100,
      "lighting": 180,
      "peopleCount": 3
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.01',
    "timeStamp": new Date("2017-03-02 17:15:10"),
    "heat": 12,
    "noise": 150,
    "lighting": 150,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.02',
      "timeStamp": new Date("2017-03-02 17:15:10"),
      "heat": 25,
      "noise": 70,
      "lighting": 200,
      "peopleCount": 5
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.03',
    "timeStamp": new Date("2017-03-02 17:15:10"),
    "heat": 24,
    "noise": 100,
    "lighting": 200,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.04',
      "timeStamp": new Date("2017-03-02 17:15:10"),
      "heat": 22,
      "noise": 100,
      "lighting": 220,
      "peopleCount": 3
    }
    arr.push(data);

    data = {
    "roomName": 'Room 1.05',
    "timeStamp": new Date("2017-03-03 17:15:10"),
    "heat": 26,
    "noise": 50,
    "lighting": 150,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.06',
      "timeStamp": new Date("2017-03-03 17:15:10"),
      "heat": 25,
      "noise": 70,
      "lighting": 200,
      "peopleCount": 7
    }

    data = {
    "roomName": 'Room 1.07',
    "timeStamp": new Date("2017-03-03 17:15:10"),
    "heat": 22,
    "noise": 70,
    "lighting": 250,
    "peopleCount": 3
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.08',
      "timeStamp": new Date("2017-03-03 17:15:10"),
      "heat": 15,
      "noise": 100,
      "lighting": 180,
      "peopleCount": 3
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.01',
    "timeStamp": new Date("2017-03-03 17:15:10"),
    "heat": 12,
    "noise": 150,
    "lighting": 150,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.02',
      "timeStamp": new Date("2017-03-03 17:15:10"),
      "heat": 25,
      "noise": 70,
      "lighting": 200,
      "peopleCount": 5
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.03',
    "timeStamp": new Date("2017-03-03 17:15:10"),
    "heat": 20,
    "noise": 150,
    "lighting": 180,
    "peopleCount": 7
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.04',
      "timeStamp": new Date("2017-03-03 17:15:10"),
      "heat": 20,
      "noise": 100,
      "lighting": 200,
      "peopleCount": 5
    }
    arr.push(data);

    data = {
    "roomName": 'Room 1.05',
    "timeStamp": new Date("2017-03-03 18:15:10"),
    "heat": 28,
    "noise": 40,
    "lighting": 200,
    "peopleCount": 7
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.06',
      "timeStamp": new Date("2017-03-03 18:15:10"),
      "heat": 30,
      "noise": 80,
      "lighting": 110,
      "peopleCount": 7
    }
    arr.push(data);

    data = {
    "roomName": 'Room 1.07',
    "timeStamp": new Date("2017-03-03 18:15:10"),
    "heat": 20,
    "noise": 80,
    "lighting": 300,
    "peopleCount": 5
    }
    arr.push(data);

    data = {
      "roomName": 'Room 1.08',
      "timeStamp": new Date("2017-03-03 18:15:10"),
      "heat": 15,
      "noise": 110,
      "lighting": 200,
      "peopleCount": 5
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.01',
    "timeStamp": new Date("2017-03-03 18:15:10"),
    "heat": 15,
    "noise": 200,
    "lighting": 200,
    "peopleCount": 3
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.02',
      "timeStamp": new Date("2017-03-03 18:15:10"),
      "heat": 20,
      "noise": 80,
      "lighting": 120,
      "peopleCount": 10
    }
    arr.push(data);

    data = {
    "roomName": 'Room 2.03',
    "timeStamp": new Date("2017-03-03 18:15:10"),
    "heat": 20,
    "noise": 110,
    "lighting": 170,
    "peopleCount": 7
    }
    arr.push(data);

    data = {
      "roomName": 'Room 2.04',
      "timeStamp": new Date("2017-03-03 18:15:10"),
      "heat": 25,
      "noise": 85,
      "lighting": 200,
      "peopleCount": 5
    }
    arr.push(data);

    return arr;
}
var insertDocument = function(db, data, callback) {
   console.log(String(data['roomName']));
   db.collection( String(data['roomName']) ).insertOne(
     {
       data: [
         {
           timeStamp: data['timeStamp'],
           heat: data['heat'],
           noise: data['noise'],
           lighting: data['lighting'],
           peopleCount: data['peopleCount']
         }
       ]
     }, function(err, result) {
    assert.equal(err, null);
    callback(); 
  });
};


router.post('/roomdata', function(req, res, next) {

  var arr = fakeData();
  MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);

    arr.forEach(function(value) {
      console.log(value);
        insertDocument(db, value, function() {
        db.close();
      }); 
    });
    res.send("Request sent!");
  });
});


module.exports = router;
