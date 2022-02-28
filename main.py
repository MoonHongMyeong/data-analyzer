import struct
import time
from multiprocessing import Queue, Process

from analyzer.cpuanalyzer import CpuAnalyzer
from analyzer.memoryanalyzer import MemoryAnalyzer
from analyzer.storageanalyzer import StorageAnalyzer

from parser.parser import Parser
from utils.socketclient import Client
from utils.socketserver import Server

if __name__ == '__main__':

    IP = '192.168.1.4'
    RECV_PORT = 8000
    SEND_PORT = 8001
    BUFFER = 16
    PACK_FORMAT = '@hfd'

    CPU_COL_SEC = 1
    MEM_COL_SEC = 5
    STR_COL_SEC = 60

    server = Server(ip=IP, port=RECV_PORT)
    que = Queue()
    p = Parser()
    ca = CpuAnalyzer(avg_sec=60 / CPU_COL_SEC,
                     peak_sec=300 / CPU_COL_SEC,
                     queue=que)
    ma = MemoryAnalyzer(avg_sec=300 / MEM_COL_SEC, queue=que)
    sa = StorageAnalyzer(avg_sec=1800 / STR_COL_SEC, queue=que)

    server.server_listen()
    recv_client, recv_address = server.server_accept()

    client = Client(que)
    client.connect(ip=IP, port=SEND_PORT)

    socket_process = Process(target=client.send)
    socket_process.start()

    while 1:
        try:
            recv_data = server.recv_data(recv_client, BUFFER)
            time.sleep(0.1)
            print(recv_data)
            unpack_data = struct.unpack(PACK_FORMAT, recv_data)
            print(unpack_data)

            if unpack_data[0] == 3:
                storage_data = p.parse_data(unpack_data)
                sa.analyze_data(storage_data)
            elif unpack_data[0] == 2:
                memory_data = p.parse_data(unpack_data)
                ma.analyze_data(memory_data)
            elif unpack_data[0] == 1:
                cpu_data = p.parse_data(unpack_data)
                ca.analyze_data(cpu_data)

        except ConnectionError:
            server.server_listen()
            recv_client, recv_address = server.server_accept()
