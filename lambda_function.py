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


def get_event_params(event):
    params = {
        'text_received': event['message']['text'],
        'first_name': event['message']['from']['first_name'],
        'chat_id': event['message']['chat']['id']
    }
    
    return params


def set_message(params):
    msg = None
    if params['text_received'] == "/start":
        msg = f"Hola {params['first_name']}! Bienvenid@, soy el bot del clima y estoy para brindarte información así no te agarra la lluvia."
    elif params['text_received'] == "Obtener información del clima":
        msg = wh.get_weather_update()
    else:
        msg = 'No te entiendo nada culiado ' + u'\U0001F937' #person shrugging emoji 🤷
        
    return msg


def lambda_handler(event, context):
    event_params = get_event_params(event)
    msg = set_message(event_params)
    reply_markup = get_reply_markup()

    params = {
        'chat_id': event_params['chat_id'], 
        'text': msg,
        'parse_mode':'Markdown', #https://core.telegram.org/bots/api#formatting-options
        'reply_markup':reply_markup #https://core.telegram.org/bots/api#replykeyboardmarkup
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