const axious = require('axios');

axious
    .post('http://192.168.1.80:8000/todos', {
        todo : 'Buy the mailk'
    })
    .then(res=>{
        console.log(`statusCode : ${res.status}`)
        console.log(res.data)
    })
    .catch(error=> {
        console.log(error)
    })