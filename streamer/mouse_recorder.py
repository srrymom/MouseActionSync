from pynput import mouse, keyboard
import time
import threading
import pickle
import socket
import logging
import errno


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"  # адрес сервера
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


class MouseRecorder:
    def __init__(self) -> None:
        self.buffer = []
        self.listener = None
        self.restart_active = True
        self.key_listener = None
        self.pause = False
        self.send_thread = None
        self.stop_event = threading.Event()  # Событие для остановки

    def restart(self):
        self.start()
        while self.restart_active:
            if not self.pause:
                self.stop()
                self.start()

    def start(self):
        self.connect()
        self.start_key_listener()
        self.start_mouse_listener()
        self.start_sending()

    def stop(self):
        self.connected = False
        self.network.disconnect()
        self.stop_mouse_listener()

    def connect(self):
        self.network = Network()
        self.network.send_and_get("password")
        self.network.send_and_get("0")
        self.connected = True

    def start_mouse_listener(self):
        if not self.pause:
            logging.info("Mouse recorder started")
            self.listener = mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll)
            self.listener.start()
        else:
            logging.info("Mouse recorder on pause")

    def start_key_listener(self):
        if not self.key_listener or not self.key_listener.running:
            self.key_listener = keyboard.Listener(
                on_press=self.on_press)
            self.key_listener.start()

    def stop_mouse_listener(self):
        logging.info("Mouse recorder stopped")
        if self.listener:
            self.listener.stop()

    def stop_key_listener(self):
        if self.key_listener:
            self.key_listener.stop()

    def start_sending(self):
        logging.info("Sending started")
        self.send_thread = threading.Thread(
            target=self.send_events_thread, name="send_events_thread")
        self.send_thread.start()
        self.send_thread.join()

    def send_event(self, buffer_copy):
        res = self.network.send(buffer_copy)
        if not res:
            self.connected = False

    def on_press(self, key):
        if key == keyboard.Key.ctrl_r:
            if not self.pause:
                self.stop_mouse_listener()
                self.pause = True
            else:
                self.pause = False
                self.start_mouse_listener()

    def send_events_thread(self):
        while self.connected:
            time.sleep(1)
            if self.buffer:
                buffer_copy = self.buffer.copy()
                self.buffer.clear()
                t = threading.Thread(
                    target=self.send_event, args=(buffer_copy,), name="send_event")
                t.start()
        self.stop_event.clear()  # Очистка события после остановки

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
    recorder.restart()


if __name__ == "__main__":
    main()
