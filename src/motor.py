import RPi.GPIO as GPIO
import threading
import time

class Motor():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        self.motor_speed = GPIO.PWM(33, 1000)
        self.motor_speed.start(0)
        self.current_speed = 0
        self.target_speed = 0
        self.step_time = 0.05
        self.immediate_change = False
        self.running = True
        self.current_work = threading.Thread(target=self.speed_modifier, daemon=True)
        self.current_work.start()
        self.current_direction = 0
    

    def move_forward(self,speed):
        if self.current_direction==-1:
            self.stop()
        GPIO.output(16, False)
        GPIO.output(18, True)
        self.target_speed = speed
        self.current_direction = 1


    def move_backward(self,speed):
        if self.current_direction==1:
            self.stop()
        GPIO.output(16, True)
        GPIO.output(18, False)
        self.target_speed = speed
        self.current_direction=-1
    

    def speed_modifier(self):
        print("speed modifier start")
        while self.running:
            print("speed modifier alive")
            if self.immediate_change:
                print("speed modifier on immediate change")
                self.current_speed = 0
                self.immediate_change = False
            else:
                print("speed modifier in else")
                if self.current_speed < 50 and self.current_speed < self.target_speed and self.direction != 0:
                    print("speed modifier in boost")
                    self.motor_speed.ChangeDutyCycle(100)
                    time.sleep(0.01)
                if self.current_speed < self.target_speed:
                    print("speed modifier in current less then target")
                    self.current_speed+=1
                elif self.current_speed > self.target_speed:
                    print("speed modifier in current greater then target")
                    self.current_speed-=1
            print("speed modifier outside if tree")
            self.motor_speed.ChangeDutyCycle(self.current_speed)
            time.sleep(self.step_time)
            print("speed modifier after everything")
        

    def stop(self):
        GPIO.output(16, False)
        GPIO.output(18, False)
        self.immediate_change = True
        self.target_speed = 0
        self.current_direction = 0


    def get_current_direction(self):
        return self.current_direction


    def get_current_speed(self):
        return self.current_speed


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
