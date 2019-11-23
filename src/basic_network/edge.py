from src.basic_network.router import Router
from src.basic_network.packet import Packet


class Edge:
    def __init__(self, a: Router, b: Router, ticks_per_packet: int):
        self.a = a
        self.b = b
        self.ticks_per_packet = ticks_per_packet
        self.packets = []

    def send(self, p: Packet, target: Router):
        self.packets.append((p, target, 0))

    def tick(self):
        """This will tick an edge along, moving every packet on the edge one
        tick along, while also manging sending to the routers if they arrive."""
        packets = ((p, tar) for (p, tar, ticks) in self.packets
                   if (ticks == self.ticks_per_packet - 1))
        for p, tar in packets:
            self.packets.remove((p, self.ticks_per_packet - 1))
            tar.recieve_packet(p)
        for i in range(len(self.packets)):
            self.packets[i] = (self.packets[i][0],
                               self.packets[i][1], self.packets[i][2] + 1)
