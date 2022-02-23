import struct
import time

from analyzer.analyzer import Analyzer


class CpuAnalyzer(Analyzer):

    def __init__(self, avg_sec, peak_sec):
        self.acc_avg = []
        self.acc_peak = []
        self.acc_rate = 0.0
        self.avg_sec = avg_sec
        self.peak_sec = peak_sec
        self.pack_format = '@hhfd'
        self.type = 1
        # 0 : raw data, 1 : avg data, 2 peak data
        self.sep = 0
        self.cpu_rate = 0.0
        self.cpu_timestamp = 0.0

    def analyze_data(self, data):
        self.acc_avg.append(data)
        self.acc_peak.append(data)

        if len(self.acc_avg) == self.avg_sec:
            self._analyze_avg()

        if len(self.acc_peak) == self.peak_sec:
            self._analyze_peak()

    def _analyze_avg(self):
        for rate in self.acc_avg:
            self.acc_rate += float(rate['rate'])

        self.cpu_rate = round(self.acc_rate / len(self.acc_avg), 2)
        self.cpu_timestamp = time.time()

        self.sep = 1

        send_data = self._format_struct_to_data()
        self._send_data(send_data)

        self.acc_rate = 0.0
        self.acc_avg.clear()

    def _analyze_peak(self):
        sort_list = sorted(self.acc_peak, key=(lambda x: x['rate']), reverse=True)

        self.sep = 2
        self.cpu_rate = sort_list[0]['rate']
        self.cpu_timestamp = sort_list[0]['timestamp']

        send_data = self._format_struct_to_data()
        self._send_data(send_data)

        self.acc_peak.clear()

    def _send_data(self, data):
        print('-------cpu-------')
        print(data)
        print(struct.unpack(self.pack_format, data))

    def _format_struct_to_data(self):
        send_bytes = struct.pack(self.pack_format, self.type, self.sep, self.cpu_rate, self.cpu_timestamp)
        return send_bytes
