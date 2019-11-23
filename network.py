class Router:
    def __init__(self, address):
        self.address = address
    def tick(self, packets):
        '''Router processes all incoming packets and sends outgoing packet(s)'''
        pass

class Packet: #Probably just make packets dictionaries themselves (or JSON objects or something)
    def __init__(self, content, destination, sender):
        self.content = content
        self.sender = sender
        self.destination = destination

routers = ['''A bunch or Routers''']

while True:
    packets = {'''A dictionary of lists of packets indexed by router address'''}
    for router in routers:
        router.tick(packets[router.address])