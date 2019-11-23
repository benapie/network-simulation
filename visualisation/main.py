from visualisation.graphics import *
import math
import random
import time

class Node:
    def __init__(self, label, x, y, r):
        self.label = label
        self.x = x
        self.y = y
        self.circle = Circle(Point(x, y), r)
        self.circle.setFill("white")

class Edge:
    def __init__(self, node_a, node_b):
        self.node_a_label = node_a.label
        self.node_b_label = node_b.label
        self.line = Line(node_a.circle.getCenter(), node_b.circle.getCenter())

class Network:
    def __init__(self, node_list, edge_list):
        self.node_list = node_list
        self.edge_list = edge_list

class Visualisation:
    def __init__(self, width, network):
        self.width = width
        self.window = GraphWin("", width, width)
        for edge in network.edge_list:
            edge.line.draw(self.window)
        for node in network.node_list:
            node.circle.draw(self.window)
        self.window.getMouse()

    def start(self):
        pass


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
        node_list.append(Node(node_label_list[i],         # label
                         x + (r * math.cos(theta)),  # x coordinate
                         y + (r * math.sin(theta)),  # y coordinate
                          10))                        # radius
    # Drawing edges
    edge_list = []
    for i in range(0, len(edge_label_list)):
        node_a = node_list[node_label_list.index(edge_label_list[i][0])]
        node_b = node_list[node_label_list.index(edge_label_list[i][1])]
        edge_list.append(Edge(node_a, node_b))

    return node_list, edge_list


def randomly_generate_network():
    """
        Randomly generates a list of nodes (A-Z) and edges
        :return: (node_label_list, edge_label_list) where edge_label_list = [node_a.label, node_b.label]
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    node_list = []
    edge_list = []
    # generate nodes
    node_count = random.randint(5, 15)  # make this 26
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
    print(edge_list)
    return node_list, edge_list


node_label_list = ['A', 'B', 'C', 'D']
edge_label_list = [('A', 'B'), ('A', 'D'), ('B', 'D'), ('A', 'C')]
# nodes = [Node('A', 50, 50, 10), Node('B', 100, 100, 10), Node('C', 100, 50, 10)]
# edges = [Edge(nodes[0], nodes[1])]
width = 750
random_network = randomly_generate_network()
node_list, edge_list = circle_arrangement(width / 2 - 20, width / 2, width / 2, random_network[0], random_network[1])
network = Network(node_list, edge_list)
vis = Visualisation(width, network)

#
#
# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#
# node_list = []
# edge_list = []
#
# # initialise nodes
# node_count = random.randint(3, 10)  # make this 26
# for i in range(0, node_count):
#     node_list.append(alphabet[i])
#
# max_edge_count = min(5, node_count - 1)
# for i in node_list:
#     edge_count = random.randint(0, max_edge_count)
#     for j in range(1, edge_count):
#         node = alphabet[random.randint(0, node_count - 1)]
#         if node != i:
#             edge_list.append((i, node))
#
# width = 300  # = height
# win = GraphWin("", width, width)
#
# r = 120  # radius of big circle
#
# # Drawing nodes
# nodes = []
# for i in range(0, len(node_list)):
#     theta = i * math.pi * 2 * math.pow(len(node_list), -1)
#     c = Circle(Point(150 + (r * math.cos(theta)), 150 + (r * math.sin(theta))), 10)
#     c.setFill("white")
#     nodes.append(c)
#
# edges = []
# for i in range(0, len(edge_list)):
#     a_point = nodes[node_list.index(edge_list[i][0])].getCenter()
#     b_point = nodes[node_list.index(edge_list[i][1])].getCenter()
#     ab_line = Line(a_point, b_point)
#     edges.append(ab_line)
# for i in edges:
#     i.draw(win)
# for i in nodes:
#     i.draw(win)
#
# # Pick an edge
# edge = edge_list[random.randint(0, len(edge_list) - 1)]
# print(edge)
#
# # Lets animate a packet
# # Initial position
# packet = Circle(nodes[node_list.index(edge[0])].getCenter(), 5)
# packet.setFill("black")
# packet.draw(win)
# # Calculate difference vector
# frame_count = 25
# dx = (nodes[node_list.index(edge[1])].getCenter().x - nodes[node_list.index(edge[0])].getCenter().x) * math.pow(25, -1)
# dy = (nodes[node_list.index(edge[1])].getCenter().y - nodes[node_list.index(edge[0])].getCenter().y) * math.pow(25, -1)
#
# # while True:
# #     win.getMouse()
# #     packet.move(dx / 10, dy / 10)
#
#
# start_time = time.time()
# frame_rate = 60
# i = 0
# win.getMouse()
# while True:
#     time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
#     win.checkMouse()
#     if i < frame_count:
#         packet.move(dx, dy)
#         i += 1
