# coding=utf-8
from gpiozero import LED, Button
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from time import sleep
from threading import Thread
import datetime

# SocketIO guide - https://www.youtube.com/watch?v=RdSrkkrj3l4
# JWT guide - https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/

THREAD = Thread()

app = Flask(__name__)
app.config['SECRET_KEY'] = "Some-Secret"
app.config['JWT_SECRET_KEY'] = "super-secret"
jwt = JWTManager(app)
socketio = SocketIO(app)
led = LED(18)
button = Button(17)

# Thread til at kunne holde øje med en event på hardware knappen uden at stoppe Flask
class ButtonThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 0.5
        super(ButtonThread, self).__init__()

    def get_data(self):
        """
        Get data and emit to socket
        """
        switchSate = False
        while True:
            button.wait_for_release()
            if not switchSate:
                socketio.emit('message', {'buttonState': 1}, namespace='/alert')
                switchSate = True
            if button.is_pressed and switchSate:
                socketio.emit('message', {'buttonState': 0}, namespace='/alert')
                switchSate = False

    def run(self):
        """Default run method"""
        self.get_data()


# Tjekker om der er en bruger ved
def user_exists(username, mode='r'):
    try:
        f = open("users/"+username, mode)
        f.close()
    except IOError:
        return False
    return True

def create_user(username,password):
    try:
        f = open("users/"+username, mode="a+")
        f.write(password)
        f.close()
    except IOError:
        return False
    return True

def get_user_password(username):
    f = open("users/"+username, mode="r")
    password = f.read()
    f.close()
    return password


@socketio.on('connect', namespace='/alert')
def sendSwitchData():
    #GPIO.add_event_detect(17,GPIO.RISING,callback=button_callback)
    global THREAD
    if not THREAD.isAlive():
        THREAD = ButtonThread()
        THREAD.start()

# simpel homepage for grafisk adgang til api.
@app.route("/")
def welcome():
    return render_template('index.html')


#side med socket og liste over api calls
@app.route("/settings")
def settings():
    return render_template('settings.html')

#login - taken from jwt guide and modifide
@app.route("/login", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if not user_exists(username):
        return jsonify({"msg": "User does not exist"}), 401

    if not password == get_user_password(username):
        return jsonify({"msg": "Wrong password"}), 401

    # Identity can be any data that is json serializable
    expires = datetime.timedelta(seconds=120) #udløber efter 2 minuter så brugeren skal lave en ny
    access_token = create_access_token(identity=username, expires_delta=expires)
    return jsonify(access_token=access_token), 200

#registers a new user
@app.route("/register", methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if user_exists(username):
        return jsonify({"msg": "Username is taken"}), 401

    create_user(username,password)

    return jsonify({"msg": "User succesfully registerd"}), 200



#return status of button
@app.route("/button", methods=['GET'])
def buttonState():
    if not button.is_pressed: #Vi bruger active Low, Denne kigger for Active High
        return "True"
    else:
        return "False"

#turn LED on or off
@app.route("/led/<action>", methods=['POST'])
@jwt_required
def toggleLED(action):
    if action == "toggle":
        led.toggle()
        return jsonify({"msg": "LED toggled"}), 200
    if action == "on":
        led.on()
        return jsonify({"msg": "LED on"}), 200
    elif action == "off":
        led.off()
        return jsonify({"msg": "LED off"}), 200
    else:
        return jsonify({"msg": "Unknow action"}), 200




if __name__ == '__main__':
    socketio.run(app)
