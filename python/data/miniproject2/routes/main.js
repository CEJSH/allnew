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
    res.send('Hello World~!!')
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
            console.log(response)
            res.sendFile('index.html', { root: 'public' });
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
            console.log(response.data)
            res.send(response.data)
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

module.exports = app;