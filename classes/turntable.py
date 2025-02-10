from gpiozero import OutputDevice
from time import sleep

class Turntable:
    def __init__(self):
        self.IN1 = OutputDevice(14)
        self.IN2 = OutputDevice(15)
        self.IN3 = OutputDevice(18)
        self.IN4 = OutputDevice(23)

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
    
    def set_step(self, w1, w2, w3, w4):
        self.IN1.value = w1
        self.IN2.value = w2
        self.IN3.value = w3
        self.IN4.value = w4

    def step_motor(self, number_of_steps, direction=1, delay=0.0007):
        for _ in range(number_of_steps):
            for step in (self.step_sequence if direction > 0 else reversed(self.step_sequence)):
                self.set_step(*step)
                sleep(delay)