from picamera2 import Picamera2
import cv2
import os
from classes.continuous_servo import ContinuousServo
import exiftool
from multiprocessing import Process, Queue
from datetime import datetime
from time import sleep

class Camera:
    def __init__(self):
        self.servo = ContinuousServo(pin=17)
        self.SERVO_UP_SPEED = 0.75
        self.SERVO_DOWN_SPEED = -0.45

        self.COLOUR_GAINS_FOLDIO2PLUS = (3.0880589485168457, 1.4724000692367554)

        self.savedImage_filename = 'image'
        self.savedImage_index = 0

        self.metadata = {
            "EXIF:Manufacturer": "RaspberryPi",
            "EXIF:Model": "Raspberry Pi HQ Camera",
            "EXIF:UserComment": "Shot with Autogrammetry v1.0",
            "EXIF:Flash": "0"
        }

        self.picamera = Picamera2()

        self.still_config = self.picamera.create_still_configuration(
            raw={"size": (4056, 3040)},
        )
        
        self.picamera.configure(self.still_config)

        self.picamera.start()

        print(type(self.COLOUR_GAINS_FOLDIO2PLUS))

        self.custom_controls = {
            'ExposureTime': 120000, 
            'AnalogueGain': 1.0, 
            'AwbEnable': False,
            'ColourGains': self.COLOUR_GAINS_FOLDIO2PLUS
        }

        sleep(2)
        self.picamera.set_controls(self.custom_controls)

        self.metadataEditQueue = Queue()
        self.metadataEditWorker = Process(target=self.exif_worker, args=(self.metadataEditQueue, self.metadata), daemon=True)
    
    def capture(self):
        img = self.picamera.capture_array()
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    def captureAndSave(self, output_dir='.', format='jpg'):
            
        filename = "{0}_{1}.{2}".format(self.savedImage_filename, str(self.savedImage_index), format)
        save_path = os.path.join(output_dir, filename)

        self.picamera.capture_file(save_path, 'raw' if format == 'dng' else None) 

        self.savedImage_index += 1
        self.metadataEditQueue.put(save_path)

    def move(self, direction='up', duration=1):
        match direction:
            case 'up':
                speed = self.SERVO_UP_SPEED
            case 'down':
                speed = self.SERVO_DOWN_SPEED
            case _:
                raise Exception('Invalid direction.')
        
        self.servo.setSpeed_forDuration(speed, duration)
        return

    def stop(self):
        self.picamera.stop()

    def setMetadata(self, metadata):
        now = datetime.now()

        copyrightHolder = metadata['EXIF:Copyright']
        artist = metadata['EXIF:Artist']
        if copyrightHolder:
            metadata['EXIF:Copyright'] = "Copyright {0} {1}. All rights reserved.".format(now.year, copyrightHolder)
        elif artist:
            metadata['EXIF:Copyright'] = "Copyright {0} {1}. All rights reserved.".format(now.year, artist)

        for key, value in metadata.items():
            self.metadata[key] = value

        self.metadataEditWorker.start()

    def exif_worker(self, queue, metadata):
        with exiftool.ExifTool() as et:

            while True:
                file_path = queue.get()

                if file_path is None:
                    break

                metadata['EXIF:DateTimeOriginal'] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

                args = [f"-{tag}={value}" for tag, value in metadata.items()]
                et.execute(b"-overwrite_original", *args, file_path)
