const express = require('express');
const app = express.Router();
const mongoose = require('mongoose')
const async = require('async');
const pool = require("../config/pool");
const axios = require('axios');

var buySchema = mongoose.Schema({
    buyid: String,
    buyer: String,
    customerid: String,
    flight: String,
    flightdate: Date,
    amount: Number,
    buydate: Date,
    passengers: String,
    note: Boolean
}, {
    versionKey: false

})

var Buy = mongoose.model('buy', buySchema);

// mysql 
app.get('/login-page', function (req, res) {
    res.sendFile("/silvercastle/public/login.html")
})

app.get('/select', async function (req, res) {
    const [rows, fields] = await pool.query('SELECT * FROM customerTBL');
    let response = {
        'ok': true,
        'result': []
    }
    if (rows.length > 0) {
        response['result'] = rows
        res.send(JSON.stringify(response));
    } else {
        response['ok'] = false;
        res.send(JSON.stringify(response));
    }
})

app.get('/dupId', async (req, res) => {
    const id = req.query.id;
    if (id == null) {
        res.write("<script>alert('id를 입력하세요.')</script>");
        console.log("id 입력해")
        return;
    }
    const [rows, fields] = await pool.query('SELECT * FROM customerTBL where customerid= ?', [id]);
    let response = {
        'ok': true,
        'result': [],
        'service': "select"
    }
    if (rows.length > 0) {
        console.log("이미존재하는 아이디입니다.");
        response['result'] = rows
        res.send(JSON.stringify(response));
    }
})

// search id
app.get('/searchid', async (req, res) => {
    const email = req.query.email
    const phone = req.query.phone
    if (email == null && phone == null) {
        res.write("<script>alert('이메일과 전화번호를 입력하세요.')</script>");
        console.log("이메일 , 전화번호 입력해");
        return;
    } else if (email == null) {
        res.write("<script>alert('이메일을 입력하세요.')</script>");
        console.log("이메일 입력해");
        return;
    } else if (phone == null) {
        res.write("<script>alert('전화번호를 입력하세요.')</script>");
        console.log("전화번호 입력해");
        return;
    }
    const [rows, fields] = await pool.query('SELECT * FROM customerTBL where email = ? and phoneNumber = ?', [email, phone]);
    let response = {
        'ok': true,
        'result': [],
        'service': "select"
    } .
    console.log(rows);
    if (rows.length > 0) {
        response['result'] = rows;
        res.send(JSON.stringify(response))
    } else {
        response['ok'] = false;
        console.log("가입된 내역이 없는 이메일입니다.");
        res.send(JSON.stringify(response))
    }
})


app.post('/updatePw', async (req, res) => {
    const { id, phone, pw, pwCheak } = req.body
    if (id == null && phone == null) {
        res.write("<script>alert('아이디와 전화번호를 입력하세요.')</script>");
        console.log("아이디 , 전화번호 입력해");
        return;
    } else if (id == null) {
        res.write("<script>alert('아이디를 입력하세요.')</script>");
        console.log("아이디 입력해");
        return;
    } else if (phone == null) {
        res.write("<script>alert('전화번호를 입력하세요.')</script>");
        console.log("전화번호 입력해");
        return;
    } else if (pw == null) {
        res.write("<script>alert('수정할 비밀번호를 입력해주세요.')</script>");
        console.log(" 수정할 비밀 번호 입력해");
        return;
    }

    // console.log(id, phone);
    let [rows, fields] = await pool.query('SELECT * FROM customerTBL where customerid = ? and phoneNumber= ?', [id, phone]);
    let response = {
        'ok': true,
        'affectedRows': 0,
        'service': "update"
    }
    console.log(rows);
    if (rows.length > 0) {
        result = await pool.query('update customerTBL set passwd=? where customerId=? and phoneNumber=?', [pw, id, phone]);
        response['affectedRows'] += result[0].affectedRows
        console.log(response);
        res.send(JSON.stringify(response))
    } else {
        response['ok'] = false;
        res.send(JSON.stringify(response))
    }
})

app.post('/register', async (req, res) => {
    const userInfo = req.body;
    columns = ['id', 'pw', 'name', 'birth', 'phone', 'email', 'addr', 'pnum']
    for (let i = 0; i < columns.length; i++) {
        if (req.body[columns[i]] == '') {
            res.write("<script>alert('모든 항목을 입력해주세요.')</script>");
            return;
        }
    }
    const [rows, fields] = await pool.query("insert into customerTBL values (?,?,?,?,?,?,?,?)",
        [userInfo.id, userInfo.pw, userInfo.name, userInfo.birth,
        userInfo.phone, userInfo.email, userInfo.addr, userInfo.pnum]);
    console.log(rows);
    let response = {
        'ok': true,
        'result': [],
        'service': "insert"
    }
    if (rows) {
        response['result'] = userInfo
        res.send(JSON.stringify(response))
    } else {
        response['ok'] = false;
        res.send(JSON.stringify(response))
    }
})

app.post('/buytotal', async (req, res) => {
    let buys = req.body.buys
    let response = {
        'ok': true,
        'affectRows': 0,
        'service': "insert"
    }
    for (let index = 0; index < buys.length; index++) {
        for (let i = 0; i < Object.keys(buys).length; i++) {
            if (buys[index][Object.keys(buys[index])[i]] == null && Object.keys(buys[index])[i] != 'id') {
                console.log(buys[index][Object.keys(buys[index])[i]])
                console.log("항목이 비어있습니다");
                return;
            }
        }
        let buydate = new Date(buys[index].buydate)
        buydate = buydate.getFullYear() + '-' + (buydate.getMonth() + 1) + '-' + buydate.getDate()
        let flightdate = new Date(buys[index].flightdate);
        flightdate = flightdate.getFullYear() + '-' + (flightdate.getMonth() + 1) + '-' + flightdate.getDate()

        const [rows, fields] = await pool.query("insert into buytotal values (NULL,?,?,?,?,?,?,?,?)",
            [buys[index].buyid, buys[index].buyer, buys[index].customerid, buys[index].flight, flightdate,
            buys[index].amount, buydate, buys[index].note]);
        console.log(rows);
        if (rows) response['affectRows'] += rows.affectedRows;
    }

    if (response['affectRows'] > 0) {
        res.send(JSON.stringify(response))
    } else {
        response['ok'] = false;
        res.send(JSON.stringify(response))
    }
})



app.post('/login', async (req, res) => {
    const { id, pw } = req.body;
    if (id == null && pw == null) {
        res.write("<script>alert('아이디와 비밀번호를 입력하세요.')</script>");
        console.log("아이디 , 비밀번호를 입력해");
        return;
    } else if (id == null) {
        res.write("<script>alert('아이디를 입력하세요.')</script>");
        console.log("아이디 입력해");
        return;
    } else if (pw == null) {
        res.write("<script>alert('비밀번호를 입력하세요.')</script>");
        console.log("비밀번호 입력해");
        return;
    }
    const [row, fields] = await pool.query('select * from customerTBL where customerid=? and passwd=?', [id, pw]);
    let response = {
        'ok': true,
        'result': [],
        'service': "select"
    }
    if (row.length === 0) {
        console.log("로그인 실패");
        res.write("<script>alert('로그인에 실패하였습니다.<br>아이디와 비밀번호를 확인해주세요')</script>");
        response['ok'] = false;
        res.send(JSON.stringify(response))
    }
    else {
        console.log(row);
        response['result'] = row;
        res.send(JSON.stringify(response));
        // if (id === 'root' || id === 'admin') {
        //     console.log(id + " => Administrator Logined");
        //     res.redirect('admin.html?id=' + id);
        // } else {
        //     console.log(id + " => User Logined");
        //     res.redirect('user.html?id=' + id);
        // }
    }
})

// mongodb
// buy collection insert
app.post('/buy', function (req, res, next) {
    const id = req.body.id
    const buyer = req.body.buyer
    const flight = req.body.flight
    const flightdate = req.body.flightdate;
    const amount = req.body.amount
    const passengers = req.body.passengers
    const note = req.body.note
    // date = new date(date)
    // 
    const buyid = "ZA" + flightdate + flight;
    // const buyId = "ZA" + date.getMonth() + date.getDate() + time + flight;
    console.log(buyid)
    let response = {
        'ok': true,
        'result': [],
        'service': "insert"
    }
    var buy = new Buy({
        'buyid': buyid, 'buyer': buyer, 'customerid': id, 'flight': flight,
        'flightdate': flightdate, 'amount': amount, "buydate": new Date(),
        'passengers': passengers, 'note': note
    });
    buy.save(function (err, silence) {
        if (err) {
            console.log("err");
            response['ok'] = false;
            res.send(JSON.stringify(response));
            return;
        }
        console.log("silence :", silence);
        response['result'] = silence
        res.send(JSON.stringify(response));
    })
})


// buylist find

app.post('/buylist', (req, res, next) => {
    const id = req.body.input

    let response = {
        'ok': true,
        'buylist': [],
        'service': "find"
    }

    Buy.find({ 'customerid': id }, (err, docs) => {
        if (err) {
            console.log("err");
            response['ok'] = false;
            console.log(JSON.stringify(response))
            res.send(JSON.stringify(response));
            return;
        }
        response['buylist'] = docs
        console.log(docs);
        res.send(JSON.stringify(response));
    })
})

// refund

app.post('/refund', function (req, res, next) {
    const id = req.body.id
    const buyid = req.body.buyid
    const flight = req.body.flight
    const amount = req.body.amount
    const flightdate = req.body.flightdate
    const passengers = req.body.passengers
    const buyer = req.body.buyer
    const note = req.body.note
    let response = {
        'ok': true,
        'result': [],
        'service': "insert"
    }
    var buy = new Buy({
        'buyid': buyid, 'buyer': buyer, 'customerid': id, 'flight': flight, 'buydate': new Date(), 'amount': amount,
        'flightdate': flightdate, 'passengers': passengers, 'note': note
    });
    buy.save(function (err, silence) {
        if (err) {
            console.log("err");
            response['ok'] = false;
            res.send(JSON.stringify(response));
            return;
        }
        // console.log("silence :", silence);
        response['result'] = silence
        res.send(JSON.stringify(response));
    })
})



app.post('/deleteMany', function (req, res, next) {
    var buyid = req.body.input;
    var buy = Buy.find({ 'buyId': buyid });
    buy.deleteMany(function (err) {
        if (err) {
            console.log('err');
            res.status(500).send('delete error');
            return;
        }
        res.status(200).send('Removed');
    })
    // user.deleteOne(function (err) {
    //     if (err) {
    //         console.log('err');
    //         res.status(500).send('delete error');
    //         return;
    //     }
    //     res.status(200).send('Removed');
    // })
})

app.get('/store-buytbl', (req, res) => {
    let result = ""
    Buy.find({ 'flightdate': { '$lte': new Date() } }, function (err, docs) {
        if (err) {
            console.log("err")
            res.write('{"ok":false, buys:' + err + 'service:');
        } else {
            axios
                .post('http://192.168.1.80:8000/buytotal', {
                    "buys": docs
                })
                .then((res) => {
                    console.log(`statusCode : ${res.status}`);
                    console.log(res.data)
                    result = JSON.stringify(res.data)
                    // console.log(res);
                })
                .catch(error => {
                    console.log(error);
                })
        }
    });
    res.send(result)
})

module.exports = app;