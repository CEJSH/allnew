const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path:"../../.env"});

var connection = new mysql ({
    host : process.env.host,
    user : process.env.user,
    password : process.env.password,
    database : process.env.database
});

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended:false }));
app.use(express.json());
app.use(express.urlencoded({ extended:true }));

app.get('/greeting', (req, res) => {
    res.send('회원 정보를 관리하세요~~!!!')
})

// request 1, query 0
app.get('/select', (req, res) => {
    const result = connection.query('select * from customer');
    console.log(result);
    res.send(result);
})

// request 1, query 0
//app.post('/select', (req, res) => {
 //   const result = connection.query('select * from user');
//    console.log(result);
 //   res.send(result);
//})

// request 1, query 1
app.get('/selectQuery', (req, res) => {
    const id = req.query.customerId;
    const result = connection.query("select * from customer where customerId=?", [id] );
    console.log(result);
    res.send(result);
})

// request 1, query 1
app.post('/selectQuery', (req, res) => {
    const id = req.body.id;
    const result = connection.query("select * from customer where customerId=?", [id] );
    console.log(result);
    res.send(result);
})

// request 1, query 1
app.post('/insert', (req, res) => {
    const { id, name, birthday, phone, address, pnum } = req.body;
    const result = connection.query("insert into customer values (?,?,?,?,?,?)", [id, name, birthday, phone, address, pnum] );
    console.log(req.body.name + "님의 정보를 성공적으로 등록하였습니다~!");
    res.send(req.body.name + "님의 정보를 성공적으로 등록하였습니다~!");
    //res.redirect('/selectQuery?userid=' + req.body.id);
})

app.post('/update', (req, res) => {
    const { id, name, birthday, phone, address, pnum } = req.body;
    const result = connection.query("update customer set customerName=?, phoneNumber=?, addr=?, pnum=? where customerId=?", [name, phone, address, pnum, id] );
    console.log(result);
    res.send(req.body.name + "님의 정보가 성공적으로 업데이트 되었습니다~!");
    //res.redirect('/selectQuery?userid=' + req.body.id);
})

app.post('/delete',(req , res)=> {
    const id =req.body.id;
    const result = connection.query("delete from customer where customerId=?", [id]);
    console.log(result);
    res.send(req.body.name + "님의 정보를 성공적으로 삭제하였습니다~!");
   //res.redirect('/select');
}
)

module.exports = app;