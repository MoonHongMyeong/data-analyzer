import struct
import time

from analyzer.analyzer import Analyzer


class MemoryAnalyzer(Analyzer):

    def __init__(self, avg_sec):
        self.acc_avg = []
        self.acc_rate = 0.0
        self.avg_rate = 0.0
        self.avg_sec = avg_sec
        self.pack_format = '@hhfd'
        self.type = 2
        self.sep = 0

    def analyze_data(self, data):
        self.acc_avg.append(data)
        if len(self.acc_avg) == self.avg_sec:
            self._analyze_avg()

    def _analyze_avg(self):
        for rate in self.acc_avg:
            self.acc_rate += float(rate['rate'])

        self.avg_rate = round(self.acc_rate / len(self.acc_avg), 2)
        self.sep = 1

        send_data = self._format_struct_to_data()
        self._send_data(send_data)

        self.acc_rate = 0.0
        self.acc_avg.clear()

    def _send_data(self, data):
        print('-------memory-------')
        print(data)
        print(struct.unpack(self.pack_format, data))

    def _format_struct_to_data(self):
        send_bytes = struct.pack(self.pack_format, self.type, self.sep, self.avg_rate, time.time())
        return send_bytes
