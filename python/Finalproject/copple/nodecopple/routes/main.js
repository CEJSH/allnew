const express = require('express');
const bodyParser = require('body-parser');
const env = require('dotenv').config({ path: "../../.env" });
const axios = require('axios')
const path = require('path');

const app = express()


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));



app.get('/', function (req, res) {
    res.sendFile("public/index.html")
})

app.get('/goalUp', function(req,res){
    const formData = req.
    axios
        .get('http://52.78.246.81:3000/goalUp',{params:  {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)}})
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
