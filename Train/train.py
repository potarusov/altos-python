# Train

import config

from Train.sensors.bluetooth_server import Bluetooth
from Train.sensors.ultrasonic import Ultrasonic
from Train.sensors.RFID_reader import RFID_reader
from Train.can import CAN
from Train.actuators.simple_dc_motor import SimpleDCMotor


class Train:
    # Constructor
    def __init__(self, position):
        self.position_on_track = position
        self.velocity = config.min_velocity

        """ Controller Area Network """
        self.can = CAN()

        """ Sensors """
        self.ultrasonic = Ultrasonic("Ultrasonic", config.pin_trigger, config.pin_echo, self.can)

        self.RFID_reader = RFID_reader("RFID reader", self.can)

        self.bluetooth = Bluetooth('Remote Control', self.can)

        """ Actuators """
        self.motor = SimpleDCMotor(config.pin_A, config.pin_B)

    def move_forward(self, step):
        if self.velocity + step >= config.min_velocity and self.velocity + step <= config.max_velocity:
            self.velocity += step
            self.motor.forward(self.velocity)
        elif self.velocity + step < config.min_velocity:
            print("The minimum velocity has been reached")
        elif self.velocity + step > config.max_velocity:
            print(self.velocity)
            print("The maximum velocity has been reached")

        print("Velocity [%f]" % self.velocity)

    def move_backward(self, step):
        if self.velocity + step >= config.min_velocity and self.velocity + step <= config.max_velocity:
            self.velocity += step
            self.motor.backward(self.velocity)
        elif self.velocity + step < config.min_velocity:
            print("The minimum velocity has been reached")
        elif self.velocity + step > config.max_velocity:
            print(self.velocity)
            print("The maximum velocity has been reached")

        print("Velocity [%f]" % self.velocity)

    def stop(self):
        self.motor.stop()

    def shutdown(self):
        self.motor.stop()
        self.motor.cleanup()
        self.ultrasonic.process.terminate()
        self.RFID_reader.process.terminate()
        self.bluetooth.close_bluetooth_socket()
        self.bluetooth.process.terminate()






