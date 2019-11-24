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

router_label_list = ["0", "1", "2", "3", "4"]
link_labels_list = [("0", "1"), ("0", "2"), ("0", "3"), ("2", "1"), ("1", "4")]

network = Network([])

# for router_label in router_label_list:
#     network.router_list.append(Router(router_label))
# for link_label_list in link_labels_list:
#
#
# network.link_to(router_list[0], router_list[1], 12)
# network.link_to(router_list[0], router_list[2], 5)
# network.link_to(router_list[0], router_list[3], 5)
# network.link_to(router_list[2], router_list[1], 6)
# network.link_to(router_list[1], router_list[4], 7)

node_label_list = ["1"]
edge_label_list = []
#
# for router in router_list:
#     node_label_list.append(router.address)

node_label_list = ["0", "1", "2", "3", "4", "5"]
edge_label_list = [("0", "1"), ("0", "2"), ("0", "3"), ("2", "1"), ("1", "4")]
#
node_list, edge_list = circle_arrangement(width/2 - 20, width / 2, width / 2, node_label_list, edge_label_list)
network = GraphicNetwork(node_list, edge_list)

vis = Visualisation(width, network)

# network = GraphicNetwork(node_list, edge_list)
# vis = Visualisation(width, network)



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



def main():
    start_time = time.time()
    frame_rate = 50
    frame_count = 0
    while True:
        frame_count += 1
        time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
        vis.tick()
        vis.window.checkMouse()
        edge = vis.network.edge_list[random.randint(0, len(vis.network.edge_list)) - 1]

        vis.send_packet(edge.node_a_label, edge.node_b_label, random.randint(40, 100))


main()

"""
</main>
"""