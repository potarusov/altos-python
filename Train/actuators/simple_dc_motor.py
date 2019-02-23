__author__ = 'POTABONNIER'

import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import config

class SimpleDCMotor:
    def __init__(self, pin_forward, pin_backward):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """

        self.pin_forward = pin_forward
        self.pin_backward = pin_backward
        self.reverse_delay = config.delay

        GPIO.setup(self.pin_forward, GPIO.OUT)
        GPIO.setup(self.pin_backward, GPIO.OUT)
        GPIO.output(self.pin_forward, GPIO.LOW)
        GPIO.output(self.pin_backward, GPIO.LOW)
        PWM.start(self.pin_forward, 0.0)
        PWM.start(self.pin_backward, 0.0)

    def forward(self, speed):
        """ pin_forward is the forward Pin, so we change its duty
             cycle according to speed. """
        GPIO.output(self.pin_forward, GPIO.LOW)
        GPIO.output(self.pin_backward, GPIO.LOW)
        PWM.set_duty_cycle(self.pin_backward, 0.0)
        time.sleep(self.reverse_delay)
        print("Forward")
        GPIO.output(self.pin_forward, GPIO.HIGH)
        PWM.set_duty_cycle(self.pin_forward, speed)

    def backward(self, speed):
        """ pin_backward is the backward Pin, so we change its duty
             cycle according to speed. """
        GPIO.output(self.pin_forward, GPIO.LOW)
        GPIO.output(self.pin_backward, GPIO.LOW)
        PWM.set_duty_cycle(self.pin_forward, 0.0)
        time.sleep(self.reverse_delay)
        print("Backward")
        GPIO.output(self.pin_backward, GPIO.HIGH)
        PWM.set_duty_cycle(self.pin_backward, speed)

    def stop(self):
        """ Set the duty cycle of both control pins to zero to stop the motor. """
        GPIO.output(self.pin_forward, GPIO.LOW)
        GPIO.output(self.pin_backward, GPIO.LOW)
        PWM.set_duty_cycle(self.pin_forward, 0.0)
        time.sleep(self.reverse_delay)
        PWM.set_duty_cycle(self.pin_backward, 0.0)
        time.sleep(self.reverse_delay)
        print("Motor has been stopped")

    def cleanup(self):
        PWM.stop(self.pin_forward)
        PWM.stop(self.pin_backward)
        PWM.cleanup()
