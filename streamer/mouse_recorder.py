import time
from pynput import mouse, keyboard
import threading
import pickle
import socket
import logging
import errno


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        self.package_size = 2048
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        while True:
            try:
                self.client.connect(self.addr)
                return self.client.recv(self.package_size).decode()
            except socket.error as e:
                if e.errno == errno.WSAECONNREFUSED:
                    logging.error("Connection refused. Retrying...")

    def send_encoded(self, data):
        try:
            self.client.sendall(data)
        except socket.error as e:
            logging.error("Failed to connect: %s", e)
            self.connect()

    def receive_encoded(self):
        return self.client.recv(self.package_size).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.receive_encoded()
            return reply
        except socket.error as e:
            logging.error("Error sending data: %s", e)
            return str(e)


class MouseRecorder:
    def __init__(self) -> None:
        self.buffer = []

    def start(self):
        self.network = Network()
        self.network.send("password")
        self.network.send("0")
        self.start_listeners()
        self.start_sending()

    def start_listeners(self):
        logging.info("Mouse recorder started")
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.listener.start()
        self.key_listebber = keyboard.Listener(
            on_press=self.on_press)
        self.key_listebber.start()

    def start_sending(self):
        logging.info("Sending started")
        self.thread = threading.Thread(target=self.send_events_thread)
        self.thread.start()

    def send_event(self, buffer_copy):
        serialized_data = pickle.dumps(buffer_copy)
        self.network.send_encoded(serialized_data)

    def on_press(self, key):
        if key == keyboard.Key.ctrl_r:
            self.listener.stop()

    def send_events_thread(self):
        while True:
            time.sleep(1)
            if self.buffer:
                buffer_copy = self.buffer.copy()
                self.buffer.clear()
                t = threading.Thread(
                    target=self.send_event, args=(buffer_copy,))
                t.start()

    def add_event(self, x, y, a=0):
        self.buffer.append((x, y, a))

    def on_move(self, x, y):
        self.add_event(x, y)

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            a = 1
        else:
            a = 2
        if not pressed:
            a += 2
        self.add_event(x, y, a)

    def on_scroll(self, x, y, dx, dy):
        pass


def main():
    logging.basicConfig(level=logging.INFO)
    recorder = MouseRecorder()
    recorder.start()


if __name__ == "__main__":
    main()
