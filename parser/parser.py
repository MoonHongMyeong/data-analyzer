class Parser:

    def __init__(self):
        self.data = {}

    def parse_data(self, data):
        self.data = {'type': data[0], 'rate': data[1], 'timestamp': data[2]}
        return self.data

