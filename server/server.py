from bottle import Bottle, request, run, route
import socket
import pickle
import threading

password = 'password'
server = socket.create_server(('localhost', 5555))
server.listen(100)
package_size = 2048
streamer = ""
replayers = []
print("Waiting for a connection")


def replayers_thread(moves):
    for replayer in replayers:
        try:
            replayer.sendall(b"test")
        except ConnectionResetError as e:
            print(e)
            replayers.remove(replayer)
    return True


def streamer_thread(conn):
    global streamer, moves
    while True:
        try:
            data = conn.recv(package_size)
            reply = pickle.loads(data)
            moves = reply
            threading.Thread(target=replayers_thread, args=(moves,)).start()
            print(threading.active_count())
        except ConnectionResetError as e:
            print(e)
            break
    streamer = ""
    return


def threaded_client(conn, addr):
    global streamer
    conn.send(b"Waiting for password")
    data = conn.recv(package_size)
    reply = data.decode('utf-8')
    if reply == password:
        conn.sendall(b"Waiting for role")
        data = conn.recv(package_size)
        reply = data.decode('utf-8')
        if reply == '0':  # streamer
            if not streamer:
                conn.sendall(b"Successfully connected")
                streamer = addr
                threading.Thread(target=streamer_thread, args=(conn,)).start()
        elif reply == '1':  # replayer
            conn.sendall(b"Successfully connected")
            replayers.append(conn)
            return
    conn.sendall(b"Failed to connect")
    return


while True:
    conn, addr = server.accept()
    print("Connected to: ", addr)
    threading.Thread(target=threaded_client, args=(conn, addr)).start()
