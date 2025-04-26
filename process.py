from classes.camera import Camera
from classes.turntable import Turntable
from classes.activeBuzzer import ActiveBuzzer
from gpiozero import Button
from time import sleep
import cv2
from threading import Event

# Camera setup
camera = Camera()

# Turntable setup
turntable = Turntable()

# Buzzer setup
buzzer = ActiveBuzzer()

# Button setup
button = Button(19)

buttonEvent = Event()

def on_press():
    if not buttonEvent.is_set():
        buttonEvent.set()

button.when_pressed = on_press

steps_mine = [
    {'action': 'move', 'direction': 'up', 'duration': 3.5},
    {'action': 'capture', 'amount': 32, 'rotation': 0.5},
    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},
    {'action': 'capture', 'amount': 32, 'rotation': 0.5},

    {'action': 'move', 'direction': 'down', 'duration': 1.2},
    {'action': 'capture', 'amount': 64, 'rotation': 1},

    {'action': 'move', 'direction': 'down', 'duration': 1.2},
    {'action': 'capture', 'amount': 64, 'rotation': 1},

    {'action': 'move', 'direction': 'down', 'duration': 1},
    {'action': 'capture', 'amount': 64, 'rotation': 1},

    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'move', 'direction': 'up', 'duration': 3.5},
    {'action': 'capture', 'amount': 64, 'rotation': 1},

    {'action': 'move', 'direction': 'down', 'duration': 1.2},
    {'action': 'capture', 'amount': 64, 'rotation': 1},

    {'action': 'move', 'direction': 'down', 'duration': 1.2},
    {'action': 'capture', 'amount': 64, 'rotation': 1},

    {'action': 'move', 'direction': 'down', 'duration': 1},
    {'action': 'capture', 'amount': 64, 'rotation': 1},
]

steps_gdh = [
    {'action': 'move', 'direction': 'up', 'duration': 3.3},
    {'action': 'capture', 'amount': 48, 'rotation': 1},

    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'move', 'direction': 'down', 'duration': 2.5},
    {'action': 'capture', 'amount': 48, 'rotation': 1},

    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'move', 'direction': 'up', 'duration': 2.5},
    {'action': 'capture', 'amount': 48, 'rotation': 1},

    {'action': 'move', 'direction': 'down', 'duration': 2.5},
    {'action': 'capture', 'amount': 48, 'rotation': 1},

    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'move', 'direction': 'down', 'duration': 0.8},
    {'action': 'move', 'direction': 'up', 'duration': 0.1},

    {'action': 'capture', 'amount': 48, 'rotation': 1},
    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'capture', 'amount': 48, 'rotation': 1},
    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'capture', 'amount': 48, 'rotation': 1},
    {'action': 'wait', 'beep': True},
    {'action': 'wait', 'beep': False},

    {'action': 'capture', 'amount': 48, 'rotation': 1},
]

def main():
    camera.move('down', duration=3.75)

    for step in steps_gdh:
        match step.get('action'):
            case 'move':
                camera.move(step.get('direction'), duration=step.get('duration'))
                sleep(1)
            case 'capture':
                stepperMotor_totalSteps = int(turntable.fullRotationPosition * step.get('rotation'))
                stepperMotor_stepsPerImage = int(stepperMotor_totalSteps / step.get('amount'))

                print('total steps, ', stepperMotor_totalSteps)
                print('per image: ', stepperMotor_stepsPerImage)


                for stepperMotor_currentStep in range(0, stepperMotor_totalSteps, stepperMotor_stepsPerImage):
                    while turntable.running.is_set():
                        img = camera.capture()
                        
                        cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
                        cv2.imshow('Preview', img)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            
                    sleep(0.1)
                    camera.captureAndSave(raw=True, output_dir="/media/sukovicm/Matija_T9/1 Euro liberte/images/dng")

                    if stepperMotor_currentStep != stepperMotor_totalSteps:
                        turntable.startMotorStep(number_of_steps=stepperMotor_stepsPerImage, direction=1)
            case 'wait':
                if step.get('beep'): buzzer.play() 
                else: buzzer.stop()
                    
                while not buttonEvent.is_set():
                    img = camera.capture()
                        
                    cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
                    cv2.imshow('Preview', img)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break  

                buzzer.bleep()
                buttonEvent.clear()

                if step.get('beep'): buzzer.stop()
            case _:
                raise Exception('Invalid action.')

if __name__ == '__main__':
    main()