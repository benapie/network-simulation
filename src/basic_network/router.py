from __future__ import annotations
from edge import Edge
from packet import Packet


class Router:
    def __init__(self, address: str):
        self.edges = []
        self.connected_to = []
        self.address = address

    def link_to(self, node: Router, ticks_per_packet: int) -> Edge:
        """Links this router to another router,
        while also setting the connection speed.

        Arguments:
            node {Router} -- The other router to link to.
            ticks_per_packet {int} -- The connection speed.

        Returns:
            Edge -- The Edge object created for this connection."""
        raise NotImplementedError("tests etst")

    def send_packet(self, addr: str, packet: Packet):
        """Sends packet to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            packet {Packet} -- The packet to send."""
        raise NotImplementedError("test test")
