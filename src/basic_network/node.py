from __future__ import annotations
from edge import Edge
from packet import Packet


class Node:
    def __init__(self):
        self.edges = []
        self.connected_to = []

    def link_to(self, node: Node, ticks_per_packet: int) -> Edge:
        raise NotImplementedError("tests etst")

    def send_packet(self, node: Node, packet: Packet):
        if node not in self.connected_to:
            raise ValueError("cannot send to disconnected node")
        raise NotImplementedError("test test")
