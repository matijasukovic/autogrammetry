from classes.camera import Camera
from classes.turntable import Turntable
from classes.activeBuzzer import ActiveBuzzer
from gpiozero import Button
from time import sleep
import cv2
from threading import Event
import inquirer
import subprocess
import os


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

isHeavyLens = False


def main():

    camera.move('down', duration=3.75)

    print('Welcome to Autogrammetry v1.0!')

    scan_method = promptUser_scanMethod()

    image_format = promptUser_imageFormat()

    output_directory = promptUser_outputDirectory()

    metadata = promptUser_metadata()
    camera.setMetadata(metadata)
    
    print('All set, starting scan sequence.')

    steps_simple = [
        {'action': 'move', 'direction': 'up', 'duration': 3.9 if isHeavyLens else 3.3},

        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 32, 'rotation': 0.5},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},
        {'action': 'capture', 'amount': 32, 'rotation': 0.5},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'up', 'duration': 3.2 if isHeavyLens else 3},

        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},
    ]

    steps_markers = [
        {'action': 'subdirectory', 'name': 'top'},

        {'action': 'move', 'direction': 'up', 'duration': 4 if isHeavyLens else 3.3},

        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'up', 'duration': 3.4 if isHeavyLens else 3},

        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'subdirectory', 'name': 'bottom'},

        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1},
        {'action': 'capture', 'amount': 64, 'rotation': 1},
    ]

    steps_gdh = [
        {'action': 'move', 'direction': 'up', 'duration': 3.3},
        {'action': 'print', 'message': 'Position the object and scale bar on the turntable.'},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 2.3},
        {'action': 'print', 'message': 'Please remove the scale bar.'},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},

        {'action': 'move', 'direction': 'up', 'duration': 2.7},
        {'action': 'print', 'message': 'Flip the object upside-down.'},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 2.3},
        {'action': 'capture', 'amount': 48, 'rotation': 1},

        {'action': 'move', 'direction': 'down', 'duration': 1.5},
        {'action': 'print', 'message': 'Prop the object upright 90 degrees.'},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},
        {'action': 'print', 'message': 'Rotate the object clockwise 90 degrees. (1/3)'},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},
        {'action': 'print', 'message': 'Rotate the object clockwise 90 degrees. (2/3)'},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},
        {'action': 'print', 'message': 'Rotate the object clockwise 90 degrees. (3/3)'},
        {'action': 'wait', 'beep': True},
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 48, 'rotation': 1},
        {'action': 'print', 'message': 'Scanning complete.'}
    ]

    steps_manual = [
        {'action': 'wait', 'beep': False},

        {'action': 'capture', 'amount': 64, 'rotation': 1},

        {'action': 'wait', 'beep': True},

        {'action': 'loop'}
    ]

    match scan_method:
        case 'Simple':
            steps = steps_simple
        case 'Markers':
            steps = steps_markers
        case 'GDH':
            steps = steps_gdh
        case 'Manual':
            steps = steps_manual
        case _:
            raise Exception("Unknown scanning mode.")

    executeSteps(steps, image_format, output_directory)
    

def executeSteps(steps, image_format, output_directory):
    subdirectory = None

    for step in steps:
        match step.get('action'):
            case 'move':
                camera.move(step.get('direction'), duration=step.get('duration'))
                sleep(1)
            case 'capture':
                stepperMotor_totalSteps = int(turntable.fullRotationPosition * step.get('rotation'))
                stepperMotor_stepsPerImage = int(stepperMotor_totalSteps / step.get('amount'))

                counter = 0
                print("Taking images... {0}/{1}".format(counter, step.get('amount')), end="\r", flush=True)

                for stepperMotor_currentStep in range(0, stepperMotor_totalSteps, stepperMotor_stepsPerImage):
                    while turntable.running.is_set():
                        img = camera.capture()
                        
                        cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
                        cv2.imshow('Preview', img)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            
                    sleep(0.25)
                    camera.captureAndSave(format = image_format, output_dir = output_directory if not subdirectory else subdirectory)

                    counter = counter + 1
                    print("Taking images... {0}/{1}".format(counter, step.get('amount')), end="\r", flush=True)

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

            case 'print':
                print(step.get('message'))

            case 'subdirectory':
                subdirectory_name = step.get('name')
                subdirectory = os.path.join(output_directory, subdirectory_name) if subdirectory_name else None

                os.makedirs(subdirectory, exist_ok=True)
            
            case 'loop':
                executeSteps(steps, image_format, output_directory)

            case _:
                raise Exception('Invalid action.')

def promptUser_scanMethod():
    return inquirer.prompt([
        inquirer.List('method',
            message="Which scanning method would you like to use?",
            choices=[
                'Simple',
                'Markers',
                'GDH',
                'Manual'
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

def promptUser_imageFormat():
    formatMap = {
        'RAW (12-bit DNG)': 'dng',
        'JPG': 'jpg',
    }

    prompt = inquirer.prompt([
        inquirer.List('formatKey',
            message="Choose an image format",
            choices=list(formatMap.keys())
        ),
    ])

    chosenKey = prompt['formatKey']

    return formatMap[chosenKey]

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
        'f/12': '12.0',
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

    global isHeavyLens
    if metadata['EXIF:FocalLength'] == '16.0':
        isHeavyLens = True

    return metadata

if __name__ == '__main__':
    main()
    sleep(5)