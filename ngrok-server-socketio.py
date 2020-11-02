from flask import Flask, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
ips = ["127.0.0.1"]

@app.route('/test')
def index():
    return render_template('index.html')

@socketio.on('message')
def onmessage(message):
    print(message)
    socketio.emit('reply','Hi')

@socketio.on('connect')
def socket_test():
    socketio.emit('success', 'Server is Accessible')

@app.route('/')
def userreq():
    '''
    Get the request from User Computer and redirect it to Local server Websocket.
    Issue is Flask is not async and socketio is async.
    '''
    print(request.method, request.path)
    socketio.emit('request', {'method':request.method, 'path':request.path})
    return 202

@socketio.on('response')
def get_request(payload):
    l_url = payload['path']
    l_method = payload['method']
    l_header = payload['header']
    l_data = payload['data']

    resp = requests.request(
                     l_method, 
                     l_url, 
                     header = l_header,
                     data = l_data
                     )
    try:
        emit('send response', {
            'status_code' : resp.status_code,
            'text' : resp.text
        })
    except Exception as e:
        print(e)
        emit('send response',{
            'text': 'Error Occured'
        })


if __name__ == '__main__':
    print("Starting Websocket server")
    socketio.run(app)