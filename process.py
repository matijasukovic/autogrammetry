from classes.camera import Camera
from classes.turntable import Turntable
from classes.activeBuzzer import ActiveBuzzer
from gpiozero import Button
from time import sleep
import cv2
from threading import Event
import inquirer
import subprocess


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

steps_simple = [
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

    print('Welcome to Autogrammetry v1.0!')

    scan_method = promptUser_scanMethod()

    outputDirectory = promptUser_outputDirectory()

    metadata = promptUser_metadata()
    camera.setMetadata(metadata)
    
    print('Ready to start!')

    match scan_method:
        case 'Simple':
            steps = steps_simple
        case 'GDH':
            steps = steps_gdh
        case _:
            raise Exception("I don't even remember how I got here")


    for step in steps:
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
                    camera.captureAndSave(raw=True, output_dir=outputDirectory)

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

                buttonEvent.clear()

                if step.get('beep'): buzzer.stop()
                buzzer.bleep()
            case _:
                raise Exception('Invalid action.')

def promptUser_scanMethod():
    return inquirer.prompt([
        inquirer.List('method',
            message="Which scanning method would you like to use?",
            choices=[
                'Simple',
                'GDH'
            ],
        ),
    ])['method']

def promptUser_outputDirectory():
    print('[?] Choose a directory for storing images.')

    while True:
        result = subprocess.run(
            ['zenity', '--file-selection', '--directory', '--title=Select a directory to save images in'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            path = result.stdout.strip()
            print(" > {0}\n".format(path))
            return path

def promptUser_metadata():
    focalLengthMap = {
        '8.0mm': '8.0',
        '16.0mm': '16.0',
        '25.0mm': '25.0',
    }

    fNumberMap = {
        'f/1.4': '1.4',
        'f/2.1': '2.1',
        'f/2.8': '2.8',
        'f/3.4': '3.4',
        'f/4': '4.0',
        'f/5.6': '5.6',
        'f/8': '8.0',
        'f/16': '16.0'
    }

    metadata = inquirer.prompt([
        inquirer.List('EXIF:FocalLength',
            message="Lens focal length",
            choices=list(focalLengthMap.keys())
        ),
        inquirer.List('EXIF:FNumber',
            message="Lens F number",
            choices=list(fNumberMap.keys())
        ),
        inquirer.Text('EXIF:LensModel', message="Lens model (Optional)"),
        inquirer.Text('EXIF:Artist', message="Artist (Optional)"),
        inquirer.Text('EXIF:Copyright', message="Copyright holder (eg. 'British Museum', leave blank if for personal use)"),
    ])

    metadata['EXIF:FocalLength'] = focalLengthMap[metadata['EXIF:FocalLength']]
    metadata['EXIF:FNumber'] = fNumberMap[metadata['EXIF:FNumber']]

    return metadata

if __name__ == '__main__':
    main()