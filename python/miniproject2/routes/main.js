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



app.get('/', function (req, res) {
    res.sendFile("public/index.html")
})

app.get('/chart', function (req, res) {
    res.sendFile('chartmore.png', { root: '.' });
})
app.get("/show_graph/:gu", (req, res) => {
    const { gu } = req.params;

    res.sendFile(`${gu}.png`, { root: 'public' })

});

app.get("/mk_graph", (req, res) => {
    axios
        .get('http://192.168.1.76:3000/get_topfive_noise')
        .then(res => {
            console.log(`statusCode : ${res.status}`)
            console.log(res)
        })
        .catch(error => {
            console.log(error)
        })
});


//검색시 자동으로 json서버에 올려진 공원데이터를받아와 정보를 띄워줍니다.
//when the input submitted, show data uploaded in json-server in html 
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
//각각 5개 구별 API에서 데이터를 받아와 mongodb에 생성
//generate new data from each 5 different api of autonomous district 
app.get('/makeFive', (req, res) => {
    axios
        .get('http://192.168.1.76:3000/getfive_gudata')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.redirect('/')
        })
        .catch(error => {
            console.log(error)
        })
})
//입력받은 내용으로 검색
//search area by the input and make circles and map by the area information about noise and construction
app.get('/getSearchedAreadata', (req, res) => {
    const sigudong = req.query.sigudong;
    axios
        .get('http://192.168.1.76:3000/getSearchedAreadata',{ params: { sigudong }})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            if (response.data[1] > 0) {
                template(response.data, res, sigudong);
                console.log('getresearched');
            }
            else {
                res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'})
                res.write("<script>alert('어디로 가야하조는 강남구, 관악구, 금천구, 영등포구, 용산구만 조회 가능합니다!')</script>");
                res.write("<script>window.location=\"/\"</script>");
            }
            console.log(response.data)
            // res.sendFile('index.html', { root: 'public' });
        })
        .catch(error => {
            console.log(error)
        })
})
app.get('/other',(req,res)=>{
    res.sendFile('other.html', { root: 'public' })

})
//2개월 이상 지속되는 공사를 보고싶을 때
//search area by the input and make circles and map by the area information about noise and construction continuing over 2 months from now on
app.get('/getmorethantwomonthdata', (req, res) => {
    const sigudong = req.query.sigudong;
    axios
        .get('http://192.168.1.76:3000/getmorethantwomonthdata',{ params: { sigudong }})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            if (response.data[1] > 0) {
                template(response.data, res, sigudong)
                console.log('here')
            }
        })
        .catch(error => {
            console.log(error)
        })
})


// 몽고DB에 든 데이터를 전부 삭제
// delete all the construction data in mongoDB
app.get('/admindelete', (req, res) => {
    axios
        .get('http://192.168.1.76:3000/admindelete')
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response.data)
            res.redirect('/')
        })
        .catch(error => {
            console.log(error)
        })
  
})
// 지원's 서버 데이터를 내 몽고로 이동
// From jiwon's json server bring noise data into my mongoDB
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
     border: none
    }   
        .container {
    display: grid;
    grid-template-columns: 1fr 4fr 1fr; /* Three equal columns */
    grid-template-rows: 1fr; /* Single row */
    grid-gap: 10px; /* Gap between grid items */
    height: 100px; /* Optional: Set a fixed height for the container */
    background-color: #f2f2f2;
    border: none;
    border-radius: 4px;
    }

    .top-left,
    .top-right,
    .center-top,
    .center-bottom {
    border: none;
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
        .top-right button {
        float: right;
        width : 120px;
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
    padding : 5px;
    }

    .center-bottom {
    grid-row: 2 / 4;
    color: #888;
    padding : 5px;
    font-color : balck;
    }

    .top-left {
    grid-column: 1 / 2; /* Position in grid: column-start / column-end */

    }

    .center-container {
    grid-column: 2 / 3;
    }

    .top-right {
    grid-column: 3 / 4;
    font-size:20px;
    }
    .top-right {
  position: absolute;
  top: 0;
  right: 0;
}

button {
  padding: 10px ;

  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

button:active {
  background-color: #3e8e41;
}

</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script>
        window.onload = function setInnerHTML() {
            const element = document.getElementById('input_frame');
            element.innerHTML += '<iframe src="result.html" frameborder="0" width="100%" height="810"></iframe>';
        }
        function loadingProcess() {
            openLoading();
            // 타이머를 이용해 로딩창 종료
            setTimeout(closeLoading, 50000);
        }
        // 로딩창 키는 함수
        function openLoading() {
            //화면 높이와 너비를 구합니다.
            let maskHeight = $(document).height();
            let maskWidth = window.document.body.clientWidth;
            //출력할 마스크를 설정해준다.
            let mask = "<div id='mask' style='position:absolute; z-index:9000; background-color:#000000; display:none; left:0; top:0;'></div>";
            // 로딩 이미지 주소 및 옵션
            let loadingImg = '';
            loadingImg += "<div id='loadingImg' style='position:absolute; top: calc(50% - (200px / 2)); width:100%; z-index:99999999;'>";
            loadingImg += " <img src='loading3.gif' style='position: relative; display: block; margin: 0px auto;'/>";
            loadingImg += "</div>";
            //레이어 추가
            $('body')
                .append(mask)
                .append(loadingImg)
            //마스크의 높이와 너비로 전체 화면을 채운다.
            $('#mask').css({
                'width': maskWidth,
                'height': maskHeight,
                'opacity': '0.3'
            });
            //마스크 표시
            $('#mask').show();
            //로딩 이미지 표시
            $('#loadingImg').show();
        }

        // 로딩창 끄는 함수
        function closeLoading() {
            $('#mask, #loadingImg').hide();
            $('#mask, #loadingImg').empty();
        }
        function load_mini(URL) {
            window.open(URL, "miniWin", "left=600,top=100,width=950,height=750");
        }
        function load_full(URL) {
            window.open(URL, "fullWin");
        }
    </script>
  </head>
  <body>
  
  <div class="container">
  <div class="top-left"><button type='button' onclick='loadingProcess();moveto()'>2개월 내 준공 예정공사<br> 제외하기</button></div>
  <div class="center-container">
    <div class="center-top">`
      template += `${responsedata[0]} ${sigudong}의 현재 공사중인 곳은 총 <span id='value'>${responsedata[1]}</span>곳입니다. </div>
    <div class="center-bottom">`
    template += ` ${responsedata[0]} 의 구별 평균 공원 수는 <span id='value'>${responsedata[2][1]}</span>개 이며, 1인당 생활권 공원면적은<span id='value'> ${responsedata[2][0]}㎡</span>이며,
     서울시 25개구 중 <span id='value'>${responsedata[2][2]}</span>위입니다.</div>
  </div>
<div class='top-right'><button onclick="load_mini('/show_graph/강남구')">강남구 TOP5</button>
    <button onclick="load_mini('/show_graph/금천구')">금천구 TOP5</button><br>
    <button onclick="load_mini('/show_graph/영등포구')">영등포구 TOP5</button>
    <button onclick="load_mini('/show_graph/관악구')">관악구 TOP5</button><br>
    <button onclick="load_mini('/show_graph/용산구')">용산구 TOP5</button>
    <button onclick="load_mini('/chart')">공사 건수 Top10</button></div>
</div>
    <hr />
    <div id="input_frame"></div>

    
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
{/* <iframe src="result.html" frameborder="0" width="100%" height="810"></iframe> */}
module.exports = app;