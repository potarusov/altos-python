
class KalmanFilter:
    def __init__(self, k_stab, x_opt_init):
        self.k_stab = k_stab
        self.x_opt = x_opt_init

    def set_x_opt(self, x_opt):
        self.x_opt = x_opt

    def callback(self, sensor_data):
        self.x_opt = self.k_stab * sensor_data + (1 - self.k_stab) * self.x_opt
        return self.x_opt

