from __future__ import annotations
from src.basic_network.edge import Edge
from src.basic_network.packet import Packet
from typing import List, Dict


class Router:
    neighbours: List[Router]
    edges: List[Edge]
    distances: Dict[str, int]
    address: str

    def __init__(self, address: str):
        self.edges = []
        self.neighbours = []
        self.address = address
        self.distances = {self.address: 0}

    def send_distance_vector(self):
        """Sends current distance vector to all neighbours"""
        for neighbour in self.neighbours:
            self.send_packet(neighbour.address, {"HEAD": "DV", "CONTENT": self.distances})

    def update_distance_vector(self, dv: Packet):
        """Upon receiving a distance vector from neighbours, each Router updates its vector to contain the most recent
        information regarding the optimum distance to other nodes"""
        for node in dv.data["CONTENT"]:
            if node not in self.distances:
                self.distances[node] = dv.data["CONTENT"][node] + self.distances[dv.from_addr]
            else:
                self.distances[node] = min(self.distances[node],
                                           dv.data["CONTENT"][node] + self.distances[dv.from_addr])

    def network_receive(self, packet: Packet):
        """Receives a packet and sends it to transport layer if need be"""
        if packet.data["HEAD"] == "DV":
            self.update_distance_vector(packet)
        else:
            pass

    def update_dv(self, edge: Edge):
        other_router = edge.b if edge.b != self else edge.a
        self.distances[other_router] = edge.ticks_per_packet

    def register_edge(self, router: Router, edge: Edge):
        """Registers the link between this router to another router, while also setting the connection speed.

        Arguments:
            router {Router} -- The other router to link to.
            edge {Edge} -- The new edge.

        Returns:
            Edge -- The Edge object created for this connection."""
        self.edges.append(edge)
        self.neighbours.append(router)
        self.update_dv(edge)

    def send_packet(self, addr: str, data):
        """Sends packet to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            data -- The data to send."""
        raise NotImplementedError("test test")

    def recieve_packet(self, packet: Packet):
        raise NotImplementedError("test setsers")
