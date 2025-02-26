from gpiozero import OutputDevice
from time import sleep
import threading

class Turntable:
    def __init__(self):
        self.IN1 = OutputDevice(14)
        self.IN2 = OutputDevice(15)
        self.IN3 = OutputDevice(18)
        self.IN4 = OutputDevice(23)

        self.running = False
        self.direction = 1
        self.delay = 0.001

        self.position = 0
        self.fullRotationPosition = 3072

        self.step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
    
    def setStep(self, w1, w2, w3, w4):
        self.IN1.value = w1
        self.IN2.value = w2
        self.IN3.value = w3
        self.IN4.value = w4

    def updatePosition(self, direction):
        if self.position == self.fullRotationPosition and direction == 1:
            self.position = 1
        elif self.position == 0 and direction == -1:
            self.position = self.fullRotationPosition - 1
        else:
            self.position += direction

    def stepMotor(self, number_of_steps=24, direction=1):
        for _ in range(number_of_steps):
            if not self.running:
                print('stepMotor action stopped externally')
                return
            
            for step in (self.step_sequence if direction > 0 else reversed(self.step_sequence)):
                self.setStep(*step)
                self.updatePosition(direction)
                sleep(self.delay)

        self.stopMotor()

    def startMotorStep(self, number_of_steps=24, direction = 1):
        self.direction = direction
        
        self.running = True
        thread = threading.Thread(target = self.stepMotor, daemon = True, args=(number_of_steps, direction))
        thread.start()

    def startMotorContinuous(self, direction = 1):
        self.direction = direction
        
        if self.running:
            return
        
        self.running = True
        thread = threading.Thread(target = self.continuous, daemon = True)
        thread.start()

    def stopMotor(self):
        self.running = False


    def continuous(self):
        while self.running:
            for step in (self.step_sequence if self.direction > 0 else reversed(self.step_sequence)):
                self.setStep(*step)
                sleep(self.delay)