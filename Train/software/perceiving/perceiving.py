import config
from Environment.map.map import Map
from Train.software.perceiving.kalman_filter import KalmanFilter

class Perceiving:
    def __init__(self, can, initial_position):
        #self.map = Map(config.map)
        self.can = can
        self.most_recent_position = initial_position
        self.kf = KalmanFilter(config.k_stab, 0)
        self.start = True

    def set_initial_position(self, initial_position):
        self.most_recent_position = initial_position

    def init_kf(self):
        self.start = True

    def get_position(self):
        RFID_frame = self.can.get_RFID_frame()
        RFID = RFID_frame.get_RFID()

        position = self.most_recent_position

        for node in self.map.nodes:
            if RFID == node['RFID']:
                position = node['label']
                self.most_recent_position = position
                break

        return position

    def get_distance(self):
        range_frame = self.can.get_range_frame()
        distance_2_obstacle = range_frame.get_distance()

        if self.start:
            self.kf.set_x_opt(distance_2_obstacle)
            self.start = False

        return self.kf.callback(distance_2_obstacle)

    def get_btrc_command(self):
        btrc_frame = self.can.get_btrc_frame()
        return btrc_frame.get_btrc_command()

    def run(self):
        distance_2_obstacle = self.get_distance()
        btrc_command = self.get_btrc_command()

        return self.most_recent_position, distance_2_obstacle, btrc_command
