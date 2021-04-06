import json 
import requests
import os
import weather_helper as wh

TOKEN = os.environ["TELEGRAM_TOKEN"]
api_url = f"https://api.telegram.org/bot{TOKEN}/"

def get_reply_markup():
    options = list()
    options.append(['Obtener información del clima'])
    reply_markup = json.dumps({"keyboard": options, "one_time_keyboard": True})

    return reply_markup


def lambda_handler(event, context):
    text_received = event['message']['text']
    first_name = event['message']['from']['first_name']
    chat_id = event['message']['chat']['id']

    msg = None
    if text_received == "/start":
        msg = f"Hola {first_name}! Bienvenid@, soy el bot del clima y estoy para brindarte información así no te agarra la lluvia."
    elif text_received == "Obtener información del clima":
        msg = wh.get_weather_update()
    
    reply_markup = get_reply_markup()

    params = {
        'chat_id': chat_id, 
        'text': msg,
        'parse_mode':'Markdown', #https://core.telegram.org/bots/api#formatting-options
        'reply_markup':reply_markup#https://core.telegram.org/bots/api#replykeyboardmarkup
    }

    if msg != None:

        res = requests.post(f"{api_url}sendMessage", data=params).json()
        if res["ok"]:
            return {
                'statusCode': 200,
                'body': res['result'],
            }
    
    print(res)
    return {
        'statusCode': 400,
        'body': event
    }