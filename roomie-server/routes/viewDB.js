var express = require('express');
var router = express.Router();

var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var url = 'mongodb://localhost:27017/roomsdb';


var roomInfo = function(db, name, callback) {
   var cursor = db.collection(name).find( );
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


/* GET users listing. */
router.get('/roomdata/:name', function(req, res, next) {
  MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    roomInfo(db, req.params.name, function(data) {
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
