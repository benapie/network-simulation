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

width = 750

# router_label_list = ["0", "1", "2", "3", "4", "5"]
# link_labels_list = [("0", "1"), ("0", "2"), ("0", "3"), ("2", "1"), ("1", "4")]
# link_delays = []
# for i in range(len(link_labels_list)):
#     link_delays.append(random.randint(4, 15))

router_label_list, link_labels_list = randomly_generate_network()
link_delays = []
for i in range(len(link_labels_list)):
    link_delays.append(random.randint(5, 40))

node_list, edge_list = circle_arrangement(width / 2 - 20, width / 2, width / 2, router_label_list, link_labels_list)
graphic_network = GraphicNetwork(node_list, edge_list)

vis = Visualisation(width, graphic_network)

network = Network(vis)

for router_label in router_label_list:
    network.add_router(Router(router_label))

for i in range(0, len(link_labels_list)):
    network.link(link_labels_list[i][0], link_labels_list[i][1], link_delays[i])


def main():
    start_time = time.time()
    frame_rate = 50
    frame_count = 0
    while True:
        frame_count += 1
        time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
        vis.tick()
        mouse = vis.window.checkMouse()
        network.network_tick()
        if frame_count % (frame_rate * 20) == 0:
            network.update_vectors()
        if frame_count % 30 == 0:
            # find a random pair
            router_a_address, router_b_address = "1", "1"
            while router_a_address == router_b_address:
                router_a_address = random.choice(list(network.router_dictionary.keys()))
                router_b_address = random.choice(list(network.router_dictionary.keys()))
            network.router_dictionary[router_a_address].transport_send("."*random.randint(200,1000), router_b_address)


main()

"""
</main>
"""
