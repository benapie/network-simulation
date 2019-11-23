from router import Router
from edge import Edge
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
