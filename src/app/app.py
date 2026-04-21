from flask import Flask, render_template, jsonify, request

# ======================= Socket code =======================

IS_IN_CONTAINER = True
ADDRESS = "0.0.0.0"
PORT = 2024

sock_thread = None


try:
    from lib.communication import communication
    from lib.server_codes import *

    sock_thread = communication((ADDRESS, PORT), "sock_thread", target_address=("host.docker.internal", PORT))

except ImportError as e:
    print(e)
    print("app is not running in container")
    IS_IN_CONTAINER = False

ALL_SERVERS = sock_thread.send_recv(Server_codes.ALL_SERVERS)

# ======================= Server code =======================

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/backend/server_count", methods=["GET"])
def backend_servercount():
    if (IS_IN_CONTAINER):
        data = sock_thread.send_recv(Server_codes.SERVER_COUNT)
        return jsonify(message=data), 200
    return jsonify(message=None), 404

@app.route("/backend/all_servers", methods=["GET"])
def backend_allservers():
    if (IS_IN_CONTAINER):
        return jsonify(message=ALL_SERVERS), 200
    return jsonify(message=None), 404

@app.route("/backend/all_running_servers", methods=["GET"])
def backend_all_running_servers():
    if (IS_IN_CONTAINER):
        data = sock_thread.send_recv(Server_codes.RUNNING_SERVERS)
        return jsonify(message=data), 200
    return jsonify(message=None), 404



@app.route("/backend/start_up", methods=["POST"])
def backend_start_up():
    if (IS_IN_CONTAINER):
        sock_thread.send(request.form.get("name"), code=Server_codes.START_SERVER,)
        return jsonify(message=":)"), 200
    return jsonify(message=None), 404