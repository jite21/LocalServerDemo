from aiohttp import web
import socketio
import asyncio

import json
from traceback import print_exc

sio = socketio.AsyncServer()

class UserSession(object):
    '''
    Class to store User Sessions and Transaction. 
    Integration with Redis will be better :)
    '''
    Sessions = {}
    Transactions = {}

    @staticmethod
    def set_session(username, sid):
        '''
        To store user session in dictionary.
        '''

        UserSession.Sessions[username] = sid

    @staticmethod
    def get_session(username):
        '''
        To get session of a user
        '''

        return UserSession.Sessions[username]

    @staticmethod
    def set_transaction(username, sid, localurls):
        '''
        To set User connection details
        '''

        UserSession.Transactions[sid] = {}
        UserSession.Transactions[sid]['username'] = username
        UserSession.Transactions[sid]['localurls'] = localurls

    @staticmethod
    def set_response(response):
        sid = response['sid']
        UserSession.Transactions[sid]['response'] = response['Response']
    
    @staticmethod
    def get_response(sid):
        try:
            return UserSession.Transactions[sid]['response']
        except Exception:
            return 'No Response Found :('

    @staticmethod
    def set_user_session(username, sid, localurls):
        UserSession.set_session(username, sid)
        UserSession.set_transaction(username, sid, localurls)

    @staticmethod
    def get_user_localurl(sid, localurlid):
        return UserSession.Transactions[sid]['localurls'][localurlid]
    
    @staticmethod
    def delete_all(sid):
        '''
        To remove session of the user from server.
        '''
        username = UserSession.Transactions[sid]['username']
        del(UserSession.Transactions[sid])
        del(UserSession.Sessions[username])

        print('{} session is removed.'%(username))

    @staticmethod
    def print_all(msg = ""):
        print('{0}\nUser Sessions : {1}\nTransactions : {2}'.format(
                                                            msg,
                                                            json.dumps(UserSession.Sessions),
                                                            json.dumps(UserSession.Transactions)
                                                            ))



class Proxy(socketio.AsyncNamespace):

    async def index(self, request):
        """Serve the client-side application."""

        try:
            self.state = 0
            localurlid = request.match_info['localurlid']
            username = request.match_info['username']
            sid = UserSession.get_session(username)
            localurl = UserSession.get_user_localurl(sid,localurlid)
            data = {'localurl':localurl, 
                    'headers':{str(key):str(value) for key,value in request.raw_headers}}

            def get_response(*args):
                response = json.loads(args[0])
                UserSession.set_response(response)
                self.state = 1

            await sio.emit('request', json.dumps(data), callback=get_response, room=sid)
            for i in range(20):
                if not self.state:
                    await asyncio.sleep(1)
            
            response = UserSession.get_response(sid)
            return web.Response(text=response['body'], headers=response['headers'])

        except KeyError:
            print_exc()
            return web.Response(text='I am sorry I was not able to find the user. Please check the username')

        except Exception as e:
            print_exc()
            return web.Response(text='Looks Like I am unable to contact the website. Please check the url.')

    async def on_set_env(self, sid, data):
        config = json.loads(data)
        UserSession.set_user_session(username = config['username'],
                                     sid = config['sid'],
                                     localurls = config['localurls']
                                     )

        UserSession.print_all('Setting Variable')

    async def on_connect(self, sid, environ):
        print("connect ", sid)

    async def on_disconnect(self, sid):
        UserSession.delete_all(sid)
        UserSession.print_all('Deleting Session')
        print('disconnect ', sid)


def main():
    app = web.Application()
    sio.attach(app)
    sio.register_namespace(Proxy('/'))
    app.router.add_get(r'/{username}/{localurlid:\d+}', Proxy().index)
    return app

if __name__ == '__main__':
    web.run_app(main())