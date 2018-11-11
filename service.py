import sys, os, socket, subprocess, socket
from flask import Flask, request, Response
from functools import wraps
from AuthDB import DataBase
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'sh'

def find_service(NAME, TYPE):
    info = zeroconf.get_service_info(TYPE, NAME + '.' + TYPE)
    if info is not None:
        addr = socket.inet_ntoa(info.address)
        return str(addr)

app = Flask(__name__)
UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    ret = Auth_db.add_user(username, password)
    return ret

@app.route('/upload/<server_name>', methods=['POST'])
@requires_auth
def upload(server_name):
    
    TYPE = "_http._tcp.local."

    if (server_name == 'led'):
        NAME = "Team7LED_Rpi"
    elif (server_name == 'storage'):
        NAME = 'Team 7\'s Storage'
    addr = find_service(NAME, TYPE)
    if addr is not None:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.Popen(["bash", filename, addr])

            return "Done"
        return "Invalid file"
    return 'Could not find service'
        
        
if __name__ == "__main__":
    TYPE = "_http._tcp.local."
    #NAME = 'Team 7\'s Storage'
    #NAME = "Team7LED_Rpi"
    Auth_db = DataBase()
    zeroconf = Zeroconf()
    #find_service(NAME, TYPE)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("google.com", 80))
    host_addr = sock.getsockname()[0]
    app.run(debug=True, host=host_addr)
