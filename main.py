"""

Virtual Networks Main File DurHack 2019

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

width = 500
random_network = randomly_generate_network()
node_list, edge_list = circle_arrangement(width / 2 - 20, width / 2, width / 2, random_network[0], random_network[1])
network = Network(node_list, edge_list)
vis = Visualisation(width, network)


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