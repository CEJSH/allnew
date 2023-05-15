onmessage = function (e) {
let num = parseInt(e.data.num);
let message;
for (i=2;i<num;i++){
    if (num % i == 0){
        message = "소수가 아닙니다~!";
        break;
} else{
    message = "소수입니다~!"
}}
postMessage(message);
}