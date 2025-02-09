from gpiozero import OutputDevice
from time import sleep

IN1 = OutputDevice(14)
IN2 = OutputDevice(15)
IN3 = OutputDevice(18)
IN4 = OutputDevice(23)

step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def set_step(w1, w2, w3, w4):
    IN1.value = w1
    IN2.value = w2
    IN3.value = w3
    IN4.value = w4

def step_motor(steps, direction=1, delay=0.001):
    for _ in range(steps):
        for step in (step_sequence if direction > 0 else reversed(step_sequence)):
            set_step(*step)
            sleep(delay)

try:
    while True:
        steps = int(input("Enter number of steps (eg. 3072 for one full revolution): "))
        direction = int(input("Enter direction (1 or -1): "))
        step_motor(steps, direction)
except KeyboardInterrupt:
    print("Program stopped by user")
