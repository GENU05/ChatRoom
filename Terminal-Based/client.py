import sys
import socket
import select
import queue
import time
from tk import *

ENCODING = 'utf-8'

class Client(threading.Thread):
    def __init__(self,HOST,PORT):
        super().__init__(daemon=True , target=self.run)
        self.host = HOST
        self.port = PORT
        self.sock = None
        self.queue = queue.Queue()
        self.connected = self.connect_to_server()
        # self.lock = threading.RLock()
        if self.connected:
            self.gui = GUI(self)
            # self.start()
            self.gui.start()
            self.run()

    def run(self):
        inputs = [self.sock]
        outputs = [self.sock]
        read , write , exceptional = [] , [] , []
        while inputs:
            try:
                read, write, exceptional = select.select(inputs, outputs, inputs)
            # if server unexpectedly quits, this will raise ValueError exception (file descriptor < 0)
            except ValueError:
                print('$ Server error $')
                # GUI.display_alert('Server error has occurred. Exit app')
                self.sock.close()
                break

            if self.sock in read:
                data = self.sock.recv(1024)
                data =  data.decode(ENCODING)
                print(data)
                self.process_data(data)

            if self.sock in write:
                if not self.queue.empty():
                    data = self.queue.get()
                    self.send_message(data)

            if self.sock in exceptional:
                print('*  Server error  *')
                GUI.display_alert('Server error has occurred. Exit app')
                self.sock.close()
                break

    def connect_to_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.sock.connect((self.host ,self.port ))
        except:
            print("# Connection Refused #")
            return False
        return True

    def exit_window(self):
        print('! Connection closed !')
        self.sock.close()
        return True

    def send_message(self,data):
        try:
            self.sock.send(data)
        except socket.error:
            self.sock.close()
            GUI.display_alert('Server error has occurred. Exit app')

    def process_data(self,data):
        if data:
            message = data
            self.gui.display_message(message)
            #GUI Display messages




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage : Script IP Port Name')
        exit()
    print('Host' , sys.argv[1])
    print('Port' , sys.argv[2])
    Client(sys.argv[1] , int(sys.argv[2]) )
