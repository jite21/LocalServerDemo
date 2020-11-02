import requests
import websocket

ws_server = "ws://127.0.0.1/echo"

def on_message(ws, message):
    print("Recieved message : {}".format(message))
    ws.send("hello")
    #print("Sent Hello again")

def on_error(ws, error):
    print("Error while connecting : {}".format(error))

def on_close(ws):
    print("Connection Closed")

def on_open(ws):
    ws.send("Hello from Client")
    print("Sent opening message")

if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_server,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()