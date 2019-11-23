from __future__ import annotations
from edge import Edge
from packet import Packet


class Node:
    def __init__(self):
        self.edges = []
        self.connected_to = []
        self.distance_vector = {}
        for address in self.connected_to:
            for edge in self.edges:
                if edge.a.address == address:
                    self.distance_vector[address] = edge.a.ticks_per_packet
                    break
                elif edge.b.address == address:
                    self.distance_vector[address] = edge.b.ticks_per_packet
                    break

    def send_distance_vector(self):
        for edge in self.edges:
            if edge.a == self:
                self.send_packet(edge.b, Packet({"HEAD": "DV", "CONTENT": self.distance_vector}))
            else:
                self.send_packet(edge.a, Packet({"HEAD": "DV", "CONTENT": self.distance_vector}))

    def update_distance_vector(self, received_vector: Packet):
        for node in received_vector["CONTENT"]:
            if node not in self.distance_vector:
                self.distance_vector[node] = received_vector["CONTENT"][node]
            else:
                self.distance_vecotr[node] = min([self.distance_vector[node], received_vector["CONTENT"][node]])

    def link_to(self, node: Node, ticks_per_packet: int) -> Edge:
        raise NotImplementedError("tests etst")

    def send_packet(self, node: Node, packet: Packet):
        if node not in self.connected_to:
            raise ValueError("cannot send to disconnected node")
        raise NotImplementedError("test test")

    def next_node(self, packet):
        '''Returns the next node for the packet to be sent to'''
