from __future__ import annotations
from src.basic_network.data_layer import DataLayer
from src.basic_network.edge import Edge
from src.basic_network.packet import Packet
from typing import List, Dict
import math

class Router:
    neighbours: List[Router]
    edges: List[Edge]
    distances: Dict[str, int]
    address: str
    to: List[str]
    data_layer: DataLayer

    def __init__(self, address: str):
        self.edges = []
        self.neighbours = []
        self.address = address
        self.distances = {self.address: 0}
        self.to = []
        self.data_layer = DataLayer()
        self.data_layer.set_router(self)
        self.packet_queues = {}

    def transport_send(self, content: str, to_addr: str):
        """Splits the content into packets and sends them"""
        # Each packet is of length 255 (§) is added to pad packets of length < 255
        # Each packet has a sequence number S_NUM (for reconstruction)
        # Each packet is sent with a NUM_P specifying the number of packets in content (for reconstruction)
        content.replace("§", "\§")
        s_num = 0
        num_p = math.ceil(len(content)/255)
        while len(content) > 255:
            Router.send_data(to_addr, {"CONTENT": "DATA", "CONTENT": content[:255], "S_NUM": s_num, "NUM_P": num_p})
            content = content[255:]
            s_num += 1
        while len(content) < 255:
            content += "§"
        if len(content) != 0:
            Router.send_data(to_addr, {"CONTENT": "DATA", "CONTENT": content, "S_NUM": s_num, "NUM_P": num_p})

    def application_send(self, data):
        pass

    def transport_receive(self, packet):
        if packet.from_addr not in self.packet_queues:
            self.packet_queues[packet.from_addr] = [packet.data]
        else:
            self.packet_queues[packet.from_addr].append(packet.data)
        if len(self.packet_queues[packet.from_addr]) == packet.data["NUM_P"]:
            self.application_send(self.reconstruct_data(self.packet_queues[packet.from_addr]))

    def reconstruct_data(self, packets: []):
        pass

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
                self.to[node] = dv.from_addr
            else:
                if self.distances[node] > dv.data["CONTENT"][node] + self.distances[dv.from_addr]:
                    self.distances[node] = dv.data["CONTENT"][node] + self.distances[dv.from_addr]
                    self.to[node] = dv.from_addr

    def where_to(self, packet: Packet) -> str:
        """Return where to send the packet."""
        return self.to[packet.to_addr]

    def network_receive(self, packet: Packet):
        """Decides what needs to be done with the received packet"""
        if packet.to_addr == self.address:
            if packet.data["HEAD"] == "DV":
                self.update_distance_vector(packet)
            else:
                self.transport_receive(packet)
        else:
            self.data_layer.send_packet(packet, self.where_to(packet))

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

    def send_data(self, addr: str, data):
        """Sends data to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            data -- The data to send."""
        p = Packet(data, self.address, addr)
        self.data_layer.send_packet(p, self.where_to(addr))

    def recieve_packet(self, packet: Packet):
        raise NotImplementedError("test setsers")
