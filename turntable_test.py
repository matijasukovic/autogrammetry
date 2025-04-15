from classes.turntable import Turntable
import time

turntable = Turntable()

def main():
    while True:
        cmd = input("Enter 'start' to run motor, 'stop' to halt, or 'exit' to quit: ").strip().lower()
        if cmd == "start":
            turntable.startMotorContinuous()
        elif cmd == "stop":
            turntable.stopMotor()
        elif cmd == "exit":
            turntable.stopMotor()
            break
        else:
            print("Invalid command. Use 'start', 'stop', or 'exit'.")

if __name__ == '__main__':
    main()

# try:
#     while True:
#         steps = int(input("Enter number of steps (eg. 3072 for one full revolution): "))
#         direction = int(input("Enter direction (1 or -1): "))
#         turntable.step_motor(steps, direction)
# except KeyboardInterrupt:
#     print("Program stopped by user")
