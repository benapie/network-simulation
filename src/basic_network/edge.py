from node import Node


class Edge:
    def __init__(self, a: Node, b: Node, ticks_per_packet: int):
        self.a = a
        self.b = b
        self.ticks_per_packet = ticks_per_packet

    def tick(self):
        # will tick along packets and send them on to node b when done
        raise NotImplementedError("test testserser")
