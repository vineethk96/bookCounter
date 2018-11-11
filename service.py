import sys
from flask import Flask, request, Response
from functools import wraps
from AuthDB import DataBase
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import socket



def find_service(NAME, TYPE):
    info = zeroconf.get_service_info(TYPE, NAME + '.' + TYPE)
    addr = socket.inet_ntoa(info.address)
    print(addr)
    return addr

app = Flask(__name__)

def check_auth(username, password):
    return Auth_db.authenticate(username, password)
def authenticate():
    return Response(
        'Authentication Fail', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/add_user', methods = ['POST'])
def new_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    Auth_db.add_user(username, password)
    return username + ' ' + password

@app.route('/upload/<server_name>', methods=['POST'])
@requires_auth
def upload(server_name):
    TYPE = "_http._tcp.local."
    #browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", handlers=[on_change])
    if (server_name == 'led'):
        NAME = "LED"
    elif (server_name == 'storage'):
        NAME = 'Team 7\'s Storage'
        addr = find_service(NAME, TYPE)

if __name__ == "__main__":
    TYPE = "_http._tcp.local."
    #NAME = 'Team 7\'s Storage'
    NAME = "Team7LED_Rpi"
    Auth_db = DataBase()
    zeroconf = Zeroconf()
    find_service(NAME, TYPE)
    app.run(debug=True, host='localhost')
