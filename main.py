from gpiozero import LED, Button
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from time import sleep
from threading import Thread

THREAD = Thread()
# SocketIO guide - https://www.youtube.com/watch?v=RdSrkkrj3l4

app = Flask(__name__)
app.config['SECRET_KEY'] = "Some-Secret"
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





@socketio.on('connect', namespace='/alert')
def sendSwitchData():
    #GPIO.add_event_detect(17,GPIO.RISING,callback=button_callback)
    global THREAD
    if not THREAD.isAlive():
        THREAD = ButtonThread()
        THREAD.start()

@app.route("/")
def welcome():
    return render_template('index.html')


#side med socket og liste over api calls
@app.route("/settings")
def settings():
    return render_template('settings.html')

#create account
@app.route("/signup", methods=['POST'])
def signuppage():
    return render_template('signup.html')

#return status of button
@app.route("/button", methods=['GET'])
def buttonState():
    if not button.is_pressed: #Vi bruger active Low, Denne kigger for Active High
        return "True"
    else:
        return "False"

#turn LED on or off
@app.route("/led/<action>", methods=['POST'])
def toggleLED(action):
    if action == "toggle":
        led.toggle()
        return "toggled LED"
    if action == "on":
        led.on()
        return "LED turned on"
    elif action == "off":
        led.off()
        return "LED turned off"
    else:
        return "unknow action"




if __name__ == '__main__':
    socketio.run(app)
