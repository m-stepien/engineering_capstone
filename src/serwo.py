from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

SERVO_CONTROL_PIN = 12
MIN_PULSE_WIDTH = 0.4/1000
MAX_PULSE_WIDTH = 2.6/1000

class Servo(AngularServo):
    def __init__(self):
        super().__init__(SERVO_CONTROL_PIN, min_pulse_width=MIN_PULSE_WIDTH, max_pulse_width=MAX_PULSE_WIDTH, pin_factory=PiGPIOFactory())
        self.initial_position = -12
        self.move(0)

    def move(self, angle):
        self.angle=self.initial_position + angle
        

class ServoMock():
    def __init__():
        self.file_name = "serwo_angle.txt"
        with open(self.file_name, "w+") as f:
            f.write("Start\n")
    
