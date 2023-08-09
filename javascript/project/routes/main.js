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

const AWS = require('aws-sdk');

AWS.config.update({
    region: 'ap-northeast-2', // Replace with your desired AWS region
    accessKeyId: process.env.aws_access_key_id,
    secretAccessKey: process.env.aws_secret_access_key
});

const dynamodb = new AWS.DynamoDB();




app.get('/', function (req, res) {
    res.sendFile("../public/index.html")
})

app.get('/copple', function (req, res) {
    res.sendFile("main.html", { root: 'public' })
})

app.post('/server-endpoint', (req, res) => {
    const clientData = JSON.parse(req.body.data);
    console.log(clientData)
    // Now you can process the client data on the server as needed
    console.log('Received data from client:', clientData);
    const queryParams = {
        TableName: 'Todo',
        KeyConditionExpression: 'UserId = :value',
        ExpressionAttributeValues: {
            ':value': { S: clientData } // Use the value you want to query
        }
    };

    dynamodb.query(queryParams, (err, data) => {
        if (err) {
            console.error('Error querying data:', err);
        } else {
            console.log('Queried data:', data.Items);
        }
    });
    res.sendStatus(200); // Respond with a success status
});

module.exports = app;
