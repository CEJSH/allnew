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
            if (response.data[1] > 0) {
                template(response.data, res, sigudong)
            }
            console.log(response.data)
            // res.sendFile('index.html', { root: 'public' });
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/getmorethantwomonthdata', (req, res) => {
    const sigudong = req.query.sigudong;
    axios
        .get('http://192.168.1.76:3000/getmorethantwomonthdata',{ params: { sigudong }})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            if (response.data[1] > 0) {
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

// app.get('/shownoise', (req, res) => {
//     axios
//         .get('http://192.168.1.76:3000/jserver_to_mongo')
//         .then(response => {
//             console.log(`statusCode : ${response.status}`)
//             console.log(response.data)
//             res.send(response.data)
//         })
//         .catch(error => {
//             console.log(error)
//         })
// })

function template(responsedata, res, sigudong) {
  res.writeHead(200);
  var template = `
  
    <!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Information</title>
    <style>
    * {
    box-sizing: border-box
    }   
        .container {
    display: grid;
    grid-template-columns: 1fr 4fr 1fr; /* Three equal columns */
    grid-template-rows: 1fr; /* Single row */
    grid-gap: 10px; /* Gap between grid items */
    height: 100px; /* Optional: Set a fixed height for the container */
    background-color: #f2f2f2;
    border: 1px solid #ccc;
    border-radius: 4px;
    }

    .top-left,
    .top-right,
    .center-top,
    .center-bottom {
    border: 1px solid black;
    // padding: 10px;
    }

    .top-left button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    height : 100%;
    font-size:20px;
    }

    .top-left button:hover {
    background-color: #45a049;    
    }   
    #value {
        font-weight : bold;
    }
    
    
    .center-container {
    display: grid;
    grid-template-columns: 1fr; /* Single column within center-container */
    grid-template-rows: auto auto; /* Two auto-sized rows within center-container */
    grid-gap: 10px; /* Gap between grid items */
    }

    .center-top {
    grid-row: 1 / 2; /* Position in grid: row-start / row-end */
    padding-left : 15px;
    }

    .center-bottom {
    grid-row: 2 / 4;
    color: #888;
    padding-left : 15px;
    font-color : balck;
    }

    .top-left {
    grid-column: 1 / 2; /* Position in grid: column-start / column-end */

    }

    .center-container {
    grid-column: 2 / 4;
    }

    // .top-right {
    // grid-column: 3 / 4;
    
    // }

</style>
  </head>
  <body>
  
  <div class="container">
  <div class="top-left"><button type='button' onclick='moveto()'>2개월 내 준공 예정공사<br> 제외하기</button></div>
  <div class="center-container">
    <div class="center-top">`
      template += `${responsedata[0]} ${sigudong}의 현재 공사중인 곳은 총 <span id='value'>${responsedata[1]}</span>곳입니다. </div>
    <div class="center-bottom">`
    template += ` ${responsedata[0]} 의 구별 평균 공원 수는 <span id='value'>${responsedata[2][1]}</span>개 이며, 1인당 생활권 공원면적은<span id='value'> ${responsedata[2][0]}㎡</span>이며,
     서울시 25개구 중 <span id='value'>${responsedata[2][2]}</span>위입니다.</div>
  </div>

</div>
    <hr />
    <iframe src="result.html" frameborder="0" width="100%" height="810"></iframe>
    
    <script>
    function moveto() {
    document.location.href="http://192.168.1.76:8000/getmorethantwomonthdata?sigudong=${sigudong}"
    }
    
    </script>
  </body>
</html>
    `;
  res.end(template);
}

module.exports = app;