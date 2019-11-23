from visualisation.graphics import *
import math
import random

from visualisation.graphics import GraphWin, Circle, Point

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

node_list = []
edge_list = []

# initialise nodes
node_count = random.randint(3, 26)  # make this 26
for i in range(0, node_count):
    node_list.append(alphabet[i])

max_edge_count = node_count - 1
for i in node_list:
    edge_count = random.randint(0, max_edge_count)
    for j in range(0, edge_count):
        node = alphabet[random.randint(0, node_count - 1)]
        if node == i:
            next
        edge_list.append((i, node))
        
width = 300  # = height
win = GraphWin("", width, width)

r = 120  # radius of big circle

# Drawing nodes
nodes = []
for i in range(0, len(node_list)):
    theta = i * math.pi * 2 * math.pow(len(node_list), -1)
    c = Circle(Point(150 + (r * math.cos(theta)), 150 + (r * math.sin(theta))), 10)
    c.setFill("white")
    nodes.append(c)

edges = []
for i in range(0, len(edge_list)):
    a_point = nodes[node_list.index(edge_list[i][0])].getCenter()
    b_point = nodes[node_list.index(edge_list[i][1])].getCenter()
    ab_line = Line(a_point, b_point)
    edges.append(ab_line)
    print(a_point, b_point)
for i in edges:
    i.draw(win)
for i in nodes:
    i.draw(win)


input()

