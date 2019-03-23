from multiprocessing import JoinableQueue
from keyboard import Keyboard
import config
from Train.train import Train

class Main:
    def __init__(self):
        self.train = Train()
        #self.keyboard_input_buffer = JoinableQueue()
        #self.keyboard = Keyboard("Keyboard", self.keyboard_input_buffer)

    def run(self):
        keyboard_input = []
        while not config.exit:
            """if not self.keyboard_input_buffer.empty():
                print("Here!")
                keyboard_input = self.keyboard_input_buffer.get_nowait()
                print(keyboard_input)
                if keyboard_input == "exit":
                    config.exit = 1"""
            most_recent_position, distance_2_obstacle, btrc_command = self.train.ps.run()
            decision = self.train.dms.run(most_recent_position, distance_2_obstacle, btrc_command, keyboard_input)
            self.train.acts.run(decision)
        self.train.shutdown()
        #self.keyboard.process.terminate()
        #self.keyboard.process.join()

main = Main()
main.run()