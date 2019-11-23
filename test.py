from network_model import *
import logging

logging.basicConfig(level=logging.DEBUG)

routers = [Router("0"), Router("1"), Router("2"), Router("3")]
network = Network(routers)
network.link_to(routers[0], routers[1], 4)
network.link_to(routers[2], routers[3], 2)
network.link_to(routers[1], routers[3], 3)

# so should go 0 -> 1 -> 3 -> 2

for _ in range(5):
    for i in range(4):
        routers[i].send_distance_vector()
    for _ in range(100):
        network.network_tick()

routers[0].transport_send("Hello, World!", "2")
for i in range(10):
    print("BEFORE TICK", i)
    network.network_tick()