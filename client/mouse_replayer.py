from pynput.mouse import Button, Controller
from pynput import keyboard
import requests
import time
import ctypes
import pickle
import socket
import logging

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

# server_url = 'http://127.0.0.1:8080/events'
# session = requests.Session()

# mouse_controller = Controller()
# last_request_time = 0


# class Network:
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.host = "localhost"
#         self.port = 5555
#         self.package_size = 2048
#         self.addr = (self.host, self.port)
#         self.id = self.connect()

#     def connect(self):
#         try:
#             self.client.connect(self.addr)
#             return self.client.recv(self.package_size).decode()
#         except socket.error as e:
#             logging.error("Failed to connect: %s", e)
#         return False

#     def send_encoded(self, data):
#         self.client.sendall(data)

#     def receive_encoded(self):
#         return self.client.recv(self.package_size).decode()

#     def send(self, data):
#         try:
#             self.client.send(str.encode(data))
#             reply = self.receive_encoded()
#             return reply
#         except socket.error as e:
#             logging.error("Error sending data: %s", e)
#             return str(e)


# class MouseReplayer:
#     def __init__(self) -> None:
#         self.network = Network()
#         print(self.network.send("password"))
#         print(self.network.send("1"))
#         while True:
#             print(self.network.receive_encoded())


# replayer = MouseReplayer()

# def get_events():

#     response = requests.get(server_url)
#     return response.json()


# def on_press(key):
#     if key  == keyboard.Key.ctrl_r:


# listener = keyboard.Listener(
#     on_press=on_press)
# listener.start()


# while True:
#     if (new := time.time()) - last_request_time > 0.5:
#         last_request_time = new
#         events = get_events()
#         for event in events.values():
#             print(event)
#             x, y, action = event
#             time.sleep(0.0001)
#             mouse_controller.position = (x, y)
#             if action == 1:
#                 mouse_controller.press(Button.left)
#             elif action == 2:
#                 mouse_controller.press(Button.right)
#             elif action == 3:
#                 mouse_controller.release(Button.left)
#             elif action == 4:
#                 mouse_controller.release(Button.right)
