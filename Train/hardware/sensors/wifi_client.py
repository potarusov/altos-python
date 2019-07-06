import socket, time, pickle
from multiprocessing import Process
import config

class WiFi:
    def __init__(self, thread_name, can):
        self.thread_name = thread_name
        self.process = Process(target=self.run, args=(can,))

        self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.TCP_socket.connect((config.server_ip, config.server_port_number))

        self.process.start()

    def run(self, can):
        while True:
            if config.exit:
                break
            train_state_2_control_center = pickle.dumps(can.get_wfts_frame())
            self.TCP_socket.send(train_state_2_control_center)

            message_from_control_center = self.TCP_socket.recv(1024).decode()
            timestamp = time.time()
            can.update_wfcc_buffer(message_from_control_center, timestamp)
            #print(message_from_control_center)

    def close_TCP_socket(self):
        self.TCP_socket.shutdown(socket.SHUT_RDWR)
        self.TCP_socket.close()
        print("TCP Socket has been closed")

