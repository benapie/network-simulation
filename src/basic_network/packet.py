class Packet:
    def __init__(self, data, from_addr, to_addr):
        self.data = data
        self.from_addr = from_addr
        self.to_addr = to_addr
