const createError = require('http-errors');
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const layouts = require("express-ejs-layouts");
const pw_auth_router = require('./routes/pwauth')
const toDoRouter = require('./routes/todo');
const teamRouter = require('./routes/team');
const zachRouter = require('./routes/zach');
const christinaRouter = require('./routes/christina');
const andyRouter = require('./routes/andy');
const indexRouter = require('./routes/index');
const weatherRouter = require('./routes/weather');

const User = require('./models/User');

/* **************************************** */
/*  Connecting to a Mongo Database Server   */
/* **************************************** */
const mongodb_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/pwdemo';
console.log('MONGODB_URI=',process.env.MONGODB_URI);


const mongoose = require( 'mongoose' );

mongoose.connect( mongodb_URI);

const db = mongoose.connection;


db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log("we are connected!!!")
});



/* **************************************** */
/* Enable sessions and storing session data in the database */
/* **************************************** */
const session = require("express-session"); // to handle sessions using cookies 
var MongoDBStore = require('connect-mongodb-session')(session);

const store = new MongoDBStore({
  uri: mongodb_URI,
  collection: 'mySessions'
});

// Catch errors                                                                      
store.on('error', function(error) {
  console.log(error);
});


/* **************************************** */
/*  middleware to make sure a user is logged in */
/* **************************************** */
function isLoggedIn(req, res, next) {
  "if they are logged in, continue; otherwise redirect to /login "
  if (res.locals.loggedIn) {
    next();
  } else {
    res.redirect("/login");
  }
}

/* **************************************** */
/* creating the app */
/* **************************************** */
var app = express();

app.use(session({
  secret: 'This is a secret',
  cookie: {
    maxAge: 1000 * 60 * 60 * 24 * 7 // 1 week                                        
  },
  store: store,
  // Boilerplate options, see:                                                       
  // * https://www.npmjs.com/package/express-session#resave                          
  // * https://www.npmjs.com/package/express-session#saveuninitialized               
  resave: true,
  saveUninitialized: true
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(pw_auth_router)

app.use(layouts);

// app.get('/', (req,res,next) => {
//   res.render('index');
// })

app.get('/', (req,res,next) => {
  res.render('index');
})

app.get('/about', 
  isLoggedIn,
  (req,res,next) => {
    res.render('about');
  }
)

const axios = require('axios')
app.get('/openai_demo',
async (req,res,next) => {
response =
await axios.post('http://gracehopper.cs-i.brandeis.edu:3500/openai',
{prompt:"how does the flu differ from covid?"})
res.json(response.data.choices[0].message.content)
})


app.get('/team', (req,res,next) => {
  res.render('team');
})

app.get('/zach', (req,res,next) => {
  res.render('zach');
})

app.get('/christina', (req,res,next) => {
  res.render('christina');
})

app.get('/andy', (req,res,next) => {
  res.render('andy');
})

app.get('/index', (req,res,next) => {
  res.render('index');
 
})

app.use(toDoRouter);
app.use(teamRouter);
app.use(indexRouter);
app.use(weatherRouter);
app.use(zachRouter);
app.use(christinaRouter);
app.use(andyRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
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
