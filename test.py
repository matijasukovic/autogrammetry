from classes.camera import Camera
from classes.turntable import Turntable
import cv2
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from pynput.keyboard import Key, Listener

# Camera setup
camera = Camera()

# Turntable setup
turntable = Turntable()

# Servo setup
factory = PiGPIOFactory()

# Defaults are 1/1000 and 2/2000
minimumPulseWidth = 0.5/1000
maximumPulseWidth = 2.5/1000

servo = Servo(
    17, 
    pin_factory=factory,
    min_pulse_width=minimumPulseWidth,
    max_pulse_width=maximumPulseWidth
)

speed = 0
increment = 0.24
def on_press(key):
    global speed
    global increment

    if key == Key.up:
        speed += increment
        servo.value = speed
    elif key == Key.down:
        speed -= increment
        servo.value = speed
    elif key == Key.left:
        if turntable.running and turntable.direction == -1:
            turntable.stopMotor()
        else:
            turntable.startMotorContinuous(direction = 1)
    elif key == Key.right:
        if turntable.running and turntable.direction == 1:
            turntable.stopMotor()
        else:
            turntable.startMotorContinuous(direction = -1)
    elif key == Key.space:
        camera.captureAndSave(raw=True)

def main():
    listener = Listener(on_press=on_press)
    listener.start()

    while True:
        img = camera.capture()
        cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
        cv2.imshow('Preview', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    listener.stop()

if __name__ == '__main__':
    main()