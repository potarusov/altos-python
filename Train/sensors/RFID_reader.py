__author__ = 'POTABONNIER'

from multiprocessing import Process
import serial
import Adafruit_BBIO.UART as UART
UART.setup("UART2")

# RFID reader ID-20LA

class RFID_reader:
    def __init__(self, can):
        self.port = serial.Serial("/dev/ttyO2", 9600)
        self.process = Process(target=self.run, args=(can,))
        print(self.port.name)
    def run(self, can):
        if self.port.isOpen():
            print("Serial port for RFID data has been opened")
            # There's incoming data
            data = ""
            while self.port.isOpen():
                # If multiple characters are being sent we want
                # to catch them all, so add received byte to our
                # data string and delay a little to give the
                #  next byte time to arrive:
                data += self.port.readline()
                delay(5)
                # Print what was sent:
                print "Data received:\n '%s'" % data
                # And echo it back to the serial port:
                # serial.write(data)
                break
            delay(100)
