from __future__ import annotations
import logging
from typing import List, Dict, Tuple, Any
import math


class Edge:
    data_in_transit: List[Tuple[Any, Device, int]]

    def __init__(self, a: Device, b: Device, ticks_for_data_passthrough: int):
        self.a = a
        self.b = b
        self.ticks_for_data_passthrough = ticks_for_data_passthrough
        self.data_in_transit = []

    def send_data_through(self, data, sender: Device):
        self.data_in_transit.append((data, self.a if sender != self.a else self.b, 0))

    def tick(self):
        """This will tick an edge along, moving every packet on the edge one
        tick along, while also manging sending to the routers if they arrive."""
        for i in range(len(self.data_in_transit)):
            self.data_in_transit[i] = (self.data_in_transit[i][0],
                                       self.data_in_transit[i][1], self.data_in_transit[i][2] + 1)
        for data, tar, ticks in self.data_in_transit:
            if ticks == self.ticks_for_data_passthrough:
                tar.accept_data(data, self)
        self.data_in_transit = [t for t in self.data_in_transit if t[2] < self.ticks_for_data_passthrough]

    def get_data_in_transit(self) -> List[Any, Device, int]:
        return self.data_in_transit


class Device:
    edges: Dict[str, Edge]
    router: Router

    def __init__(self):
        self.edges = {}

    def set_router(self, r: Router):
        self.router = r

    def send_data(self, data, target: str):
        print("Sending data", data, "to", target)
        self.edges[target].send_data_through(data, self)

    def accept_data(self, data, src: Edge):
        print("Received data", data, "from edge", src)
        self.router.receive_packet(data)

    def add_edge(self, edge: Edge, address: str):
        self.edges[address] = edge


# Packet stands alone, should not be doing **anything** should just sit there and take it!
class Packet:
    def __init__(self, data, from_addr, to_addr):
        self.data = data
        self.from_addr = from_addr
        self.to_addr = to_addr


class Router:
    neighbours: List[Router]
    distances: Dict[str, int]
    address: str
    to: Dict[str, str]
    device: Device

    def __init__(self, address: str):
        self.neighbours = []
        self.address = address
        self.distances = {self.address: 0}
        self.to = {}
        self.device = Device()
        self.device.set_router(self)
        self.packet_queues = {}

    def application_receive(self, data):
        pass

    def transport_send(self, content: str, to_addr: str):
        """Splits the content into packets and sends them"""
        # Each packet is of length 255 (§) is added to pad packets of length < 255
        # Each packet has a sequence number S_NUM (for reconstruction)
        # Each packet is sent with a NUM_P specifying the number of packets in content (for reconstruction)
        content.replace("§", "\\§")
        s_num = 0
        num_p = math.ceil(len(content)/255)
        while len(content) > 255:
            self.send_new_packet(to_addr, {"HEAD": "DATA", "CONTENT": content[:255], "S_NUM": s_num, "NUM_P": num_p})
            content = content[255:]
            s_num += 1
        while len(content) < 255:
            content += "§"
        if len(content) != 0:
            self.send_new_packet(to_addr, {"HEAD": "DATA", "CONTENT": content, "S_NUM": s_num, "NUM_P": num_p})

    def transport_receive(self, packet):
        def reconstruct_data(packets: []):
            packets.sort(key=lambda x: x["S_NUM"])
            data = ""
            for p in packets:
                data += p["CONTENT"]
            return data

        if packet.from_addr not in self.packet_queues:
            self.packet_queues[packet.from_addr] = [packet.data]
        else:
            self.packet_queues[packet.from_addr].append(packet.data)
        if len(self.packet_queues[packet.from_addr]) == packet.data["NUM_P"]:
            self.application_receive(reconstruct_data(self.packet_queues[packet.from_addr]))  # TODO: change app

    def send_distance_vector(self):
        """Sends current distance vector to all neighbours"""
        for neighbour in self.neighbours:
            self.send_new_packet(neighbour.address, {"HEAD": "DV", "CONTENT": self.distances})

    def update_distance_vector(self, dv_packet: Packet):
        """Upon receiving a distance vector from neighbours, each Router updates its vector to contain the most recent
        information regarding the optimum distance to other nodes"""
        for node in dv_packet.data["CONTENT"]:
            if node not in self.distances:
                self.distances[node] = dv_packet.data["CONTENT"][node] + self.distances[dv_packet.from_addr]
                self.to[node] = dv_packet.from_addr
            else:
                if self.distances[node] > dv_packet.data["CONTENT"][node] + self.distances[dv_packet.from_addr]:
                    self.distances[node] = dv_packet.data["CONTENT"][node] + self.distances[dv_packet.from_addr]
                    self.to[node] = dv_packet.from_addr

    def where_to(self, packet: Packet) -> str:
        """Return where to send the packet."""
        return self.to[packet.to_addr]

    def receive_packet(self, packet: Packet):
        """Decides what needs to be done with the received packet"""
        if packet.to_addr == self.address:
            if packet.data["HEAD"] == "DV":
                self.update_distance_vector(packet)  # accept DV packet as something to process independently
            else:
                self.transport_receive(packet)
        else:
            self.device.send_data(packet, self.where_to(packet))  # routes packet to next hop if that's what's needed

    def register_edge(self, router: Router, edge: Edge):
        """Registers the link between this router to another router."""
        self.neighbours.append(router)
        self.device.add_edge(edge, router.address)
        if router.address not in self.distances.keys() or \
                edge.ticks_for_data_passthrough <= self.distances[router.address]:
            self.distances[router.address] = edge.ticks_for_data_passthrough
            self.to[router.address] = router.address

    def send_new_packet(self, addr: str, data):
        """Sends data to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            data -- The data to send."""
        p = Packet(data, self.address, addr)
        self.device.send_data(p, self.where_to(p)) #


class Network:
    def __init__(self, routers: List[Router] = None):
        self.routers = routers
        self.edges = []

    def link_to(self, x: Router, y: Router, ticks_for_data_passthrough: int) -> Edge:
        """Links two routers together,
        while also setting the connection speed.

        Arguments:
            x {Router} -- One of the routers to link to.
            y {Router} -- The other router to link to.
            ticks_per_packet {int} -- The connection speed.

        Returns:
            Edge -- The Edge object created for this connection."""
        edge = Edge(x.device, y.device, ticks_for_data_passthrough)
        self.edges.append(edge)
        x.register_edge(y, edge)
        y.register_edge(x, edge)
        return edge

    def network_tick(self):
        """Ticks all edges."""
        for edge in self.edges:
            edge.tick()
