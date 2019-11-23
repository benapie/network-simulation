from router import Router


class Edge:
    def __init__(self, a: Router, b: Router, ticks_per_packet: int):
        self.a = a
        self.b = b
        self.ticks_per_packet = ticks_per_packet

    def tick(self):
        """This will tick an edge along, moving every packet on the edge one
        tick along, while also manging sending to the routers if they arrive."""
        raise NotImplementedError("test testserser")
