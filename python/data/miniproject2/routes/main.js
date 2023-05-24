const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../../.env" });
const axios = require('axios')

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

app.get('/select', (req, res) => {
    const result = connection.query('select * from user');
    console.log(result);
    res.send(result);
})

app.get('/getsearchedareadata', (req, res) => {
    const params = {sigudong:'영등포 당산'};
    axios
        .get('http://192.168.1.76:3000/getsearchedareadata',{params})
        .then(response => {
            console.log(`statusCode : ${response.status}`)
            console.log(response)
            res.send(response.data)
        })
        .catch(error => {
            console.log(error)
        })
})

app.get('/getmorethantwomonthadata', (req, res) => {
    axios
        .get('http://192.168.1.76:3000/getmorethantwomonthadata')
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
        .get('http://192.168.1.158:3000/getmongo')
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