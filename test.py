from classes.camera import Camera
from classes.turntable import Turntable
import cv2
from pynput.keyboard import Key, Listener

# Camera setup
camera = Camera()

# Turntable setup
turntable = Turntable()

def on_press(key):
    global speed
    global increment

    if key == Key.up:
        camera.move('up', duration=0.5)
    elif key == Key.down:
        camera.move('down', duration=0.5)
    elif key == Key.left:
        if turntable.running.is_set() and turntable.direction == -1:
            turntable.stopMotor()
        else:
            turntable.startMotorContinuous(direction = 1)
    elif key == Key.right:
        if turntable.running.is_set() and turntable.direction == 1:
            turntable.stopMotor()
        else:
            turntable.startMotorContinuous(direction = -1)
    elif key == Key.space:
        print('Capturing image...')
        camera.captureAndSave(format='jpg')

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