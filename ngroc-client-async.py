import socketio
import requests

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on('request')
def user_req(url):
    print(url)
    resp = requests.get(url)
    return resp.text

sio.connect('http://localhost:8080')
sio.emit('message','test')
sio.wait()