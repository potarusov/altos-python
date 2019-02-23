__author__ = 'POTABONNIER'

import time
from multiprocessing import Process
import serial
import Adafruit_BBIO.UART as UART
UART.setup("UART2")
import config

# RFID reader ID-20LA
class RFID_reader:
    def __init__(self, thread_name, can):
        self.thread_name = thread_name
        self.port = serial.Serial("/dev/ttyO2", 9600)
        print(self.port.name)
        self.process = Process(target=self.run, args=(can,))
        self.delay = config.delay
        self.process.start()
    def run(self, can):
        while True:
            #if self.port.isOpen():
                print("Serial port for RFID data has been opened")
                # There's incoming data
                data = ""
                while self.port.isOpen():
                    # If multiple characters are being sent we want
                    # to catch them all, so add received byte to our
                    # data string and delay a little to give the
                    #  next byte time to arrive:
                    data += self.port.readline()
                    time.sleep(self.delay)

                    # Print what was sent:
                    print "RFID Data Received:\n '%s'" % data

                    timestamp = time.time()
                    can.update_RFID_buffer(data, timestamp)



