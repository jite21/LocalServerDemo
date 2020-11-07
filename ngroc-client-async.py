import socketio
import requests
import json

from traceback import print_exc
import sys

sio = socketio.Client()
serverurl = 'http://localhost:8080/'
localurls = ['http://localhost:5001/', 'http://localhost:5002/']
username = 'jitendra'

def set_config():
    return dict(enumerate(localurls))

@sio.event
def connect():
    print('connection established')
    config = {}
    config['localurls'] = set_config()
    config['sid'] = sio.sid
    config['username'] = username
    print(config)
    sio.emit('set_env', json.dumps(config))

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on('request')
def user_req(data):
    request = json.loads(data)
    try:
        resp = requests.get(request['localurl'], headers = request['headers'])
        resp_dict = {'Response':{}}
        resp_dict['Response']['headers'] = dict(resp.headers)
        resp_dict['Response']['body'] = resp.text
        resp_dict['sid'] = sio.sid
        return json.dumps(resp_dict)
    except Exception as e:
        return str(print_exc())

def start_server():
    sio.connect(serverurl)
    sio.wait()

if __name__ == '__main__':
    start_server()