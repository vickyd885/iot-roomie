var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
  res.render('mac');
});


router.post('/save', function(req, res, next) {
  console.log(req.body.user);
  console.log(req.body.mac);
  res.send({'status':'complete'});
});

module.exports = router;
