import json
import random
from pynput import mouse
from pynput import keyboard
import time
import _thread
import pickle
from os.path import exists as file_exists
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os
import sys

from firebase_notification import send_notification, send_notification_real_time, send_notification_real_time_key, \
    send_notification_mouse_click_AI, send_notification_keyboard_press_AI

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Tracker:
    def __init__(self, userId, parentID):
        self.keyboard_modelMade = False

        self.listening = True
        self.movedTime = 0
        self.keyPressedTime = 0
        self._startTime = time.gmtime()
        self._record = {}
        self.stream = ""
        self._record["on_move"] = dict()
        self._record["on_click"] = dict()
        self._record["on_press"] = dict()
        self._record["on_release"] = dict()
        self.userId = userId
        self.parentId = parentID
        self.numClicks = 0
        self.clickTime = 0
        self.isFocused = True
        self._invalid_chars = {'$': "Dollar Sign", '#': "Hashtag Symbol", '[': "Left Bracket", ']': "Right Bracket",
                               '/': "Slash", '.': "Period", '\n': "New Line"}

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        self.mouse_listener.start()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.keyboard_listener.start()

        filenameMouse = resource_path("model/mouse_model.sav")
        if (not file_exists(filenameMouse)):
            # make_mouse_model()
            print("File " + filenameMouse + " did not exist")
        else:
            print("File " + filenameMouse + " exists")
        self.mouse_model = pickle.load(open(filenameMouse, 'rb'))
        self.mouse_clicked_class = {0: "Not Paying Attention", 1: "Paying Attention"}

        filenameKeyboard = resource_path('model/keyboard_model.sav')
        # if(not file_exists(filenameKeyboard)):
        #     make_keyboard_model()
        #     print("File " + filenameKeyboard + " did not exist")
        # else:
        #     print("File " + filenameKeyboard + " exists")
        # make_keyboard_model()
        self.keyboard_model = pickle.load(open(filenameKeyboard, 'rb'))
        self.keyboard_class_target = ['dialog', 'note']

        #Load Vocabulary
        self.transformer = TfidfTransformer()
        self.load_vec = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(resource_path("model/feature.pkl"),"rb")))
        self.keyboard_modelMade = True

    # Update this later
    def stop_listening(self):
        # print("Stopped Listening")
        self.listening = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

        # Update On Move
        # record = json.dumps(self._record['on_move'])
        # for key, value in self._record['on_move'].items():
        #     record = {'x': value['x'], 'y': value['y']}
        #     send_notification(record=record, userID=self.get_user(), parentID=self.parentId,
        #                       action='mouse_on_move/' + str(
        #                           time.strftime("%Y-%m-%d %H:%M:%S", self._startTime)) + '/' + str(key))

        # Update On Click
        # record = json.dumps(self._record['on_click'])
        # for key, value in self._record['on_click'].items():
        #     record = {'x': value['x'], 'y': value['y']}
        #     send_notification(record=record, userID=self.get_user(), parentID=self.parentId,
        #                       action='on_click/' + str(time.strftime("%Y-%m-%d %H:%M:%S", self._startTime)) + '/' + str(
        #                           key))

        # Update On Scroll
        # record = json.dumps(self._record['on_scroll'])
        # send_notification(record=record, userID=self.get_user(), parentID=self.parentId,
        #                   action='on_scroll/' + str(time.strftime("%Y-%m-%d %H:%M:%S", self._startTime)))

        # Update Keyboard Presses
        # record = self._record["on_press"]
        # send_notification(record=record, userID=self.get_user(), parentID=self.parentId,
        #                   action='on_press/' + str(time.strftime("%Y-%m-%d %H:%M:%S", self._startTime)))

        # Update On Release Presses
        #record = json.dumps(self._record['on_release'])
        #send_notification(record=record, userID=self.get_user(), action='on_release')

        # Change user status
        record = {'status': 'off', 'End Time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))}
        send_notification(record=record, userID=self.get_user(), parentID=self.parentId, action='user_status')

        # print(self.userId)
        # print(self._record)

        # TESTING PURPOSES ONLY
        #print("MOUSE MODEL TEST")
        #for i in range(20):dawdaswd dwAwdwdsd grg drg drgsrg vfgdcvbvbfgfdfdfaawd dsas gefawd asdawdAdqdqetrgfdvbbvcvdsdfxdvdsfrrvsdffsefeseesfefseefsesfe
        #    rand = random.randint(0, 50)
        #    print("Number of Clicks: " + str(rand))
        #    print(self.mouse_pred(rand))

    def is_listening(self):
        return self.listening

    def get_mouse_record(self):
        return self._record

    def get_user(self):
        return self.userId

    def on_move(self, x, y):
        if self.movedTime < time.time():
            self.movedTime = time.time() + 0.5
            # print('Pointer moved to {0}'.format((x, y)))
            self._record["on_move"][time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())] = {'x': x, 'y': y}
            #print(x, y)

            # record = json.dumps(self._record['on_move'])

            try:
                _thread.start_new_thread(send_notification_real_time, (x, y, self.get_user(), self.parentId))
            except Exception as e:
                print(e)
            #send_notification_real_time(x, y,  userID = self.get_user(), parentID = self.parentId)
            #send_notification(record=record, userID = self.get_user(),action='mouse_on_move')

    def on_click(self, x, y, button, pressed):
        # print('{0} at {1}'.format(
        #    'Pressed' if pressed else 'Released',
        #   (x, y)))
        #self._record["on_click"][time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())] = {'x': x, 'y': y}

        # # record = json.dumps(self._record['on_click'])
        # # send_notification(record=record, userID=self.get_user(), action='on_click')
        # if self.clickTime < time.time() and self.isFocused:
        #     #print("MOUSE_CLICK_TEST")
        #     if(self.clickTime != 0):
        #         #upload to firebase
        #         string_pred = self.mouse_pred(self.numClicks)
        #         num_val_pred = self.mouse_model.predict([[self.numClicks]])
        #         #print(self.numClicks)
        #         print(string_pred)
        #         #print(num_val_pred)
        #         if(num_val_pred == 0):
        #             self.isFocused = False
        #             print("Student stopped focusing; The student clicked " + str(self.numClicks))
        #         send_notification_mouse_click_AI(num_result=num_val_pred[0], num_clicks=self.numClicks, userID=self.get_user(), parentID=self.parentId)
        #     self.clickTime = time.time() + 10
        #     self.numClicks = 0
        self.numClicks = self.numClicks + 1

    #@tl.job(interval=timedelta(seconds = 10))
    def send_mouse_pred(self):
        num_val_pred = self.mouse_model.predict([[self.numClicks]])

        ## For testing
        # string_pred = self.mouse_pred(self.numClicks)
        # print(string_pred)
        # if (num_val_pred == 0):
        #     print("Student stopped focusing; The student clicked " + str(self.numClicks))
        send_notification_mouse_click_AI(num_result=num_val_pred[0], num_clicks=self.numClicks, userID=self.get_user(),
                                         parentID=self.parentId)

        self.numClicks = 0

    def send_keyboard_pred(self):
        num_val_pred = self.keyboard_pred_num(self.stream)
        try:
            _thread.start_new_thread(send_notification_keyboard_press_AI, (num_val_pred[0], self.stream,
                                                                       self.get_user(), self.parentId))
        except Exception as e:
            print(e)
        self.stream = ""

    def on_press(self, key):
        try:
            #print('alphanumeric key {0} pressed'.format(
            #   key.char))
            if key.char in self._invalid_chars:
                #key = self._invalid_chars[key.char]
                # Set key to empty string if a character is invalid; better for text input
                key = ""
            else:
                key = str(key.char)

        except AttributeError:
            # print('special key {0} pressed'.format(
            #     key))
            key = str(key)
            key = key[4:]
            if(key == "space"):
                key = " "
            else:
                key = ""

        if key in self._record["on_press"]:
            self._record["on_press"][str(key)] += 1
        else:
            self._record["on_press"][str(key)] = 1
        self.stream += key
        #print(self.stream)
        #if(self.keyboard_modelMade):
        #    print(self.keyboard_pred(self.stream))

        # record = json.dumps(self._record['on_press'])
        # record = {str(time.strftime("%x %X", time.gmtime())): str(key)}
        # record = {str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())) : str(key)}
        # send_notification(record=record, userID=self.get_user(), action='on_press')
        if(key != ""):
            # This is for realtime visualization of stream
            if(self.keyPressedTime < time.time()):
                self.keyPressedTime = time.time()+0.5
                try:
                    _thread.start_new_thread(send_notification_real_time_key, (self.stream, self.get_user(), self.parentId))
                except Exception as e:
                    print(e)
        #
        #     # Analysis
        #     num_val_pred = self.keyboard_pred_num(self.stream)
        #     _thread.start_new_thread(send_notification_keyboard_press_AI,(num_val_pred[0], self.stream,
        #                                      self.get_user(), self.parentId))
    def on_release(self, key):
        # print('{0} released'.format(
        #    key))
        if key in self._record["on_release"]:
            self._record["on_release"][str(key)] += 1
        else:
            self._record["on_release"][str(key)] = 1
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    # This function is for testing purposes
    def mouse_pred(self, n):
        pred = self.mouse_model.predict([[n]])
        return "Prediction: " + self.mouse_clicked_class[pred[0]]

    def keyboard_pred(self, sentence):
        data = self.transformer.fit_transform(self.load_vec.fit_transform(np.array([sentence])))
        pred = self.keyboard_model.predict(data)
        #print(sentence)
        #print(self.keyboard_class_target[pred[0]])
        return "Prediction: " + self.keyboard_class_target[pred[0]]

    def keyboard_pred_num(self,sentence):
        data = self.transformer.fit_transform(self.load_vec.fit_transform(np.array([sentence])))
        pred = self.keyboard_model.predict(data)
        return pred

    def modelsMade(self):
        return self.keyboard_modelMade

    # def reset_database(self):
    #     record = None
    #     send_notification(record=record, userID=self.get_user(), action='mouse_on_move')
    #     send_notification(record=record, userID=self.get_user(), action='on_click')
    #     send_notification(record=record, userID=self.get_user(), action='on_scroll')
    #     send_notification(record=record, userID=self.get_user(), action='on_press')
    #     send_notification(record=record, userID=self.get_user(), action='on_release')
