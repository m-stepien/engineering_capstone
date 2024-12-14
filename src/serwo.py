from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import threading

SERVO_CONTROL_PIN = 12
MIN_PULSE_WIDTH = 0.4/1000
MAX_PULSE_WIDTH = 2.6/1000

class Servo(AngularServo):
    def __init__(self):
        super().__init__(SERVO_CONTROL_PIN, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH, pin_factory=PiGPIOFactory())
        self.position = 0
        self.move(self.position)
        self.go_to = 0
        self.step = 1
        self.pause = 0.05
        self.current_work = None
        self.running = False

    def move(self, angle):
        while self.running:
            if self.position < self.go_to:
                self.position += self.step
            elif self.position > self.go_to:
                self.position -= self.step
            sleep(self.pause)
    

    def start_go_to(self, angle):
        if self.current_work is None:
            self.running = True
            self.current_work = threading.Thread(target=self.move, daemon=True)
            self.current_work.start()
        self.go_to = angle


#ewentualne dołożenie dynamicznej zmiany stepu


#testy na szybko
servo = Servo()
servo.start_go_to(40)
sleep(3)
servo.start_go_to(-40)
sleep(3)


# servo.start_go_to(40)
# sleep(1)
# servo.start_go_to(-40)
# sleep(1)

# servo.start_go_to(40)
# sleep(0.20)
# servo.start_go_to(-40)
# sleep(3)
