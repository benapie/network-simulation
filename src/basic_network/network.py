from src.basic_network.router import *
from typing import List

class Network:
    def __init__(self, routers: List[Router] = None):
        self.routers = routers
        self.edges = []

    def link_to(self, x: Router, y: Router, ticks_per_packet: int) -> Edge:
        """Links two routers together,
        while also setting the connection speed.

        Arguments:
            x {Router} -- One of the routers to link to.
            y {Router} -- The other router to link to.
            ticks_per_packet {int} -- The connection speed.

        Returns:
            Edge -- The Edge object created for this connection."""

    def network_tick(self):
        """Ticks the network, ticking edges first then routers."""

if __name__ == '__main__':
    routers = []
    for i in range(6):
        routers.append(Router(str(i)))

    routers[0].register_edge(routers[1], Edge(routers[0], routers[1], 10))
    for i in range(1, 5):
        routers[i].register_edge(routers[i + 1], Edge(routers[i], routers[i + 1], 10))
        routers[i].register_edge(routers[i - 1], Edge(routers[i], routers[i - 1], 10))
    routers[5].register_edge(routers[4], Edge(routers[5], routers[4], 10))

    for i in range(100):
        for j in range(6):
            routers[j].send_distance_vector()

    routers[0].transport_send("Hello, world!", "5")
    routers[4].transport_send("My name is 4!", "2")