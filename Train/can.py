""" Controller Area Network """
from multiprocessing import JoinableQueue

# Ultrasonic Range Finder CAN Frame
class RangeCANFrame:
    def __init__(self, distance, timestamp):
        self.distance = distance
        self.timestamp = timestamp

    def get_distance(self):
        return self.distance

    def get_timestamp(self):
        return self.timestamp

# RFID Reader CAN Frame
class RFIDCANFrame:
    def __init__(self, RFID, timestamp):
        self.RFID = RFID
        self.timestamp = timestamp

    def get_RFID(self):
        return self.RFID

    def get_timestamp(self):
        return self.timestamp

# Android Bluetooth Remote Control CAN Frame
class BluetoothRemoteControlCANFrame:
    def __init__(self, btrc_command, timestamp):
        self.btrc_command = btrc_command
        self.timestamp = timestamp

    def get_btrc_command(self):
        return self.btrc_command

    def get_timestamp(self):
        return self.timestamp


class CAN:
    def __init__(self):
        # Distance Buffer
        self.distance_buffer = JoinableQueue()
        self.last_received_range_frame = RangeCANFrame(0, 0)

        # RFID Buffer
        self.RFID_buffer = JoinableQueue()

        # Bluetooth Remote Control Command Buffer
        self.btrc_buffer = JoinableQueue()

    def update_distance_buffer(self, distance_to_obstacle, timestamp):
        self.distance_buffer.put(RangeCANFrame(distance_to_obstacle, timestamp))

    def update_RFID_buffer(self, RFID, timestamp):
        self.RFID_buffer.put(RFIDCANFrame(RFID, timestamp))

    def update_btrc_buffer(self, btrc_command, timestamp):
        self.btrc_buffer.put(BluetoothRemoteControlCANFrame(btrc_command, timestamp))

    def get_range_frame(self):
        if not self.distance_buffer.empty():
            self.last_received_range_frame = self.distance_buffer.get_nowait()
        return self.last_received_range_frame

    def get_RFID_frame(self):
        if not self.RFID_buffer.empty():
            return self.RFID_buffer.get_nowait()
        else:
            return RFIDCANFrame("NaN", 0)

    def get_btrc_frame(self):
        if not self.btrc_buffer.empty():
            return self.btrc_buffer.get_nowait()
        else:
            return BluetoothRemoteControlCANFrame("None", 0)






