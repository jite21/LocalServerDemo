import socketio
import requests
import json

from traceback import print_exc
import sys

sio = socketio.Client()
server_url = 'http://34.72.78.16:80/'
local_urls = ['http://localhost:5001/', 'http://localhost:5002/']
username = 'jitendra'

def set_config():
    return dict(enumerate(local_urls))

@sio.event
def connect():
    print('connection established')
    config = {}
    config['urlmap'] = set_config()
    config['username'] = username
    sio.emit('set_env',json.dumps(config))

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
    try:
        resp = requests.get(url)
        return resp.text
    except Exception as e:
        return str(print_exc())

sio.connect(server_url)
sio.wait()