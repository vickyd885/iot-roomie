var express = require('express');
var router = express.Router();
var moment = require('moment');
var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var url = 'mongodb://localhost:27017/roomsdb';


var roomInfo = function(db, name, time, callback) {
  var cursor;
  //  if(time){
  //     cursor = db.collection(name ).find({ created_at : {
  //      $gte: moment().subtract(2, 'months'),
  //      $lt: moment().format()
  //     }});
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


/* GET Room data by room name */
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

// get room data by name and date
router.get('/timedroomdata', function(req, res, next) {
  var time = req.query.time;
  var name = req.query.name;

  MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    roomInfo(db, name, time, function(data) {
        console.log("heard request for room: "+req.params.name);
        db.close();
        res.send(data);
    });
  });
});


router.get('/rooms', function(req, res, next) {
  MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    roomInfo(db, function(data) {
        db.close();
        res.send(data);
    });
  });
});




module.exports = router;
