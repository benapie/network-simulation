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
height = 750

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
    mode_text = Text(Point(10, 10), "")
    mode_text.setTextColor("white")
    mode_text.draw(vis.window)

    while True:
        frame_count += 1
        time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
        vis.tick()
        mouse = vis.window.checkMouse()
        key = vis.window.checkKey()
        if key != "":
            if key == "r":
                mode_text.setText("r")
            elif key == "w":
                mode_text.setText("w")
            elif key == "a" and mode_text.getText() == "w":
                # Add node
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                vis.add_node(GraphicNode(str(frame_count), x, y))
                network.add_router(Router(str(frame_count)))

                # Get closest 2-4 nodes
                closest_node_list = vis.get_closest_node_label_list(x, y, random.randint(2, 4))
                for node_label in closest_node_list:
                    vis.add_edge_by_labels(str(frame_count), node_label)
                    network.link(str(frame_count), node_label, random.randint(5, 20))
            elif key == "a" and mode_text.getText() == "r":
                if len(vis.network.node_list) > 1:
                    x = random.randint(0, width - 1)
                    y = random.randint(0, height - 1)
                    nearest_router = vis.get_closest_node(x, y)
                    vis.network.remove_node_by_label(nearest_router)
                    network.delete_router(nearest_router)
            elif key == "d":
                if len(vis.network.node_list) > 1:
                    network.update_vectors()
            elif key == "p":
                router_list = vis.get_closest_node_label_list(0, 0, len(vis.network.node_list) - 1)
                for router in router_list:
                    vis.network.remove_node_by_label(router)
                    network.delete_router(router)
            elif key == "Escape":
                mode_text.setText("")
            elif key == "space":
                vis.window.getKey()
        if mouse is not None:
            if mode_text.getText() == "r":
                if len(vis.network.node_list) > 1:
                    nearest_router = vis.get_closest_node(mouse.x, mouse.y)
                    vis.network.remove_node_by_label(nearest_router)
                    network.delete_router(nearest_router)
            elif mode_text.getText() == "w":
                # Add node
                vis.add_node(GraphicNode(str(frame_count), mouse.x, mouse.y))
                network.add_router(Router(str(frame_count)))

                # Get closest 2-4 nodes
                closest_node_list = vis.get_closest_node_label_list(mouse.x, mouse.y, random.randint(2, 4))
                for node_label in closest_node_list:
                    vis.add_edge_by_labels(str(frame_count), node_label)
                    network.link(str(frame_count), node_label, random.randint(5, 20))
        network.network_tick()
        if frame_count % (frame_rate * 20) == 0:
            network.update_vectors()
        if frame_count % 30 == 0:
            router_a_address, router_b_address = "1", "1"
            if len(list(network.router_dictionary.keys())) >= 2:
                while router_a_address == router_b_address:
                    router_a_address = random.choice(list(network.router_dictionary.keys()))
                    router_b_address = random.choice(list(network.router_dictionary.keys()))
                network.router_dictionary[router_a_address].transport_send("."*random.randint(200, 1000), router_b_address)

main()

"""
</main>
"""
