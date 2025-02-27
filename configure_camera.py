import cv2
from classes.camera import Camera
from pynput.keyboard import Listener

# Initialize camera
camera = Camera()

# Default camera settings
controls = {'ExposureTime': 39000, 'AnalogueGain': 1.0, 'Contrast': 1.3, 'Sharpness': 1.5, 'Saturation': 1.3}

camera.picamera.set_controls(controls)


def on_press(key):
    if key.char == 'e':
        controls["ExposureTime"] = min(controls["ExposureTime"] + 1000, 200000)
        camera.picamera.set_controls(controls) 
        print(f"Increased ExposureTime: {controls}")
    elif key.char == 'r':
        controls["ExposureTime"] = max(controls["ExposureTime"] - 1000, 1000)
        camera.picamera.set_controls(controls) 
        print(f"Decreased ExposureTime: {controls}")
    elif key.char == 'd':
        controls["Contrast"] = min(controls["Contrast"] + 0.1, 32)
        camera.picamera.set_controls(controls) 
        print(f"Increased Contrast: {controls}")
    elif key.char == 'f':
        controls["Contrast"] = max(controls["Contrast"] - 0.1, 0)
        camera.picamera.set_controls(controls) 
        print(f"Decreased Contrast: {controls}")
    elif key.char == 'g':
        controls["Sharpness"] = min(controls["Sharpness"] + 0.1, 16.0)
        camera.picamera.set_controls(controls) 
        print(f"Increased Sharpness: {controls}")
    elif key.char == 'h':
        controls["Sharpness"] = max(controls["Sharpness"] - 0.1, 0.0)
        camera.picamera.set_controls(controls) 
        print(f"Decreased Sharpness: {controls}")
    elif key.char == 'b':
        controls["Saturation"] = min(controls["Saturation"] + 0.1, 32.0)
        camera.picamera.set_controls(controls) 
        print(f"Increased Saturation: {controls}")
    elif key.char == 'n':
        controls["Saturation"] = max(controls["Saturation"] - 0.1, 0.0)
        camera.picamera.set_controls(controls) 
        print(f"Decreased Saturation: {controls}")
    elif key.char == 'q':
        cv2.destroyAllWindows()
        camera.picamera.stop()

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


