var express = require('express');
var router = express.Router();

var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var url = 'mongodb://localhost:27017/roomsdb';
var moment = require('moment');


var insertDocument = function(db, data, callback) {
   console.log(String(data['roomName']));
   db.collection( String(data['roomName']) ).insertOne(
     {
       data: [
         {
           timeStamp: moment().format(),
           heat: data['heat'],
           noise: data['noise'],
           lighting: data['lighting'],
           peopleCount: data['peopleCount']
         }
       ]
     }, function(err, result) {
    assert.equal(err, null);
    console.log("Inserted some data for a room.");
    callback();
  });
};

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
    });
  });
});


module.exports = router;
