import struct

from analyzer.cpuanalyzer import CpuAnalyzer
from analyzer.memoryanalyzer import MemoryAnalyzer
from analyzer.storageanalyzer import StorageAnalyzer

from parser.parser import Parser
from socketserver import Socket

if __name__ == '__main__':

    IP = '192.168.1.4'
    PORT = 8000
    BUFFER = 16
    PACK_FORMAT = '@hfd'

    CPU_COL_SEC = 1
    MEM_COL_SEC = 5
    STR_COL_SEC = 60

    server = Socket(ip=IP, port=PORT)
    server.server_listen()
    client, address = server.server_accept()
    print("client : ", address)

    p = Parser()
    ca = CpuAnalyzer(avg_sec=60/CPU_COL_SEC,
                     peak_sec=300/CPU_COL_SEC)
    ma = MemoryAnalyzer(avg_sec=300/MEM_COL_SEC)
    sa = StorageAnalyzer(avg_sec=1800/STR_COL_SEC)
    reset_count = 0

    while 1:
        recv_data = server.recv_data(client, BUFFER)
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
