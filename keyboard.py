
from multiprocessing import Process
import config

class Keyboard:
    def __init__(self, thread_name, input_queue):
        self.thread_name = thread_name
        self.process = Process(target=self.run, args=(input_queue,))

        self.command = []

        self.delay = config.delay

        self.start = True

        self.process.start()

    def run(self, input_queue):
        while True:
            if config.exit:
                break

            input_string = input("Waiting for keyboard input...")
            print(input_string)
            input_queue.put(input_string)
