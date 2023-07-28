const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const AWS = require('aws-sdk');

AWS.config.update({ region: 'ap-northeast-2' });

const dynamodb = new AWS.DynamoDB.DocumentClient();
const table_name = 'Goal';

app.use(bodyParser.json());

// 목표등록 라우트
app.post('/goalUp', (req, res) => {
  const { user_id, title, detail } = req.body;

  const item = {
    UserId: user_id,
    Title: title,
    Detail: detail,
  };

  const params = {
    TableName: table_name,
    Item: item,
  };

  dynamodb.put(params, (error) => {
    if (error) {
      console.error('Error putting item:', error);
      res.status(500).json({ message: 'An error occurred while adding the goal.' });
    } else {
      res.json({ message: '목표가 성공적으로 등록되었습니다!' });
    }
  });
});

// 목표 등록 폼을 제공하는 라우트
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});