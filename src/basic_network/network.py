from node import Router
from typing import List


class Network:
    def __init__(self, nodes: List[Node] = None):
        self.nodes = nodes
    def __init__(self, nodes: List[Router] = None):
        self.nodes = nodes

    def network_tick(self):
        """Ticks the network, ticking edges first then routers."""
        raise NotImplementedError("sdhfjsdf xD!! elvnne!")
