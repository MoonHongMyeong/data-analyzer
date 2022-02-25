import socket


class Client:

    def __init__(self, queue):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._queue = queue

    def connect(self, ip, port):
        self._client.connect((ip, port))

    def send(self):
        while 1:
            if self._queue.qsize() > 0:
                self._client.sendall(self._queue.get())
