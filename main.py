import config
#from Environment.Environment import Environment
from Train.train import Train
from driver import Driver
#from PS.PS import PS
#from MPS.MPS import MPS

class Main:
    def __init__(self):
        #self.env = map(config.map)

        self.train = Train(config.initial_position)

        self.driver = Driver(self.train)
        #self.ps = PS(self.env, self.train)
        #self.mps = MPS(self.robot)

    def run(self):
        #self.ps.Core()
        #self.mps.Core()
        self.driver.run()

main = Main()
main.run()