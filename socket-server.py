import socketio

# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='aiohttp')

# wrap with ASGI application
app = socketio.ASGIApp(sio)

@sio.event
async def my_event(sid, data):
    print('event : ',sid, data)

@sio.event
async def connect(sid, environ):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.on('my custom event')
async def another_event(sid, data):
    print('my custom event : ', sid, data)