from bottle import Bottle, request, run, route
import time
from datetime import datetime

app = Bottle()

moves = {}


@route('/test')
def handle_post():
    return "test"


@route('/events', method='POST')
def handle_post():
    global moves
    moves = {x: y for x, y in enumerate(request.json)}
    print(moves)


@route('/events', method='GET')
def handle_get():
    print(moves)
    return moves


if __name__ == '__main__':
    run(host='127.0.0.1', port=8080, debug=False)
