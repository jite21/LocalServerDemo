import asyncio
import os

import aiohttp.web

HOST = '0.0.0.0'
PORT = 8080


async def get_user_request(request):
    '''
    To get user's Request
    '''
    return aiohttp.web.Response(text='User Request')


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')

    print('Websocket connection closed')
    return ws


def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/', get_user_request)
    app.router.add_route('GET', '/ws', websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()