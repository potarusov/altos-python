""" Controller Area Network """
from multiprocessing import JoinableQueue, Manager

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

# Raspberry WiFi Control Center CAN Frame
class WiFiControlCenterCANFrame:
    def __init__(self, wfcc_message, timestamp):
        self.wfcc_message = wfcc_message
        self.timestamp = timestamp

    def get_wfcc_message(self):
        return self.wfcc_message

    def get_timestamp(self):
        return self.timestamp

# WiFi Train State CAN Frame
class WiFiTrainStateCANFrame:
    def __init__(self, most_recent_position, mode, state, decision, timestamp):
        self.most_recent_position = most_recent_position
        self.mode = mode
        self.state = state
        self.decision = decision
        self.timestamp = timestamp

class CAN:
    def __init__(self):
        # Distance Buffer
        self.distance_buffer = JoinableQueue(100)
        self.last_received_range_frame = RangeCANFrame(0, 0)

        # RFID Buffer
        self.RFID_buffer = JoinableQueue(100)

        # Bluetooth Remote Control Command Buffer
        self.btrc_buffer = JoinableQueue(100)

        # WiFi Control Center Message Buffer
        self.wfcc_buffer = JoinableQueue(100)

        # WiFi Train State Message Buffer
        self.wfts_buffer = JoinableQueue(100)

    def update_distance_buffer(self, distance_to_obstacle, timestamp):
        self.distance_buffer.put(RangeCANFrame(distance_to_obstacle, timestamp))

    def update_RFID_buffer(self, RFID, timestamp):
        self.RFID_buffer.put(RFIDCANFrame(RFID, timestamp))

    def update_btrc_buffer(self, btrc_command, timestamp):
        self.btrc_buffer.put(BluetoothRemoteControlCANFrame(btrc_command, timestamp))

    def update_wfcc_buffer(self, wfcc_message, timestamp):
        self.wfcc_buffer.put(WiFiControlCenterCANFrame(wfcc_message, timestamp))

    def update_wfts_buffer(self, most_recent_position, mode, state, decision, timestamp):
        self.wfts_buffer.put(WiFiTrainStateCANFrame(most_recent_position, mode, state, decision, timestamp))

    def get_range_frame(self):
        if not self.distance_buffer.empty():
            self.last_received_range_frame = self.distance_buffer.get_nowait()
        return self.last_received_range_frame

    def get_RFID_frame(self):
        if not self.RFID_buffer.empty():
            return self.RFID_buffer.get_nowait()
        else:
            return RFIDCANFrame("NaRFID", 0)

    def get_btrc_frame(self):
        if not self.btrc_buffer.empty():
            return self.btrc_buffer.get_nowait()
        else:
            return BluetoothRemoteControlCANFrame("None", 0)

    def get_wfcc_frame(self):
        if not self.wfcc_buffer.empty():
            wfcc_frame = self.wfcc_buffer.get()
            return wfcc_frame
        else:
            return WiFiControlCenterCANFrame("None", 0)

    def get_wfts_frame(self):
        if not self.wfts_buffer.empty():
            wfts_frame = self.wfts_buffer.get()
            return wfts_frame
        else:
            return WiFiTrainStateCANFrame(-1, "UNKNOWN", "UNKNOWN", "NO", 0)
