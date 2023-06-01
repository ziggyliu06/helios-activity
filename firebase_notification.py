import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
           'Content-Type': 'application/json',
           'Connection': 'keep-alive'}

def send_notification(record, userID, parentID, action):
    #Please add your firebase realtime database url
    url = 'https://ziggy-project-2-default-rtdb.firebaseio.com/'
    # put data to firebase (create a new record)
    try:
        response = requests.put(f'{url}/{parentID}/{userID}/tracker/{action}.json', data=json.dumps(record))
    except ConnectionError as e:
        print(e)
    #print(response.content)
    #print(response)
    #print("Response sent")

def send_notification_real_time(x, y, userID, parentID):
    url = 'https://ziggy-project-2-default-rtdb.firebaseio.com/'
    #print("Sent real time")
    try:
        response = requests.put(f'{url}/{parentID}/{userID}/realtime.json', data=json.dumps({"x" : x, "y" : y}), headers=headers)
    except ConnectionError as e:
        print("Caught exception")
        print(e)
    #print(response.content)
    #print(response)

def send_notification_real_time_key(string_stream, userID, parentID):
    url = 'https://ziggy-project-2-default-rtdb.firebaseio.com/'
    #print("Sent real time")
    try:
        response = requests.put(f'{url}/{parentID}/{userID}/realtimek.json', data=json.dumps({"stream" :  string_stream}), headers=headers)
    except ConnectionError as e:
        print("Caught exception")
        print(e)
    #print(response.content)
    #print(response)

def send_notification_mouse_click_AI(num_result, num_clicks, userID, parentID):
    url = 'https://ziggy-project-2-default-rtdb.firebaseio.com/'
    print("Sends Mouse Clicks")
    try:
        response = requests.put(f'{url}/{parentID}/{userID}/mouse_click_focus.json',
                                data=json.dumps({"Focused" : int(num_result),"num_clicks":int(num_clicks)}), headers=headers)
    except ConnectionError as e:
        print("Caught exception")
        print(e)
    #print(response)

def send_notification_keyboard_press_AI(num_result, stream, userID, parentID):
    url = 'https://ziggy-project-2-default-rtdb.firebaseio.com/'
    print("Sends Keyboard Data")
    print(int(num_result))
    try:
        response = requests.put(f'{url}/{parentID}/{userID}/keyboard_input_focus.json',
                                data=json.dumps({"Focused" : int(num_result),"stream": stream}), headers=headers)
    except ConnectionError as e:
        print("Caught exception")
        print(e)
    #print(response)




