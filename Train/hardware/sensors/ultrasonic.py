#
import time
from multiprocessing import Process
import Adafruit_BBIO.GPIO as GPIO
import config

class Ultrasonic:
    def __init__(self, thread_name, pin_trigger, pin_echo, can):
        self.thread_name = thread_name
        self.process = Process(target=self.run, args=(can,))

        self.timestamp = 0

        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        self.distance = 0.0

        self.delay = config.delay

        self.start = True

        GPIO.setup(self.pin_trigger, GPIO.OUT)
        GPIO.setup(self.pin_echo, GPIO.IN)
        GPIO.output(self.pin_trigger, GPIO.LOW)

        self.process.start()

    def run(self, can):
        while True:
            if config.exit:
                break
            new_reading = False
            counter = 0
            GPIO.output(self.pin_trigger, GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.pin_trigger, GPIO.LOW)

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

            # with open('ultrasonic_distance.csv', 'a') as file_2_write:
            #     write_2_file = csv.writer(file_2_write)
            #     row = [self.distance]
            #     write_2_file.writerow(row)
            if config.log_distance:
                self.print_distance()

    def print_distance(self):
        print("Distance : %.1f" % self.distance)


