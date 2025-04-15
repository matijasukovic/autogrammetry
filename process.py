from classes.camera import Camera
from classes.turntable import Turntable
import cv2
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from pynput.keyboard import Key, Listener
from time import sleep
import math

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
increment = 0.8

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
    sleep(4)

    servoDelays_perStep = [0.3, 1.2, 1.2, 1.2]
    stepperSteps_perStep = 48

    for i in range(len(servoDelays_perStep)):
        # lift camera
        servo.value = increment
        sleep(servoDelays_perStep[i])
        servo.value = 0
        sleep(1)

        # for j in range(0, turntable.fullRotationPosition, stepperSteps_perStep):
        #     while turntable.running:
        #         img = camera.capture()
                
        #         cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
        #         cv2.imshow('Preview', img)

        #         if cv2.waitKey(1) & 0xFF == ord('q'):
        #             break
            

        #     sleep(0.1)
        #     camera.captureAndSave(raw=True, output_dir="/media/sukovicm/Matija_T9/test/top")

        #     if j != turntable.fullRotationPosition:
        #         turntable.startMotorStep(number_of_steps=stepperSteps_perStep, direction=1)
        #     else:
        #         # End of a cycle, move turntable slightly so that the next cycle is slightly shifted to the side
        #         shiftStep = math.floor(stepperSteps_perStep / len(servoDelays_perStep))
        #         turntable.startMotorStep(number_of_steps=shiftStep)
        
    listener.stop()
    sleep(1)

if __name__ == '__main__':
    main()