# Bluetooth Server on the Beaglebone Black Wireless

import time
from multiprocessing import Process
from bluetooth import *
import config

class Bluetooth:
    def __init__(self, thread_name, can):
        self.thread_name = thread_name
        self.process = Process(target=self.run, args=(can,))

        """ Initialize a bluetooth sezrver on the BeagleBone """
        self.server_socket = BluetoothSocket(RFCOMM)
        self.server_socket.bind(("", PORT_ANY))
        self.server_socket.listen(1)

        port = self.server_socket.getsockname()[1]

        advertise_service(self.server_socket, config.android_application_name, service_id=config.service_uuid,
                          service_classes=[config.service_uuid, SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE])

        print("Awaiting RFCOMM connection on channel:%d" % port)

        self.client_socket, client_info = self.server_socket.accept()
        print("Accepted connection from:", client_info)
        self.process.start()

    def run(self, can):
        while True:
            data = self.client_socket.recv(1024).strip()
            if len(data) == 0:
                continue
            if config.exit:
                break
            print("Received [%s]" % data)
            self.client_socket.sendall('OK')

            timestamp = time.time()
            can.update_btrc_buffer(data, timestamp)

    def close_bluetooth_socket(self):
        self.client_socket.close()
        self.server_socket.close()
        print("Bluetooth Socket has been closed")




