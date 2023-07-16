import socket
import threading
import logging
import pickle

password = 'password'
# оставляем адрес пустым если на сервере
server = socket.create_server(('localhost', 5555))
server.listen(100)
package_size = 2048
streamer = ""
replayers = []

logging.basicConfig(level=logging.INFO)


def replayers_thread(moves):
    for replayer in replayers:
        try:
            replayer.sendall(moves)
        except ConnectionError as e:
            logging.error(e)
            replayers.remove(replayer)
    return True


def streamer_thread(conn):
    global streamer
    while True:
        try:
            data = conn.recv(package_size)
            moves = data
            threading.Thread(target=replayers_thread, args=(moves,)).start()
        except ConnectionResetError as e:
            logging.error(e)
            break
    streamer = ""
    return


def send(conn, mes):
    mes = pickle.dumps(mes)
    conn.send(mes)


def receive(conn):
    return pickle.loads(conn.recv(package_size))


def threaded_client(conn, addr):
    global streamer
    send(conn, "Waiting for password")
    reply = receive(conn)
    if reply == password:
        send(conn, "Waiting for role")
        reply = receive(conn)
        if reply == '0':  # streamer
            if not streamer:
                send(conn, "Successfully connected")
                streamer = addr
                threading.Thread(target=streamer_thread, args=(conn,)).start()
        elif reply == '1':  # replayer
            send(conn, "Successfully connected")
            replayers.append(conn)
            return
    send(conn, "Failed to connect")
    return


while True:
    conn, addr = server.accept()
    logging.info("Connected to: %s", addr)
    threading.Thread(target=threaded_client, args=(conn, addr)).start()
