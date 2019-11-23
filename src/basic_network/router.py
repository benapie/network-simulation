from __future__ import annotations
from edge import Edge
from packet import Packet


class Router:
    def __init__(self, address: str):
        self.edges = []
        self.connected_to = []
        self.address = address

    def send_packet(self, addr: str, packet: Packet):
        """Sends packet to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            packet {Packet} -- The packet to send."""
        raise NotImplementedError("test test")

    def recieve_packet(self, packet: Packet):
        raise NotImplementedError("test setsers")
