import pynput
from pynput.keyboard import Key, Listener
import datetime

charCount = 0
keys = {}
log_file = None

def start_new_session():
    global log_file, charCount
    if log_file:
        log_file.close()
    session_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = open(f'session_{session_time}.txt', 'a')
    charCount = 0
    keys.clear()

def onKeyPress(key):
    global charCount
    try:
        print(f'Key Pressed: {key} (total number of keys pressed till now:{charCount+1})')
        keys[key] = keys.get(key, 0) + 1
        charCount += 1
        if key == Key.esc:
            end_current_session()
    except Exception as ex:
        print("There was an error:", ex)

def onKeyRelease(key):
    if key == Key.esc:
        return False

def end_current_session():
    print("Session Summary:")
    for key, count in keys.items():
        print(f'Key: {key} - Pressed {count} times')
    writeToFile()
    keys.clear()

def writeToFile():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with log_file as file:
        file.write(f"{timestamp} - Session Summary:\n")
        for key, count in keys.items():
            file.write(f"{timestamp} - Key: {key} - Pressed {count} times\n")
        file.write(f"{timestamp} - Keylog for the session:\n")
        for key in keys.keys():
            file.write(f"{timestamp} - {key}\n")
        file.write(f"{timestamp} - Total Key Counts at the end of the session:\n")
        for key, count in keys.items():
            file.write(f"{timestamp} - Key: {key} - Pressed {count} times\n")

# Only start a new session when the script begins, not at the end of the session.
start_new_session()

with Listener(on_press=onKeyPress, on_release=onKeyRelease) as listener:
    listener.join()
