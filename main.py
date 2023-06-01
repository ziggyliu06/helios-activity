import tkinter
from mouse_model import make_mouse_model
from tracker import Tracker
from tkinter import ttk
from tkinter import messagebox
import time
import urllib.request
from firebase_notification import send_notification
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from timeloop import Timeloop
from datetime import timedelta
import json
import pickle
import random
from os.path import exists as file_exists
from keyboard_model import make_keyboard_model

# Fetch the service account key JSON file contents
cred = credentials.Certificate('ziggy-project-2-firebase-adminsdk-k97lv-cb69583cd7.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ziggy-project-2-default-rtdb.firebaseio.com"
})
ref = db.reference()
print(ref.get())

global t
t = None
global stu_ID
global parent_ID
global t1
t1 = Timeloop()

@t1.job(interval = timedelta(seconds=15))
def send_predictions():
    global t
    if(t != None and t.modelsMade()):
        t.send_mouse_pred()
        t.send_keyboard_pred()
    else:
        print("Something broke")

def check_connection():
    try:
        urllib.request.urlopen('http://google.com')  # Python 3.x
        return True
    except:
        return False


def verify_user():
    global t
    find_user = False
    global stu_ID
    global parent_ID
    stu_ID = stu_name.get() + ": " + s_id.get()
    if check_connection():
        for i in ref.get():
            for student in ref.child(i).child("Student List").get():
                #print(ref.child(i).child("Student List").child(student).get())
                if stu_ID == ref.child(i).child("Student List").child(student).get():
                    parent_ID = i
                    print(parent_ID)
                    textbox.config(state="disable")
                    textbox1.config(state="disable")
                    loginButton.destroy()
                    endButton.grid(pady=20)
                    print("You are logged in!")
                    return True
        if not find_user:
            create = messagebox.showinfo("ERROR", "Student ID not found. Please ask your parent about this.")
            return False
    else:
        messagebox.showinfo("failedConnection", "You don't have internet connection")
        return False


def start_tracker():
    if verify_user():
        print("\n######################################################\n")
        print("Tracking initialized")
        record = {'status': 'on', 'Start Time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))}
        send_notification(record=record, userID=stu_ID, parentID=parent_ID, action='user_status')
        global t
        t = Tracker(stu_ID, parent_ID)
        global t1
        t1.start()
        print("TimeLoop has started")


def end_tracking():
    global t
    global t1
    t.stop_listening()
    t1.stop()
    endButton.config(state="disable")


def on_closing():
    global t
    global t1
    if t is not None:
        if t.is_listening():
            t.stop_listening()
            t1.stop()
    root_window.destroy()


root_window = tkinter.Tk()
root_window.geometry("180x250")
root_window.title("Mouse and Keyboard Tracker")
root_window.resizable(False, False)
frm = ttk.Frame(root_window, padding=30)
frm.grid()
ttk.Label(frm, text="Username").grid(pady=20)
stu_name = tkinter.StringVar()
textbox = ttk.Entry(frm, textvariable=stu_name)
textbox.grid()
ttk.Label(frm, text="Student ID").grid(pady=10)
s_id = tkinter.StringVar()
textbox1 = ttk.Entry(frm, textvariable=s_id)
textbox1.grid()
loginButton = ttk.Button(frm, text="Log In", command=start_tracker)
loginButton.grid(pady=20)
endButton = ttk.Button(frm, text="End", command=end_tracking)
root_window.protocol("WM_DELETE_WINDOW", on_closing)
root_window.mainloop()

