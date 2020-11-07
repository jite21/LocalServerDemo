from flask import Flask
import time
#testing fork, cmd commit, pull request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Test</h1><p>Test</p><button>Test</button><b>This is response from Localserver</b>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')