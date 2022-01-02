import json 
import requests
import os
import weather_helper as wh
from weather_helper import WeatherInfoHandler

TOKEN = os.environ["TELEGRAM_TOKEN"]
api_url = f"https://api.telegram.org/bot{TOKEN}/"

def get_reply_markup():
    keyboard = list()
    keyboardbuttons_1stline = list()
    keyboardbuttons_2ndtline = list()
    
    keyboardbuttons_1stline.append('Obtener información del clima')
    button = {
        "text": "Enviar ubicación",
        "request_contact": False,
        "request_location": True,
        "request_poll": False
    }
    
    keyboardbuttons_2ndtline.append(button)
    
    keyboard.append(keyboardbuttons_1stline)
    keyboard.append(keyboardbuttons_2ndtline)
    reply_markup_dict = {
        "keyboard": keyboard, 
        # "resize_keyboard": False,
        # "selective": False,
        # "input_field_placeholder": "Some text",
        "one_time_keyboard": True
    }
    
    reply_markup = json.dumps(reply_markup_dict)

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
        msg = get_welcome_message(params)
        
    elif params['text_received'] == "Obtener información del clima":
        wih = WeatherInfoHandler()
        msg = wih.get_weather_update()
    
    else:
        msg = get_default_message()
        
    return msg


def get_welcome_message(params):
    return f"Hola {params['first_name']}! Bienvenid@, soy el bot del clima y estoy para brindarte información así no te agarra la lluvia."


def get_default_message():
    return 'No entendí tu mensaje ' + u'\U0001F937' #person shrugging emoji 🤷


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