import logging
from typing import Dict
from src.basic_network.edge import Edge
from src.basic_network.packet import Packet
from src.basic_network.router import Router


class DataLayer:
    edges: Dict[str, Edge]
    router: Router

    def __init__(self):
        self.edges = {}

    def set_router(self, r: Router):
        self.router = r

    def send_packet(self, p: Packet, target: str):
        logging.debug("Sending Packet", p, "to", target)
        self.edges[target].send(p, target)

    def accept_packet(self, p: Packet, src: Edge):
        logging.debug("Received Packet", p, "from edge", src)
        self.router.receive_packet(p)
