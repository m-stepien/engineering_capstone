# import RPi.GPIO as GPIO
# import time

# class Motor():
#     def __init__():
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setup(16, GPIO.OUT)
#         GPIO.setup(18, GPIO.OUT)
#         GPIO.setup(22, GPIO.OUT)
#         motor_speed = GPIO.PWM(22, 1000)

#     def move_forward(speed):
#         GPIO.output(16, True)
#         GPIO.output(18, False)
#         motor_speed.ChangeDutyCycle(100)
#         time.sleep(1/100)
#         motor_speed.ChangeDutyCycle(speed)
#         time.sleep(1)
    
#     def move_backward(speed):
#         GPIO.output(16, False)
#         GPIO.output(18, True)
#         motor_speed.ChangeDutyCycle(100)
#         time.sleep(1/100)
#         motor_speed.ChangeDutyCycle(speed)
#         time.sleep(1)

#     def stop():
#         GPIO.output(16, False)
#         GPIO.output(18, False)
#         motor_speed.ChangeDutyCycle(0)

class MotorMock():

    def __init__(self):
        self.file_name = "speed"
        with open(self.file_name, "w+") as f:
            f.write("Start/n")

    def move_forward(speed):
        with open(self.file_name, "a") as f:
            f.write(speed+"/n")
    
    def move_backward(speed):
        with open(self.file_name, "a") as f:
            f.write("-"+ speed+"/n")

    def stop():
        with open(self.file_name, "a") as f:
            f.write("stop")