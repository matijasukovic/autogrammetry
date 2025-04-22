from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

class ContinuousServo:
    def __init__(self, pin=17):
        self.speed = 0

        factory = PiGPIOFactory()

        # Defaults are 1/1000 and 2/2000
        minimumPulseWidth = 0.5/1000
        maximumPulseWidth = 2.5/1000

        self.servo = Servo(
            pin, 
            pin_factory=factory,
            min_pulse_width=minimumPulseWidth,
            max_pulse_width=maximumPulseWidth
        )

    def setSpeed(self, speed):
        if speed < -1 or speed > 1:
            raise Exception('Servo speed can only be a value betweeen -1 and 1.')
        
        self.speed = speed
        self.servo.value = self.speed

    def setSpeed_forDuration(self, speed, duration):
        self.setSpeed(speed)
        sleep(duration)
        self.setSpeed(0)
    
