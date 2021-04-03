import json 
import requests
import os
import weather_helper as wh

TOKEN = os.environ["TELEGRAM_TOKEN"]
api_url = f"https://api.telegram.org/bot{TOKEN}/"

def lambda_handler(event, context):
    chat_id = event['message']['chat']['id']
    params = {'chat_id': chat_id, 'text': wh.get_weather_update()}
    res = requests.post(f"{api_url}sendMessage", data=params).json()

    if res["ok"]:
        return {
            'statusCode': 200,
            'body': res['result'],
        }
    else:
        print(res)
        return {
            'statusCode': 400,
            'body': event
        }