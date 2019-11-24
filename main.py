"""

Virtual Networks Main File DurHack 2019

Ben Napier, Jacob Howes, Eric "the Refactor" Rodriguez

"""

"""
<imports>
"""

from network_model import *
from visualisation.main import *

"""
</imports>
"""

"""
<main>
"""

import logging

logging.basicConfig(level=logging.DEBUG)

width = 500

router_label_list = ["0", "1", "2", "3", "4", "5"]
link_labels_list = [("0", "1"), ("0", "2"), ("0", "3"), ("2", "1"), ("1", "4")]
link_delays = [12, 5, 5, 6, 7]

network = Network()

for router_label in router_label_list:
    network.add_router(Router(router_label))

for i in range(0, len(link_labels_list)):
    network.link(link_labels_list[i][0], link_labels_list[i][1],
                 link_delays[i])  # todo change to addresses

node_list, edge_list = circle_arrangement(width / 2 - 20, width / 2, width / 2, router_label_list, link_labels_list)
graphic_network = GraphicNetwork(node_list, edge_list)

vis = Visualisation(width, graphic_network)

#
# for _ in range(10):
#     for i in range(6):
#         routers[i].send_distance_vector()
#     for _ in range(100):
#         network.network_tick()
#
# long_str = ""
# for i in range(333):
#     long_str += "xyza"
#
# routers[4].transport_send(long_str, "3")
# for i in range(500):
#     # print("BEFORE TICK", i)
#     if i == 10:
#         network.link_to(routers[4], routers[5], 10)
#     network.network_tick()


# good test don't delete (pls)
# width = 500
# random_network = randomly_generate_network()
# node_list, edge_list = circle_arrangement(width / 2 - 20, width / 2, width / 2, random_network[0], random_network[1])
# network = GraphicNetwork(node_list, edge_list)
# vis = Visualisation(width, network)

for _ in range(10):
    for i in network.router_dictionary:
        network.router_dictionary[i].send_distance_vector()
    for _ in range(100):
        network.network_tick()

long_str = ""
for i in range(333):
    long_str += "xyza"



def main():
    start_time = time.time()
    frame_rate = 50
    frame_count = 0
    while True:
        frame_count += 1
        time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
        vis.tick()
        vis.window.checkMouse()
        network.network_tick()
        if frame_rate % 100 == 0:
            # find a random pair
            edge = network.edges[random.randint(0, len(network.edges) - 1)]
            network.router_dictionary[edge.a.router.address].transport_send("123", edge.b.router.address)
            # vis.send_packet(edge.a.router.address, edge.b.router.address, )


main()

"""
</main>
"""
