from flask import Flask
import time
#testing fork, cmd commit, pull request

app = Flask(__name__)

@app.route('/')
def index():
    time.sleep(5)
    return 'This is response from Localserver'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')