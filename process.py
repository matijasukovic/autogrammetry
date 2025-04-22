from classes.camera import Camera
from classes.turntable import Turntable
from time import sleep
import cv2
import math

# Camera setup
camera = Camera()

# Turntable setup
turntable = Turntable()

def main():
    camera.move('down', duration=3.5)

    cameraMovementDurations = [0.1, 1.2, 1.1, 0.9]
    stepperSteps_perStep = 48

    for i in range(len(cameraMovementDurations)):
        camera.move('up', duration=cameraMovementDurations[i])
        sleep(1)

        for j in range(0, turntable.fullRotationPosition, stepperSteps_perStep):
            while turntable.running:
                img = camera.capture()
                
                cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
                cv2.imshow('Preview', img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            sleep(0.1)
            camera.captureAndSave(raw=True, output_dir="/home/sukovicm/temp")

            if j != turntable.fullRotationPosition:
                turntable.startMotorStep(number_of_steps=stepperSteps_perStep, direction=1)


if __name__ == '__main__':
    main()