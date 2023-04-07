const express = require('express');
const morgan = require('morgan');
const path = require('path');
const app = express();
const bodyParse = require('body-parser');
const cookiePase = require('body-parser');
const router = express.Router();

app.get('port', process.env.PORT || 8000)
app.use(morgan('dev'))
app.use(bodyPase.json())
app.use(bodyPase.urlencoded({extended:false}))
app.use(cookieParse.json())
app.use(express.static(path.join(__dirname, 'public')))

var main = require('./routes/main.js')
app.use('/', main)

app.listen(app.get('port'), () => {
    console.log('8000 Port : Server Started~!!');
})