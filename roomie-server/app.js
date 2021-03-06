var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');

var viewDB = require('./routes/viewDB');
var insertDB = require('./routes/insertDB');
var insertFakeData = require('./routes/insertFakeData');
var registerMac = require('./routes/registerMac');
var dashboard = require('./routes/dashboard');
var findSomeone = require('./routes/findSomeone');
var findRoom = require('./routes/findRoom');


var cors = require('cors')
var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');


app.use(cors())

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');


app.use('/', index);
app.use('/viewDB', viewDB);
app.use('/insertDB', insertDB);
app.use('/registerMac', registerMac);
app.use('/dashboard', dashboard);
app.use('/insertFakeData', insertFakeData);
app.use('/findPerson', findSomeone);
app.use('/findRoom', findRoom);


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
