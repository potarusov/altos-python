# Train
import config

from Train.hardware.can import CAN
from Train.hardware.sensors.bluetooth_server import Bluetooth
from Train.hardware.sensors.ultrasonic import Ultrasonic
from Train.hardware.sensors.RFID_reader import RFID_reader
from Train.hardware.actuators.simple_dc_motor import SimpleDCMotor
from Train.software.perceiving.perceiving import Perceiving
from Train.software.decision_making.dmaking import DecisionMaking
from Train.software.acting.acting import Acting

class Train:
    # Constructor
    def __init__(self):
        """ Controller Area Network """
        self.can = CAN()

        """ Sensors """
        self.ultrasonic = Ultrasonic("Ultrasonic", config.pin_trigger, config.pin_echo, self.can)

        self.RFID_reader = RFID_reader("RFID reader", self.can)

        self.bluetooth = Bluetooth('Remote Control', self.can)

        """ Actuators """
        self.motor = SimpleDCMotor(config.pin_A, config.pin_B)

        """ Systems/modules """
        self.ps = Perceiving(self.can, config.initial_position)
        self.dms = DecisionMaking(self.ps)
        self.acts = Acting(self.motor)

    def shutdown(self):
        self.ultrasonic.process.terminate()
        self.ultrasonic.process.join()
        self.RFID_reader.process.terminate()
        self.RFID_reader.process.join()
        self.bluetooth.close_bluetooth_socket()
        self.bluetooth.process.terminate()
        self.bluetooth.process.join()








