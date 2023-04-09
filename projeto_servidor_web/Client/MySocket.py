import socket

class MySocket:
    def __init__(self, Host, Port):
        self.HOST = Host
        self.PORT = Port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open_connection()

    def open_connection(self):
        dest = (self.HOST, self.PORT)
        self.tcp.connect(dest)

    def dispatch(self, path = './home.html', method = 'GET', version = '1.1'):
        request = ' '.join([method, path, version, '\r\n'])
        print('Sending the following http request: ', request)
        self.tcp.send((request).encode())

    def listen(self):
        msg = self.tcp.recv(1024)
        return msg.decode()

    def close_connection(self):
        self.tcp.close()
