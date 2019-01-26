""" Controller Area Network """
from multiprocessing import Queue, JoinableQueue

# Ultrasonic Range Finder CAN Frame
class RangeCANFrame:
    def __init__(self, distance, timestamp):
        self.distance = distance
        self.timestamp = timestamp

    def get_distance(self):
        return self.distance

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

        # Bluetooth Remote Control Command Buffer
        self.btrc_buffer = JoinableQueue()

    def update_distance_buffer(self, distance_to_obstacle, timestamp):
        #if not self.distance_buffer.empty():
        #    self.distance_buffer.get()
        self.distance_buffer.put(RangeCANFrame(distance_to_obstacle, timestamp))

    def update_btrc_buffer(self, btrc_command, timestamp):
        #if not self.btrc_buffer.empty():
        #    self.btrc_buffer.get()
        self.btrc_buffer.put(BluetoothRemoteControlCANFrame(btrc_command, timestamp))

    def get_range_frame(self):
        if not self.distance_buffer.empty():
            return self.distance_buffer.get_nowait()
        else:
            return RangeCANFrame(150.0, 0)

    def get_btrc_frame(self):
        if not self.btrc_buffer.empty():
            return self.btrc_buffer.get_nowait()
        else:
            return BluetoothRemoteControlCANFrame("None", 0)






