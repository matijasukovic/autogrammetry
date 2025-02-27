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
        
        self.picamera.configure(self.still_config)

        print(self.picamera.camera_controls)
        self.picamera.set_controls({'ExposureTime': 34000, 'AnalogueGain': 1.0, 'Contrast': 1.3, 'Sharpness': 1.5, 'Saturation': 1.2})

        self.picamera.start()

        self.savedImage_filename = 'bottom'
        self.savedImage_index = 0
        self.savedImage_extension = '.png'

    def capture(self):
        img = self.picamera.capture_array()
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    def captureAndSave(self, output_dir='.'):
        filename = self.savedImage_filename + '_' + str(self.savedImage_index) + self.savedImage_extension
        save_path = os.path.join(output_dir, filename)

        self.picamera.capture_file(save_path)
        print('saved as: ' ,save_path) 

        self.savedImage_index += 1

    def saveImage(self, image, output_dir='.'):
        filename = self.savedImage_filename + '_' + str(self.savedImage_index) + self.savedImage_extension
        save_path = os.path.join(output_dir, filename)

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(save_path, image)

        print('saved as: ' ,save_path) 
        self.savedImage_index += 1
