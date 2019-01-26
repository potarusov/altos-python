#
import time
from multiprocessing import Process
import Adafruit_BBIO.GPIO as GPIO
import config

class Ultrasonic:
    def __init__(self, thread_name, pin_trigger, pin_echo, can):
        self.thread_name = thread_name
        self.process = Process(target=self.run, args=(can,))
        #self.thread.daemon = True
        self._sentinel = object()

        self.timestamp = 0

        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        self.distance = 0.0

        self.reverse_delay = 0.00001

        GPIO.setup(self.pin_trigger, GPIO.OUT)
        GPIO.setup(self.pin_echo, GPIO.IN)
        GPIO.output(self.pin_trigger, GPIO.LOW)

        self.process.start()

    def run(self, can):
        while True:
            #btrc_frame = can.get_btrc_frame()
            #btrc_command = btrc_frame.get_btrc_command()
            #if btrc_command == "Exit":
            #    break
            if config.exit:
                break
            new_reading = False
            counter = 0
            GPIO.output(self.pin_trigger, GPIO.HIGH)
            time.sleep(self.reverse_delay)
            GPIO.output(self.pin_trigger, GPIO.LOW)
            #time.sleep(self.reverse_delay)

            while not GPIO.input(self.pin_echo):
                counter += 1
                if counter == 5000:
                    new_reading = True
                    break

            if new_reading:
                continue

            pulse_start = time.time()

            while GPIO.input(self.pin_echo):
                pass

            pulse_end = time.time()

            # Calculate pulse length
            elapsed = pulse_end - pulse_start

            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            self.distance = elapsed * 34000.0

            # That was the distance there and back so halve the value
            self.distance = self.distance / 2

            can.update_distance_buffer(self.distance, pulse_end)
            self.print_distance()

    def print_distance(self):
        print("Distance : %.1f" % self.distance)


