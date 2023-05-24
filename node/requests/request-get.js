const https = require('https');
const express = require('express');
const request = require('request');
const CircularJSON = require('circular-json');
const app = express();

app.get('/', (req, res) => {
    res.send("Web Sever started...");
})

app.get('/hello', (req, res) => {
    res.send("Hello World - Choi");
})

let option = "http://192.168.1.76:3000/getthree_gudata"
app.get("/three", function (req, res) {
    request(option, { json: true }, (err, result, body) => {
        if (err) { return console.log(err) }
        res.send(CircularJSON.stringify(body))
    })
})

const data = JSON.stringify({ todo: 'Buy the milk - Choi' })
app.get("/data", function (req, res) {
    res.send(data);
})

rdata = "http://192.168.1.76:8000/data"
app.get("/rdata", function (req, res) {
    request(option, { json: true }, (err, result, body) => {
        if (err) { return console.log(err) }
        res.send(CircularJSON.stringify(body))
    })
})

app.listen(8000, function () {
    console.log('8000 Port : Server Started....');
})