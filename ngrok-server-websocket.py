from flask import Flask, request
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def hello():
    return 'Hello World !!'

@sockets.route('/echo')
def echo_socket(ws):
    msg = ws.receive()
    print(msg)
    ws.send('Ok Got it')

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app, handler_class=WebSocketHandler)
    server.serve_forever()