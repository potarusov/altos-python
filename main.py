import config
from Train.train import Train

class Main:
    def __init__(self):
        self.train = Train()

    def run(self):
        while not config.exit:
            most_recent_position, distance_2_obstacle, btrc_command, message_from_cc = self.train.ps.run()
            decision = self.train.dms.run(most_recent_position, distance_2_obstacle, btrc_command, message_from_cc)
            self.train.acts.run(decision)
        self.train.shutdown()

main = Main()
main.run()