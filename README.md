# test
To make localserver accessible to internet
 
# How to Run ?
## Install python 3

1. Create python virtual environment : **python -m venv <project_name>**
2. Activate the Project : **.\<project_name>\Scripts\activate.bat**
3. create 'src' in <project_name> then go to 'src' directory : **.\<project_name>\src**
4. Run **pip install -r requirements.txt** to install required packages.
5. open 2 cmd in cmd-1 run **'python ngrok-server-socketio.py'** and in cmd-2 run **'python ngrok-client-socketio.py'**

# Description
Protocol used is SocketIO.
ngrok-server-socketio.py - SocketIO server which will take request from User from Internet and redirect it to local server.
ngrok-client-socketio.py - SocketIO Client will run on localserver. It will get request from SocketIO server and pass it to localhost.
localapp.py - Local server app running in localhost.
