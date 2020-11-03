from aiohttp import web
import socketio

import asyncio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

class Proxy():
    def __init__(self):
        pass
    
    async def index(self, request):
        """Serve the client-side application."""
        req_url = 'http://localhost:5001'
        self.resp = 'Not Able to Connect'
        def get_response(*args):
            self.resp = args[0]
            print(self.resp)
            
        await sio.emit('request', str(req_url), callback=get_response)
        print('before sleep')
        await asyncio.sleep(5)
        print('after sleep')
        return web.Response(text=self.resp)

@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('response')
def get_response(data):
    print(data)


app.router.add_get('/', Proxy().index)

if __name__ == '__main__':
    web.run_app(app)