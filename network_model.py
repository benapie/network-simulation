from __future__ import annotations
from typing import List, Dict, Optional, Deque
import math
from collections import deque
from random import Random
import random


class Edge:
    a: Device
    b: Device
    ticks_for_data_passthrough: int
    curr_tick: int
    data_in_transit: Optional[Edge.TransitData]
    data_waiting: Deque[Edge.TransitData]
    main_rng: Random

    class TransitData:
        target: Device
        end_tick: int

        def __init__(self, data, target: Device, end_tick):
            self.data = data
            self.target = target
            self.end_tick = end_tick

    def __init__(self, a: Device, b: Device, ticks_for_data_passthrough: int):
        self.a = a
        self.b = b
        self.ticks_for_data_passthrough = ticks_for_data_passthrough
        self.data_in_transit = None
        self.data_waiting = deque()
        self.main_rng = Random()
        self.curr_tick = 0

    def send_data_through(self, data, sender: Device):
        end_tick = self.ticks_for_data_passthrough + self.main_rng.randint(0, 3*self.ticks_for_data_passthrough)
        if self.data_in_transit is None:
            end_tick += self.curr_tick
            self.data_in_transit = Edge.TransitData(data, self.a if sender != self.a else self.b, end_tick)
        else:
            self.data_waiting.append(Edge.TransitData(data, self.a if sender != self.a else self.b, end_tick))

    def tick(self):
        """This will tick an edge along, moving every packet on the edge one
        tick along, while also manging sending to the routers if they arrive."""
        self.curr_tick += 1
        if self.data_in_transit is not None and self.data_in_transit.end_tick == self.curr_tick:
            self.data_in_transit.target.accept_data(self.data_in_transit.data, self)
            if len(self.data_waiting) == 0:
                self.data_in_transit = None
            else:
                self.data_in_transit = self.data_waiting.popleft()
                self.data_in_transit.end_tick += self.curr_tick

    def __str__(self):
        return str(self.a) + " -> " + str(self.b)


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

    def __str__(self):
        return "D#" + str(self.router)

    def remove_edge(self, address: str):
        del self.edges[address]


# Packet stands alone, should not be doing **anything** should just sit there and take it!
class Packet:
    def __init__(self, data, from_addr, to_addr):
        self.data = data
        self.from_addr = from_addr
        self.to_addr = to_addr

    def __str__(self):
        return str(self.data) + ", " + self.from_addr + " -> " + self.to_addr


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
        print(data)
        print(self.address)

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
            d = ""
            for p in packets:
                d += p["CONTENT"]
            return d

        if packet.from_addr not in self.packet_queues:
            self.packet_queues[packet.from_addr] = [packet.data]
        else:
            self.packet_queues[packet.from_addr].append(packet.data)
        if len(self.packet_queues[packet.from_addr]) == packet.data["NUM_P"]:
            data = reconstruct_data(self.packet_queues[packet.from_addr])
            while data[-1] == "§" and data[-2] != "\\":
                data = data[:-1]
            self.application_receive(data)

    def send_distance_vector(self):
        """Sends current distance vector to all neighbours"""
        for neighbour in self.neighbours:
            self.send_new_packet(neighbour.address, {"HEAD": "DV", "CONTENT": self.distances})

    def update_distance_vector(self, dv_packet: Packet):
        """Upon receiving a distance vector from neighbours, each Router updates its vector to contain the most recent
        information regarding the optimum distance to other nodes"""
        to_remove = []
        for node in self.to:
            if self.to[node] == dv_packet.from_addr and node not in dv_packet.data["CONTENT"]:
                to_remove.append(node)
        for node in to_remove:
            self.to.pop(node)
            self.distances.pop(node)
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
        if packet.to_addr not in self.to:
            return random.choice(list(self.to.values()))
        return self.to[packet.to_addr]

    def receive_packet(self, packet: Packet):
        """Decides what needs to be done with the received packet"""
        if packet.to_addr == self.address:
            if packet.data["HEAD"] == "DV":
                self.update_distance_vector(packet)  # accept DV packet as something to process independently
            elif packet.data["HEAD"] == "DEL":
                self.remove_router(packet)
            else:
                self.transport_receive(packet)
        else:
            self.device.send_data(packet, self.where_to(packet))  # routes packet to next hop if that's what's needed

    def remove_router(self, packet):
        self.distances.pop(packet.from_addr)
        self.send_distance_vector()
        self.device.remove_edge(packet.from_addr)

    def register_edge(self, router: Router, edge: Edge):
        """Registers the link between this router to another router."""
        self.neighbours.append(router)
        self.device.add_edge(edge, router.address)
        if router.address not in self.distances.keys() or \
                edge.ticks_for_data_passthrough <= self.distances[router.address]:
            self.distances[router.address] = edge.ticks_for_data_passthrough
            self.to[router.address] = router.address
        self.send_distance_vector()

    def send_del(self):
        """Sends a delete packet to neighbours"""
        for neighbour in self.neighbours:
            self.send_new_packet(neighbour.address, {"HEAD": "DEL", "CONTENT": "It's been fun boys"})

    def send_new_packet(self, addr: str, data):
        """Sends data to addr. If this is unknown,
        query network layer over where to send it to.

        Arguments:
            addr {str} -- The address of the target.
            data -- The data to send."""
        p = Packet(data, self.address, addr)
        self.device.send_data(p, self.where_to(p))

    def __str__(self):
        return self.address


class Network:
    router_list: Dict[str, Router]
    edges: List[Edge]

    def __init__(self):
        self.router_list = {}
        self.edges = []

    def add_router(self, router: Router):
        self.router_list[router.address] = router

    def get_router(self, addr: str) -> Router:
        return self.router_list[addr]

    def delete_router(self, addr: str):
        """Deletes a router"""
        self.router_list[addr].send_del()
        del self.router_list[addr]

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
