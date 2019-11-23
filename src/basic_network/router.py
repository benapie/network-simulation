from __future__ import annotations
from src.basic_network.packet import Packet
from typing import List, Dict
import math
import logging

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

class DataLayer:
    edges: Dict[str, Edge]
    router: Router

    def __init__(self):
        self.edges = {}

    def set_router(self, r: Router):
        self.router = r

    def send_packet(self, p: Packet, target: str):
        logging.debug("Sending Packet", p, "to", target)
        if self.edges[target].a == self.router.address:
            self.edges[target].a.receive_packet(p)
        else:
            self.edges[target].b.receive_packet(p)
        #self.edges[target].send(p, target)

    def accept_packet(self, p: Packet, src: Edge):
        logging.debug("Received Packet", p, "from edge", src)
        self.router.receive_packet(p)

class Router:
    def __init__(self, address: str):
        self.edges = []
        self.neighbours = []
        self.address = address
        self.distances = {self.address: 0}
        self.to = {}
        self.data_layer = DataLayer()
        self.data_layer.set_router(self)
        self.packet_queues = {}

    def application_receive(self, data):
        print(data)
        print(self.address)

    def transport_send(self, content: str, to_addr: str):
        """Splits the content into packets and sends them"""
        # Each packet is of length 255 (§) is added to pad packets of length < 255
        # Each packet has a sequence number S_NUM (for reconstruction)
        # Each packet is sent with a NUM_P specifying the number of packets in content (for reconstruction)
        s_num = 0
        num_p = math.ceil(len(content)/255)
        while len(content) > 255:
            self.send_data(to_addr, {"HEAD": "DATA", "CONTENT": content[:255], "S_NUM": s_num, "NUM_P": num_p})
            content = content[255:]
            s_num += 1
        while len(content) < 255:
            content += "§"
        if len(content) != 0:
            self.send_data(to_addr, {"HEAD": "DATA", "CONTENT": "DATA", "CONTENT": content, "S_NUM": s_num, "NUM_P": num_p})

    def transport_receive(self, packet):
        if packet.from_addr not in self.packet_queues:
            self.packet_queues[packet.from_addr] = [packet.data]
        else:
            self.packet_queues[packet.from_addr].append(packet.data)
        if len(self.packet_queues[packet.from_addr]) == packet.data["NUM_P"]:
            data = self.reconstruct_data(self.packet_queues[packet.from_addr])
            while data[-1] == "§" and data[-2] != "\\":
                data = data[:-1]
            self.application_receive(data)

    def reconstruct_data(self, packets: []):
        packets.sort(key=lambda x: x["S_NUM"])
        data = ""
        for packet in packets:
            data += packet["CONTENT"]
        return data

    def send_distance_vector(self):
        """Sends current distance vector to all neighbours"""
        for neighbour in self.neighbours:
            self.send_data(neighbour.address, {"HEAD": "DV", "CONTENT": self.distances})

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

    def receive_packet(self, packet: Packet):
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
        self.distances[other_router.address] = edge.ticks_per_packet
        self.to[other_router.address] = other_router.address

    def register_edge(self, router: Router, edge: Edge):
        """Registers the link between this router to another router, while also setting the connection speed.

        Arguments:
            router {Router} -- The other router to link to.
            edge {Edge} -- The new edge.

        Returns:
            Edge -- The Edge object created for this connection."""
        self.edges.append(edge)
        self.neighbours.append(router)
        self.data_layer.edges[router.address] = edge
        self.update_dv(edge)

    def send_data(self, addr: str, data):
        """Sends data to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            data -- The data to send."""
        p = Packet(data, self.address, addr)
        self.data_layer.send_packet(p, self.where_to(p))