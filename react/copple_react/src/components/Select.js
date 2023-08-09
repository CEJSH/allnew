import React, { useState, useRef, useEffect } from "react";
import Select from "react-select";
const AWS = require('aws-sdk');

AWS.config.update({
    region: 'ap-northeast-2',
    apiVersion: 'latest',
    accessKeyId: process.env.REACT_APP_ACCESS_KEY_ID,
    secretAccessKey: process.env.REACT_APP_SECRET_ACCESS_KEY,
  })

const dynamodb = new AWS.DynamoDB.DocumentClient({ convertEmptyValues: true });


const Selectop = (props) => {
    const [selectValue, setSelectValue] = useState('')
    const selectInputRef = useRef(null);
    const [options, setOptions] = useState([]);

    function fetchDataFromDynamoDB() {
        const objectToArray = obj => Object.entries(obj)
        
        return new Promise((resolve, reject) => {
            dynamodb.scan({
                TableName: 'Goal',
            }, (err, data) => {
                if (err) {
                    console.error('Error fetching data from DynamoDB:', err);
                    reject(err);
                } else {
                    resolve(data.Items);
                    return objectToArray(data.Items);
                }
            }); 
        });
    }
    
     async function getScannedGoals() {
  
        try {
            const items =  await fetchDataFromDynamoDB();  
     
        
            const titles = items.map(item => ({
                value: item.Title,
                label: item.Title
            }));
            return titles;
        } catch (error) {
            console.error('An error occurred:', error);
            // You might want to rethrow the error here if needed
            throw error;
        }
    }
    

    const dataget = async function fetchDataAndProcess () {
        try {
            const titles = await getScannedGoals();
            // const data = JSON.stringify(titles);
            setOptions(titles);
            return titles
        } catch (error) {
            console.error('An error occurred:', error);
            throw error; // Re-throw the error to be handled at a higher level
        }
    }

    useEffect(() => {
        dataget()
        }
    , []);

   
    const onClearSelect = () => {
        if (selectInputRef.current) {
            selectInputRef.current.clearValue();
        }
    }
    props.onSelectedData(selectValue)

    return (
        <div>
            <Select
                ref={selectInputRef}
                onChange={(e) => {
                    if (e) {
                        setSelectValue(e.value);
                    } else {
                        setSelectValue("");
                    }
                }}
                options={options}
                
                placeholder="목표를 선택하세요."
            />
            {/* <button onClick={() => onClearSelect()}>
                초기화
            </button> */}
        </div>
    )
}
export default Selectop;