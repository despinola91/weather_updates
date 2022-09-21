import json 
import requests
import os
import weather_helper as wh
from weather_helper import WeatherInfoHandler

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEATHER_API_TOKEN = os.environ["WEATHER_API_TOKEN"]
api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

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
    text = ""
    try:
        text = event['message']['text']
    except:
        print('No text was found in message')
    
    location = ""
    try:
        location = event['message']['location']
    except:
        print('No location was found in message')
        
    params = {
        'text_received': text,
        'first_name': event['message']['from']['first_name'],
        'chat_id': event['message']['chat']['id'],
        'location': location
    }
    
    return params


def set_message(params):
    msg = None
    
    if params['text_received'] == "/start":
        msg = get_welcome_message(params)
        
    elif params['text_received'] == "Obtener información del clima":
        wih = WeatherInfoHandler()
        msg = wih.get_weather_update()
    
    elif params['location'] != "":
        msg = get_location_message(params)
    else:
        msg = get_default_message()
        
    return msg


def get_welcome_message(params):
    return f"Hola {params['first_name']}! Bienvenid@, soy el bot del clima y estoy para brindarte información así no te agarra la lluvia."


def get_location_message(params):
    #return f"Hola! Me enviaste tu ubicacion con latitud {params['location']['latitude']} y longitud {params['location']['longitude']}. Estoy trabajando en esto!"
    lat = params['location']['latitude']
    lon = params['location']['longitude']

    #https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_TOKEN}&lang=es&units=metric")
    
    message = """
    I'm working on that. 
    Testing testing.
    Multiline.
    """
    #message = "res.status_code: {res.status_code}  res.url = {res.url}"

    #res.text = {res.text}
    #json: {json.dumps(res.json(), indent=4)}
    #res.text
    #message = json.dumps(res.json(), indent=4)
    #message = res.text
    #print("res: " + res)
    #print(res.text)
    #message = res.json()
    #print("res.text: " + res.text)
    #print(f"res.json(): {res.json()}")
    #print(f"json.dumps(): {json.dumps(res.json(), indent=4)}")
    return message

def get_default_message():
    return 'No entendí tu mensaje ' + u'\U0001F937' #person shrugging emoji 🤷


def lambda_handler(event, context):
    print(json.dumps(event))
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