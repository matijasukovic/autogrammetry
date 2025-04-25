from gpiozero import Buzzer
from time import sleep
from threading import Thread

class ActiveBuzzer:
    STEPS_WAITING = [
        {'on': True, 'duration': 1},
        {'on': False, 'duration': 1},           
        {'on': True, 'duration': 1},
        {'on': False, 'duration': 2},
        {'on': False, 'duration': 2},
        {'on': False, 'duration': 2},
        {'on': False, 'duration': 2},
        {'on': False, 'duration': 2},
    ]
    
    def __init__(self, pin=26):
        self.buzzer = Buzzer(pin)

        self.isPlaying = False

        self.thread_playing = Thread(target = self.noiseLoop, daemon = True)
        self.thread_playing.start()

    def executeSoundSequence(self, steps=STEPS_WAITING):
        for step in steps:
            if not self.isPlaying:
                return
            
            if step.get('on'):
                self.buzzer.on()
            else:
                self.buzzer.off()
            sleep(step.get('duration'))

    def bleep(self):
        self.buzzer.beep(on_time=0.05, off_time=0.05, n=1)

    def noiseLoop(self):
        while True:
            if self.isPlaying:
                self.executeSoundSequence()
    
    def play(self):
        print('play')
        self.isPlaying = True

    def stop(self):
        print('stop')
        self.isPlaying = False
        self.buzzer.off()
        
    



