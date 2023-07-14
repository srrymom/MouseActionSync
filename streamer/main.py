import time
from pynput import mouse, keyboard
from pynput.mouse import Button
import requests
import threading

server_url = 'http://127.0.0.1:8080/events'
session = requests.Session()

buffer = []
previous_time = time.time()


def send_event(events):
    try:
        session.post(server_url, json=events)
    except:
        print("pizdec")


def add_event(x, y, a=0):
    buffer.append((x, y, a))


def on_move(x, y):
    add_event(x, y)


def on_click(x, y, button, pressed):
    if button == Button.left:
        a = 1
    else:
        a = 2
    if not pressed:
        a += 2
    add_event(x, y, a)


def on_scroll(x, y, dx, dy):
    pass


def send_event_thread():
    while True:
        time.sleep(1)
        if buffer:
            buffer_copy = buffer.copy()
            buffer.clear()
            t = threading.Thread(target=send_event, args=(tuple(buffer_copy),))
            t.start()


time.sleep(2)
thread = threading.Thread(target=send_event_thread)
thread.start()


listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()


def on_press(key):
    if key == keyboard.Key.ctrl_r:
        listener.stop()


key_listebber = keyboard.Listener(
    on_press=on_press)
key_listebber.start()
