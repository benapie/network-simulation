from network_model import *
import logging

logging.basicConfig(level=logging.DEBUG)

routers = [Router("0"), Router("1"), Router("2"), Router("3"), Router("4"), Router("5")]
network = Network(routers)
network.link_to(routers[0], routers[1], 12)
network.link_to(routers[0], routers[2], 5)
network.link_to(routers[0], routers[3], 5)
network.link_to(routers[2], routers[1], 6)
network.link_to(routers[1], routers[4], 7)

for _ in range(10):
    for i in range(6):
        routers[i].send_distance_vector()
    for _ in range(100):
        network.network_tick()

routers[4].transport_send("Hello, World!", "3")
for i in range(100):
    #print("BEFORE TICK", i)
    network.network_tick()