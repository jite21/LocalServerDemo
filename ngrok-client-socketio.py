from socketIO_client import SocketIO, LoggingNamespace

def show_reply(*reply):
    print(*reply)

def onconnect():
    print('Connected')

def onrequest(*req):
    print(*req)

with SocketIO('127.0.0.1', 5000, LoggingNamespace) as socketIO:
    socketIO.emit('message','hello')
    socketIO.on('reply', show_reply)
    socketIO.on('connect', onconnect)
    socketIO.on('request', onrequest)
    socketIO.wait()