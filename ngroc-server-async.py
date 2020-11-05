from aiohttp import web
import socketio

import asyncio
from traceback import print_exc

sio = socketio.AsyncServer()

class Proxy(socketio.AsyncNamespace):
    resp = 'Not Able to Connect'
    config = {}

    async def index(self, request):
        """Serve the client-side application."""

        try:
            self.state = 0
            localsiteid = request.match_info['localsiteid']
            username = request.match_info['username']
            localurl = Proxy.config[username][localsiteid]

            def get_response(*args):
                Proxy.resp = args[0]
                self.state = 1

            await sio.emit('request', localurl, callback=get_response)
            for i in range(20):
                if not self.state:
                    await asyncio.sleep(1)
            
            return web.Response(text=Proxy.resp)

        except KeyError:
            print_exc()
            return web.Response(text='I am sorry I was not able to find the user. Please check the username')

        except Exception as e:
            print_exc()
            return web.Response(text='Looks Like I am unable to contact the website. Please check the url.')

    def on_connect(self, sid, environ):
        print("connect ", sid)

    def on_disconnect(self, sid):
        print('disconnect ', sid)

    async def on_set_env(self, sid, data):
        import json
        config = json.loads(data)
        Proxy.config[config['username']] = config['urlmap']

def main():
    app = web.Application()
    sio.attach(app)
    sio.register_namespace(Proxy('/'))
    app.router.add_get(r'/{username}/{localsiteid:\d+}', Proxy().index)
    web.run_app(app)
    
if __name__ == '__main__':
    main()