from classes.camera import Camera
from classes.turntable import Turntable
import cv2
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from pynput.keyboard import Key, Listener
from time import sleep

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
        camera.captureAndSave()

def main():
    listener = Listener(on_press=on_press)
    listener.start()

    # place camera to lowest position
    servo.value -= increment
    sleep(7)

    for i in range(3):
        # lift camera
        servo.value = increment
        sleep(3.7 if i != 0 else 1.9)
        servo.value = 0
        sleep(1)

        for j in range(0, turntable.fullRotationPosition, 24):
            while turntable.running:
                img = camera.capture()
                
                cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
                cv2.imshow('Preview', img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            

            sleep(0.1)
            img = camera.capture()
            camera.saveImage(img, output_dir="top")
                
            cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
            cv2.imshow('Preview', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if j != turntable.fullRotationPosition:
                turntable.startMotorStep(number_of_steps=24, direction=1)
        


    listener.stop()

if __name__ == '__main__':
    main()