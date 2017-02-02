var moment = require('moment');

var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var url = 'mongodb://localhost:27017/roomsdb';


var insertDocument = function(db, callback) {
   db.collection('rooms').insertOne(
     {
       roomName: "exampleA",
       data: [
         {
           timeStamp: moment().format(),
           heat: 5 ,
           noise: 5,
           lighting: 5 ,
           peopleCount: 5
         }
       ]
     }, function(err, result) {
    assert.equal(err, null);
    console.log("Inserted a document into the rooms collection.");
    callback();
  });
};


MongoClient.connect(url, function(err, db) {
  assert.equal(null, err);
  insertDocument(db, function() {
      db.close();
  });
});
