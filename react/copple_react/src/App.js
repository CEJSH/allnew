import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Plan from "./routes/Plan";
import Goal from "./routes/Goal";
import Todo from "./routes/Todo";
import Calendar from "./routes/Calendar";
import shortId from "shortid";
const AWS = require('aws-sdk');


AWS.config.update({
  region: 'ap-northeast-2',
  apiVersion: 'latest',
  accessKeyId: process.env.REACT_APP_ACCESS_KEY_ID,
  secretAccessKey: process.env.REACT_APP_SECRET_ACCESS_KEY,
})


const dynamodb = new AWS.DynamoDB.DocumentClient({convertEmptyValues: true});

function App() {

  const saveGoalDataHandler = (enteredGoalData) => {
    const goal_params = {
      TableName: 'Goal',
      Item: {
        'UserId': shortId.generate(),
        'Title': enteredGoalData.title,
        'Detail': enteredGoalData.content,
        'Date' : enteredGoalData.date,
        'Adress': enteredGoalData.adress,
        'Image' : enteredGoalData.image
      }
    };

    console.log(goal_params)
    dynamodb.put(goal_params, (error) => {
      if (error) {
        console.error('Error putting item:', error);

      } else {
        console.log({ message: '목표가 성공적으로 등록되었습니다!' });
      }
    })

  }

  const savePlanDataHandler = (enteredPlanData) => {
    const plan_params = {
      TableName: 'Event',
      Item: {
        'UserId': Math.random().toString(),
        'Title': enteredPlanData.title,
        'Goal': enteredPlanData.goal,
        'Detail': enteredPlanData.content,
        'Adress': enteredPlanData.adress
      
      }
    };
    console.log(plan_params)
    dynamodb.put(plan_params, (error) => {
      if (error) {
        console.error('Error putting item:', error);

      } else {
        console.log({ message: '목표가 성공적으로 등록되었습니다!' });
      }
    });
  }

  const saveTodoDataHandler = (enteredTodoData) => {
    const todo_params = {
      TableName: 'Todo',
      Item: {
        'UserId': Math.random().toString(),
        'Title': enteredTodoData.title,
        'Goal': enteredTodoData.goal,
        'Detail': enteredTodoData.content,
        'Adress': enteredTodoData.adress
      
      }
    };
    console.log(todo_params)
    dynamodb.put(todo_params, (error) => {
      if (error) {
        console.error('Error putting item:', error);

      } else {
        console.log({ message: '목표가 성공적으로 등록되었습니다!' });
      }
    });
  }

  return (
    <Router>
      <Switch>
        <Route path="/calendar">
          <Calendar />
        </Route>
        <Route path="/todo">
          <Todo onSaveTodoData={saveTodoDataHandler}/>
        </Route>
        <Route path="/plan">
          <Plan onSavePlanData={savePlanDataHandler} />
        </Route>
        <Route path="/goal">
          <Goal onSaveGoalData={saveGoalDataHandler} />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
