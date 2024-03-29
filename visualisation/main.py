import math
import random

from visualisation.graphics import *


class GraphicNode:
    def __init__(self, label, x, y, r=10):
        self.label = label
        self.x = x
        self.y = y
        self.circle = Circle(Point(x, y), r)
        self.circle.setOutline("white")
        self.color = color_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.circle.setFill(self.color)


class GraphicEdge:
    def __init__(self, node_a, node_b):
        self.node_a_label = node_a.label
        self.node_b_label = node_b.label
        self.line = Line(node_a.circle.getCenter(), node_b.circle.getCenter())
        self.line.setFill("white")


class GraphicNetwork:
    def __init__(self, node_list, edge_list):
        self.node_list = node_list
        self.edge_list = edge_list

    def add_node(self, new_node):
        for node in self.node_list:
            if new_node.label == node.label:
                raise ValueError("Error on entry of node to a network. "
                                 "Node label already in the network.")
            else:
                self.node_list.append(new_node)
                return

    def add_edge(self, new_edge):
        inverted_edge = GraphicEdge(self.get_node_by_label(new_edge.node_b_label),
                                    self.get_node_by_label(new_edge.node_a_label))
        if new_edge not in self.edge_list and inverted_edge not in self.edge_list:
            self.edge_list.append(new_edge)

    def add_edge_by_labels(self, node_a_label, node_b_label):
        if self.edge_exist_by_labels(node_a_label, node_b_label):
            return
        self.add_edge(self.get_node_by_label(node_a_label), self.get_node_by_label(node_b_label))

    def edge_exist_by_labels(self, node_a_label, node_b_label):
        for edge in self.edge_list:
            if edge.node_a_label == node_a_label and edge.node_b_label == node_b_label:
                return True
        return False

    def get_edge_by_labels(self, node_a_label, node_b_label):
        for edge in self.edge_list:
            if edge.node_a_label == node_a_label and edge.node_b_label == node_b_label:
                return edge
        return None

    def get_node_by_label(self, node_label):
        for node in self.node_list:
            if node.label == node_label:
                return node
        return None

    def remove_node_by_label(self, node_label):
        """ Removes a node by label, will not throw an error if it is not found """
        found_node = None
        for node in self.node_list:
            if node.label == node_label:
                node.circle.undraw()
                self.node_list.remove(node)
                found_node = node_label
                break
        if found_node is None:
            return
        edge_death_note = []
        for edge in self.edge_list:
            if found_node == edge.node_a_label or found_node == edge.node_b_label:
                edge_death_note.append(edge)
                edge.line.undraw()
        for edge in edge_death_note:
            self.edge_list.remove(edge)

    def remove_edge_by_labels(self, node_a_label, node_b_label):
        """ Removes the edge that has node_a_label and node_b_label (could be the opposite way around) """
        for edge in self.edge_list:
            if edge.node_a_label == node_a_label and edge.node_b_label == node_b_label:
                edge.line.undraw()
                self.edge_list.remove(edge)
                return
            if edge.node_b_label == node_a_label and edge.node_a_label == node_b_label:
                edge.line.undraw()
                self.edge_list.remove(edge)
                return

    def remove_edge(self, edge_to_remove):
        """ Removes the edge (goes by label of the nodes) """
        self.remove_edge_by_labels(edge_to_remove.node_a_label, edge_to_remove.node_b_label)


class Visualisation:
    def __init__(self, width, network):
        self.width = width
        self.network = network
        self.window = GraphWin("", width, width, autoflush=False)
        self.window.setBackground("black")
        self.packet_list = []
        for edge in network.edge_list:
            edge.line.draw(self.window)
        for node in network.node_list:
            node.circle.draw(self.window)

    def tick(self):
        self.tick_packet()

    def tick_packet(self):
        packet_death_note = []
        for packet in self.packet_list:
            if packet.tick() == 1:
                packet_death_note.append(packet)
        for packet in packet_death_note:
            packet.square.undraw()
            self.packet_list.remove(packet)

    def add_node(self, new_node):
        new_node.circle.draw(self.window)
        self.network.add_node(new_node)

    def add_edge_by_labels(self, node_a, node_b):
        if not self.network.edge_exist_by_labels(node_a, node_b):
            edge = GraphicEdge(self.network.get_node_by_label(node_a), self.network.get_node_by_label(node_b))
            edge.line.draw(self.window)
            self.network.add_edge(edge)

    def send_packet(self, node_a_label, node_b_label, node_origin_label, frame_count, outline_opacity=1):
        """ Visualises a packet going from node A to node B """
        # find the nodes
        node_a = self.network.get_node_by_label(node_a_label)
        node_b = self.network.get_node_by_label(node_b_label)
        node_origin = self.network.get_node_by_label(node_origin_label)

        if None in [node_a, node_b, node_origin]:
            return

        packet = Packet(node_a.circle.getCenter().x,
                        node_a.circle.getCenter().y,
                        node_b.circle.getCenter().x,
                        node_b.circle.getCenter().y,
                        frame_count,
                        node_origin.color,
                        outline_opacity)
        packet.square.draw(self.window)

        self.packet_list.append(packet)

    def color_curve(self, x):
        return math.pow(math.e, -1 * math.pow(3, -1) * x)

    def update_edge_queue(self, node_a_label, node_b_label, queue_length):
        if self.network.edge_exist_by_labels(node_a_label, node_b_label):
            self.network.get_edge_by_labels(node_a_label, node_b_label).line.setFill(
                color_rgb(255, int(255 * self.color_curve(queue_length)), int(255 * self.color_curve(queue_length))))

    def get_closest_node(self, x, y):
        min_node = self.network.node_list[0]
        min_distance = math.pow(math.pow(min_node.x - x, 2) + math.pow(min_node.y - y, 2), 0.5)
        for node in self.network.node_list:
            distance = math.pow(math.pow(node.x - x, 2) + math.pow(node.y - y, 2), 0.5)
            if distance < min_distance:
                min_node = node
                min_distance = distance
        return min_node.label

    def get_closest_node_label_list(self, x, y, count):
        count = min(count, len(self.network.node_list) - 1)
        node_distance_list = []
        for node in self.network.node_list:
            distance = math.pow(math.pow(node.x - x, 2) + math.pow(node.y - y, 2), 0.5)
            node_distance_list.append((node.label, distance))

        node_distance_list = sorted(node_distance_list, key=lambda x: x[1])[1:]
        node_list = []
        for node_distance in node_distance_list:
            if node_distance[1] != 0:
                node_list.append(node_distance[0])
        return node_list[:count]


def circle_arrangement(r, x, y, node_label_list, edge_label_list):
    """
        Will take a list of node labels and a list of edges (of the form [(node_a_label, node_b_label), ...]) and return
        some nice Edge and Node objects in a nice circle arrangement.

        :argument r:               the radius of the circle arrangement
        :argument x:               x coordinate of the midpoint
        :argument y:               y coordinate of the midpoint
        :argument node_label_list: as above
        :argument edge_label_list: as above

        :return: 2-tuple of a list of nodes and a list of edges ([Node], [Edge])
    """
    # Drawing nodes
    node_list = []
    for i in range(0, len(node_label_list)):
        theta = i * math.pi * 2 * math.pow(len(node_label_list), -1)
        node_list.append(GraphicNode(node_label_list[i],  # label
                                     x + (r * math.cos(theta)),  # x coordinate
                                     y + (r * math.sin(theta)),  # y coordinate
                                     10))  # radius
    # Drawing edges
    edge_list = []
    for i in range(0, len(edge_label_list)):
        node_a = node_list[node_label_list.index(edge_label_list[i][0])]
        node_b = node_list[node_label_list.index(edge_label_list[i][1])]
        edge_list.append(GraphicEdge(node_a, node_b))

    return node_list, edge_list


def randomly_generate_network(node_count_lower_bound=10, node_count_upper_bound=20):
    """
        Randomly generates a list of nodes (A-Z) and edges
        :return: (node_label_list, edge_label_list) where edge_label_list = [node_a.label, node_b.label]
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    node_list = []
    edge_list = []
    # generate nodes
    node_count = random.randint(node_count_lower_bound, node_count_upper_bound)  # make this 26
    for i in range(0, node_count):
        node_list.append(alphabet[i])
    # generate edges
    max_edge_count = min(5, node_count - 1)
    for i in node_list:
        edge_count = random.randint(0, max_edge_count)
        for j in range(1, edge_count):
            node = alphabet[random.randint(0, node_count - 1)]
            while node == i or (node, i) in edge_list or (i, node) in edge_list:
                node = alphabet[random.randint(0, node_count - 1)]
            edge_list.append((i, node))
    return node_list, edge_list


class Packet:
    def __init__(self, node_a_position_x, node_a_position_y, node_b_position_x, node_b_position_y, frame_count_max,
                 color="black", outline_opacity=1.):
        self.square = Rectangle(Point(node_a_position_x - 5, node_a_position_y - 5),
                                Point(node_a_position_x + 5, node_a_position_y + 5))
        self.square.setFill(color)
        self.square.setOutline(
            color_rgb(int(255 * outline_opacity), int(255 * outline_opacity), int(255 * outline_opacity)))
        self.dx = (node_b_position_x - node_a_position_x) / frame_count_max
        self.dy = (node_b_position_y - node_a_position_y) / frame_count_max
        self.frame_count = 0
        self.frame_count_max = frame_count_max

    def tick(self):
        self.square.move(self.dx, self.dy)
        self.frame_count += 1
        return self.frame_count == self.frame_count_max

# Following is testing stuff
# def main():
#     start_time = time.time()
#     frame_rate = 50
#     frame_count = 0
#     while True:
#         frame_count += 1
#         time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
#         vis.tick()
#         vis.window.checkMouse()
#         edge = vis.network.edge_list[random.randint(0, len(vis.network.edge_list)) - 1]
#
#         vis.send_packet(edge.node_a_label, edge.node_b_label, random.randint(40, 100))
#
#
# ## Testing!!
# width = 500
# random_network = randomly_generate_network()
# node_list, edge_list = circle_arrangement(width / 2 - 20, width / 2, width / 2, random_network[0], random_network[1])
# network = Network(node_list, edge_list)
# vis = Visualisation(width, network)
#
# main()
