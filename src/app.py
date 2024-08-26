from flask import Flask, Response, jsonify, send_file, redirect, render_template
from flask import request, session, flash, url_for
from functools import wraps
from wireguardconfig import WireguardConfigJson
from qr import qr_generator
import json
import io
import os
from config import PASSWORD
from password import set_password

app = Flask(__name__)
config: WireguardConfigJson | None = None

app.secret_key = os.urandom(24) 


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #username = request.form['username']
        password = request.form['password']
        
        if set_password(password) == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/api/save', methods=['GET', 'POST'])
@login_required
def save_data():
    global config
    os.system("wg-quick down wg0")
    with open("/etc/wireguard/wg0.conf", "w", encoding="utf-8") as fh:
        print(config, file=fh)
    with open("wg0.json", "w", encoding="utf-8") as fh:
        print(repr(config), file=fh)
    os.system("wg-quick up wg0")
    return Response(status=200)

@app.route('/api/session', methods=['GET']) #@app.before_request
@login_required
def create_session():
    global config
    try:
        with open("wg0.json", 'r', encoding="utf-8") as file:
            config_data = json.load(file)
            config = WireguardConfigJson(config_data)
    except:
        config = WireguardConfigJson(None)
    
    return Response(status=200)

@app.route('/api/wireguard/client', methods=['GET'])
@login_required
def get_clients():
    global config
    return jsonify(config.devices())

@app.route('/api/wireguard/client/<name>', methods=['POST'])
@login_required
def create_client(name):
    global config
    device = config.add_device(name, enabled=True)
    save_data()
    return jsonify(device)

@app.route('/api/wireguard/client/<client_id>', methods=['DELETE'])
@login_required
def delete_client(client_id):
    config.remove_device(client_id)
    save_data()
    return Response(status=200)

@app.route('/api/wireguard/client/<client_id>/enable/<state>', methods=['POST'])
@login_required
def enable_client(client_id, state):
    global config
    config.enable_device(client_id, state)
    save_data()
    return Response(status=200)


@app.route('/api/wireguard/client/<client_id>/disable', methods=['POST'])
@login_required
def disable_client(client_id):
    global config
    config.enable_device(client_id, False)
    return redirect("/api/save")


@app.route('/api/wireguard/client/<client_id>/configuration', methods=['GET', 'POST'])
@login_required
def download_configuration(client_id):
    global config
    file_content = config.to_device(client_id)
    name = [peer["name"] for peer in config.peers if peer["id"]==client_id][0]
    file_name = f"{name}.conf"
    
    file_obj = io.BytesIO()
    file_obj.write(file_content.encode('utf-8'))
    file_obj.seek(0)
    
    return send_file(file_obj, as_attachment=True, download_name=file_name, mimetype='text/plain')

@app.route('/api/wireguard/client/<client_id>/qrcode', methods=['GET', 'POST'])
@login_required
def qrcode_generator(client_id):
    global config
    qrcode_content = config.to_device(client_id)
    qr_img = qr_generator(qrcode_content)
    
    file_obj = io.BytesIO()
    file_obj.write(qr_img)
    file_obj.seek(0)

    return send_file(file_obj, mimetype='image/png')
   

@app.route('/api/wireguard/client/<client_id>/address', methods=['PUT'])
@login_required
def update_client_address(client_id):
    return None


@app.route('/api/wireguard/restore', methods=['PUT'])
@login_required
def restore_configuration():
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
