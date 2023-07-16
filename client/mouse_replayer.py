from pynput.mouse import Button, Controller
import time
import ctypes
import socket
import logging
import errno
import pickle

try:
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
except:
    print("Не винда")


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"  # адресс сервера
        self.port = 5555
        self.package_size = 2048
        self.addr = (self.host, self.port)
        self.alive = True
        self.id = self.connect()

    def disconnect(self):
        self.client.close()
        self.alive = False

    def connect(self):
        while self.alive:
            try:
                self.client.connect(self.addr)
                return self.receive()
            except socket.error as e:
                if e.errno == errno.WSAECONNREFUSED:
                    logging.error("Connection refused. Retrying...")
                    time.sleep(1)  # Пауза перед новой попыткой подключения

    def receive(self):
        return pickle.loads(self.client.recv(self.package_size))

    def send_and_get(self, data):
        self.send(data)
        return self.receive()

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return True
        except socket.error as e:
            logging.error("Error sending data: %s", e)
            return False


class MouseReplayer:
    def __init__(self) -> None:
        self.buffer = []
        self.send_thread = None
        self.mouse_controller = Controller()
        self.delay = 0.00001

    def connect(self):
        self.network = Network()
        self.network.send_and_get("password")
        self.network.send_and_get("1")
        self.connected = True

    def start(self):
        while True:
            events = self.network.receive()
            print("delayu")
            # for event in events.values():
            #     print(event)
            #     x, y, action = event
            #     time.sleep(self.delay)
            #     self.mouse_controller.position = (x, y)
            #     if action == 1:
            #         self.mouse_controller.press(Button.left)
            #     elif action == 2:
            #         self.mouse_controller.press(Button.right)
            #     elif action == 3:
            #         self.mouse_controller.release(Button.left)
            #     elif action == 4:
            #         self.mouse_controller.release(Button.right)


replayer = MouseReplayer()
replayer.connect()
replayer.start()
