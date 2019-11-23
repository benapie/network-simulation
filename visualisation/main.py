from visualisation.graphics import *
import math
import random
import time

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

node_list = []
edge_list = []

# initialise nodes
node_count = random.randint(3, 10)  # make this 26
for i in range(0, node_count):
    node_list.append(alphabet[i])

max_edge_count = min(5, node_count - 1)
for i in node_list:
    edge_count = random.randint(0, max_edge_count)
    for j in range(1, edge_count):
        node = alphabet[random.randint(0, node_count - 1)]
        if node != i:
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
for i in edges:
    i.draw(win)
for i in nodes:
    i.draw(win)

# Pick an edge
edge = edge_list[random.randint(0, len(edge_list) - 1)]
print(edge)

# Lets animate a packet
# Initial position
packet = Circle(nodes[node_list.index(edge[0])].getCenter(), 5)
packet.setFill("black")
packet.draw(win)
# Calculate difference vector
frame_count = 25
dx = (nodes[node_list.index(edge[1])].getCenter().x - nodes[node_list.index(edge[0])].getCenter().x) * math.pow(25, -1)
dy = (nodes[node_list.index(edge[1])].getCenter().y - nodes[node_list.index(edge[0])].getCenter().y) * math.pow(25, -1)

# while True:
#     win.getMouse()
#     packet.move(dx / 10, dy / 10)


start_time = time.time()
frame_rate = 60
i = 0
win.getMouse()
while True:
    time.sleep(math.pow(frame_rate, -1) - ((time.time() - start_time) % math.pow(frame_rate, -1)))
    win.checkMouse()
    if i < frame_count:
        packet.move(dx, dy)
        i += 1
