from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse
import boto3

app = FastAPI()

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table_name = 'Goal'
table = dynamodb.Table(table_name)


# 목표등록 라우트
@app.post("/goalUp")
def signup(user_id: str = Body(...), title: str = Body(...), detail: str = Body(...)):

    item = {
        'UserId': user_id,
        'Title': title,
        'Detail': detail
    }
    table.put_item(Item=item)

    return {"message": "목표가 성공적으로 등록되었습니다!"}

# 목표 등록 폼을 제공하는 라우트


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("public/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
