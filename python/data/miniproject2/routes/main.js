const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../../.env" });
const axios = require('axios')
const path = require('path');

var connection = new mysql({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
});

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/hello', (req, res) => {
    res.sendFile('layout.png',{ root: 'public' })
})

app.get('/', function (req, res) {
    res.sendFile("public/index.html")
})

app.get('/getParkdata', (req, res) => {
    const sigudong = req.query.sigudong;
    axios
        .get('http://192.168.1.76:3000/getParkdata',{ params: { sigudong }})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/makethree', (req, res) => {
    axios
        .get('http://192.168.1.76:3000/getthree_gudata')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/getsearchedareadata', (req, res) => {
    const sigudong = req.query.sigudong;
    axios
        .get('http://192.168.1.76:3000/getsearchedareadata',{ params: { sigudong }})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            if (response.data > 0) {
                template(response.data, res, sigudong)
            }
            console.log(response.data)
            // res.sendFile('index.html', { root: 'public' });
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/getmorethantwomonthadata', (req, res) => {
    const sigudong = req.query.sigudong;
    axios
        .get('http://192.168.1.76:3000/getmorethantwomonthadata',{ params: { sigudong }})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            if (response.data > 0) {
                template(response.data, res, sigudong)
            }
            console.log(response.data)
            // res.sendFile('index.html', { root: 'public' });
            console.log(response.data)

        })
        .catch(error => {
            console.log(error)
        })
})



app.get('/admindelete', (req, res) => {
    axios
        .get('http://192.168.1.76:3000/admindelete')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/shownoise', (req, res) => {
    axios
        .get('http://192.168.1.76:3000/jserver_to_mongo')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

function template(response, res, sigudong) {
  res.writeHead(200);
  var template = `
  
    <!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Information</title>
    <style>
        .container {
    display: grid;
    grid-template-columns: 1fr 4fr 1fr; /* Three equal columns */
    grid-template-rows: 1fr; /* Single row */
    grid-gap: 10px; /* Gap between grid items */
    height: 100px; /* Optional: Set a fixed height for the container */
    }

    .top-left,
    .top-right,
    .center-top,
    .center-bottom {
    border: 1px solid black;
    // padding: 10px;
    }

    .center-container {
    display: grid;
    grid-template-columns: 1fr; /* Single column within center-container */
    grid-template-rows: auto auto; /* Two auto-sized rows within center-container */
    grid-gap: 10px; /* Gap between grid items */
    }

    .center-top {
    grid-row: 1 / 2; /* Position in grid: row-start / row-end */
    }

    .center-bottom {
    grid-row: 2 / 3;
    }

    .top-left {
    grid-column: 1 / 2; /* Position in grid: column-start / column-end */

    }

    .center-container {
    grid-column: 2 / 3;
    }

    .top-right {
    grid-column: 3 / 4;
    
    }

</style>
  </head>
  <body>
  
  <div class="container">
  <div class="top-left"><button type='button' onclick='moveto()'>2개월 내 준공 예정공사 제외하기</button></div>
  <div class="center-container">
    <div class="center-top">`
      template += `${sigudong}의 현재 공사중인 곳은 총 ${response}곳입니다. </div>
    <div class="center-bottom">Center Bottom</div>
  </div>
  <div class="top-right">Top Right</div>
</div>
    <hr />
    <iframe src="result.html" frameborder="0" width="100%" height="810"></iframe>
    
    <script>
    function moveto() {
    document.location.href="http://192.168.1.76:8000/getmorethantwomonthadata?sigudong=${sigudong}"
    }
    
    </script>
  </body>
</html>
    `;
  res.end(template);
}

module.exports = app;