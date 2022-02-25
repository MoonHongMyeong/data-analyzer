import socket


class Server:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))

    def server_listen(self):
        self.sock.listen(0)
        print('socket server listen...')

    def server_accept(self):
        return self.sock.accept()

    @staticmethod
    def recv_data(client, buff):
        return client.recv(buff)

    def server_close(self):
        self.sock.close()
