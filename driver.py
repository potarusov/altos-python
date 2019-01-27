# Manual mode

import sys, time
import config


class Driver:
    def __init__(self, train):
        self.train = train
        self.moving_forward = True
        self.moving_backward = False
        self.stop = False
        self.obstacle_ahead = False

    def run(self):
        while not config.exit:
            if sys.platform.startswith('linux2'):
                range_frame = self.train.can.get_range_frame()
                distance_2_obstacle = range_frame.get_distance()
                if distance_2_obstacle > 0.0 and distance_2_obstacle < 15.0 and not self.obstacle_ahead\
                        and not self.stop:
                    print("Obstacle ahead!")
                    self.train.stop()
                    self.obstacle_ahead = True
                    self.stop = True
                elif distance_2_obstacle > 15.0 and self.obstacle_ahead and self.stop:
                    self.train.velocity = config.min_velocity
                    self.obstacle_ahead = False
                    self.train.move_forward(0.0)
                    self.stop = False

                btrc_frame = self.train.can.get_btrc_frame()
                btrc_command = btrc_frame.get_btrc_command()
                if btrc_command:
                    if btrc_command == 'accelerate': # Forward
                        print("Accelerate")
                        if self.moving_forward:
                            self.train.move_forward(config.velocity_step)
                        elif self.moving_backward:
                            self.train.move_backward(config.velocity_step)
                    elif btrc_command == 'decelerate':
                        print("Decelerate")
                        if self.moving_forward:
                            self.train.move_forward(-config.velocity_step)
                        elif self.moving_backward:
                            self.train.move_backward(-config.velocity_step)
                    elif btrc_command == 'direction':
                        print("Change Direction")
                        if self.moving_forward:
                            self.moving_forward = False
                            self.moving_backward = True
                            self.train.stop()
                            self.train.move_backward(0.0)
                        elif self.moving_backward:
                            self.moving_backward = False
                            self.moving_forward = True
                            self.train.stop()
                            self.train.move_forward(0.0)
                    elif btrc_command == 'stop':
                        print("Stop")
                        self.train.stop()
                    elif btrc_command == 'shutdown':
                        print("Shutdown")
                        self.train.shutdown()
                        config.exit = 1
                        self.train.ultrasonic.process.terminate()
                        self.train.bluetooth.process.terminate()





