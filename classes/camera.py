from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import os
from PIL import Image

class Camera:
    def __init__(self):
        self.picamera = Picamera2()

        self.still_config = self.picamera.create_still_configuration(
            raw={"size": (4056, 3040)},
        )

        self.custom_controls = {'ExposureTime': 19000, 'AnalogueGain': 1.0, 'Contrast': 1.0, 'Sharpness': 1.0, 'Saturation': 1.0, 'AwbMode': 0}
        
        self.picamera.configure(self.still_config)

        print(self.picamera.camera_controls)
        self.picamera.set_controls(self.custom_controls)

        self.picamera.start()

        self.savedImage_filename = 'top'
        self.savedImage_index = 0
        self.savedImage_extension = '.png'

    def capture(self):
        img = self.picamera.capture_array()
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    def captureAndSave(self, output_dir='.', raw=False):
        extension = '.dng' if raw else self.savedImage_extension
            
        filename = self.savedImage_filename + '_' + str(self.savedImage_index) + extension
        save_path = os.path.join(output_dir, filename)

        self.picamera.capture_file(save_path, 'raw' if raw else None) 
        print('saved as: ' ,save_path) 

        self.savedImage_index += 1

    def saveImage(self, image, output_dir='.'):
        filename = self.savedImage_filename + '_' + str(self.savedImage_index) + self.savedImage_extension
        save_path = os.path.join(output_dir, filename)

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(save_path, image)

        print('saved as: ' ,save_path) 
        self.savedImage_index += 1

    def stop(self):
        self.picamera.stop()
