from network_model import *
import logging

logging.basicConfig(level=logging.DEBUG)

network = Network()
routers = [Router("0"), Router("1"), Router("2"), Router("3"), Router("4"), Router("5")]
for router in routers:
    network.add_router(router)
network.link("0", "1", 12)
network.link("0", "2", 5)
network.link("0", "3", 5)
network.link("2", "1", 6)
network.link("1", "4", 7)

for _ in range(10):
    for i in range(6):
        routers[i].send_distance_vector()
    for _ in range(100):
        network.network_tick()

long_str = ""
for i in range(333):
    long_str += "xyza"

routers[4].transport_send(long_str, "3")
for i in range(500):
    # print("BEFORE TICK", i)
    network.network_tick()
