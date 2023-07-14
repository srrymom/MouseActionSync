from pynput.mouse import Button, Controller
from pynput import keyboard
import requests
import time
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

server_url = 'http://127.0.0.1:8080/events'
session = requests.Session()

mouse_controller = Controller()
last_request_time = 0


def get_events():

    response = requests.get(server_url)
    return response.json()


# def on_press(key):
#     if key  == keyboard.Key.ctrl_r:


# listener = keyboard.Listener(
#     on_press=on_press)
# listener.start()


while True:
    if (new := time.time()) - last_request_time > 0.5:
        last_request_time = new
        events = get_events()
        for event in events.values():
            print(event)
            x, y, action = event
            time.sleep(0.0001)
            mouse_controller.position = (x, y)
            if action == 1:
                mouse_controller.press(Button.left)
            elif action == 2:
                mouse_controller.press(Button.right)
            elif action == 3:
                mouse_controller.release(Button.left)
            elif action == 4:
                mouse_controller.release(Button.right)
