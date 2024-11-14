import RPi.GPIO as GPIO
import time

class Motor():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        self.motor_speed = GPIO.PWM(33, 1000)
        self.motor_speed.start(0)

    def move_forward(self,speed):
        GPIO.output(16, True)
        GPIO.output(18, False)
        self.motor_speed.ChangeDutyCycle(100)
        time.sleep(1/100)
        self.motor_speed.ChangeDutyCycle(speed)
        time.sleep(0.1)
        self.stop()

    def move_backward(self,speed):
        GPIO.output(16, False)
        GPIO.output(18, True)
        self.motor_speed.ChangeDutyCycle(100)
        time.sleep(1/100)
        self.motor_speed.ChangeDutyCycle(speed)
        time.sleep(0.1)
        self.stop()

    def stop(self):
        GPIO.output(16, False)
        GPIO.output(18, False)
        self.motor_speed.ChangeDutyCycle(0)

    def cleanup(self):
        GPIO.cleanup()

    def __del__(self):
        self.stop()
        self.cleanup()


# motor = Motor()
# motor.move_forward(50)  
# time.sleep(2) 
# motor.move_backward(50) 
# time.sleep(2)
# motor.stop()  
# motor.cleanup()
