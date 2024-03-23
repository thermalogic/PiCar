from flask import Flask, render_template, Response, request, jsonify, stream_with_context
import RPi.GPIO as GPIO
import threading
import cv2
from components.motor import Motor
from components.stepper_motor import Stepper_Motor
from components.ultrasonic import Ultrasonic
from components.led import Led
from components.irremote import *
from components.camera import CameraStream
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

led =Led()

motor = Motor()
# stepper_motor
IN1 = 37  # GPIO 26
IN2 = 36  # GPIO 16
IN3 = 26  # GPIO 7
IN4 = 24  # GPIO 8
stepper_motor=Stepper_Motor(IN1,IN2,IN3,IN4)

ultrasonic = Ultrasonic()
ul_thread = threading.Thread(target=ultrasonic.worker,args=(motor,),daemon=True)
ul_thread.start()
ir_thread = threading.Thread(target=irremote_worker,args=(motor,led,),daemon=True)
ir_thread.start()

cap = CameraStream().start()


def gen_frame():
    """Video streaming generator function."""
    while cap:
        frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result


app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/data')
def data():
    def generate_data():
        while True:
           json_data = json.dumps({'value': ultrasonic.distance})
           yield f"data:{json_data}\n\n"
           time.sleep(0.3)

    response = Response(stream_with_context(
        generate_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("index.html")


@app.route('/car_action', methods=['GET'])
def car_action():
    m_action = int(request.args.get('action'))
    motor.action(m_action)
    led.action(m_action)
    return jsonify({'motor status':m_action})


@app.route('/speed', methods=['GET'])
def speed():
    speed = request.args.get('speed')
    motor.adjust_speed(int(speed))
    return jsonify({'speed': speed})


@app.route('/turn_speed', methods=['GET'])
def turn_speed():
    turn_speed = request.args.get('turn_speed')
    motor.adjust_turn_speed(int(turn_speed))
    return jsonify({'turn_speed': turn_speed})


@app.route('/stepper_motor_action', methods=['GET'])
def stepper_motor_action():
    stepper_motor_action = int(request.args.get('action'))
    stepper_motor.action(stepper_motor_action)
    return jsonify({'stepper motor status':stepper_motors_action})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
    cv2.destroyAllWindows()
    GPIO.cleanup()
