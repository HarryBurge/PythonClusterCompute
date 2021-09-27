#~ Imports
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from multiprocessing.managers import BaseManager
import multiprocessing


from Node import node

#~ Consts

#~ SimDNS
class DNS:
    def __init__(self):
        self._table= {} # {IP : {Port : actual_port}}
        self._freeport= 7010

    def get_actual_address(self, address):
        try:
            return self._table[address[0]][address[1]]
        except KeyError:
            return None

    def get_fake_address(self, address):
        for ip, d in self._table.items():
            for port, a in d.items():
                if (address==a):
                    return (ip, port)
        return None

    def set_actual_address(self, f_address, a_address):
        try:
            self._table[f_address[0]][f_address[1]]= a_address
        except KeyError:
            self._table[f_address[0]]= {}
            self._table[f_address[0]][f_address[1]]= a_address

    def next_actual_port(self):
        self._freeport+=1
        return self._freeport

    def next_fake_port(self, f_ip):
        try:
            temp= self._table[f_ip]
            return max(temp.keys())+1
        except KeyError:
            return None

    def print_table(self):
        print(self._table)

#~ SimNodes
class Nodes:
    def __init__(self, nodes):
        self._nodes= nodes
    def get(self, index):
        return self._nodes[index]
    def get_all(self):
        return self._nodes
    def set(self, index, item):
        self._nodes[index]= item


#~ Visualize
def visualize(nodes: Nodes, screen: object) -> bool:

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            return False

    screen.fill((255,255,255))
    
    def rotate(origin, point, angle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    deg= 2*math.pi/len(nodes.get_all())

    for n in nodes.get_all():
        for _,(tarip, _) in n.sockets:
            pygame.draw.line(screen, 
                (255, 0, 0), 
                rotate((500, 500), (500, 800), deg*int(n.ip.split('.')[-1])),
                rotate((500, 500), (500, 800), deg*int(tarip.split('.')[-1])),
                4
            )


    for n in nodes.get_all():
        pygame.draw.circle(screen, 
            (0, 0, 255), 
            rotate((500, 500), 
            (500, 800), 
            deg*int(n.ip.split('.')[-1])), 
            25
        )

    pygame.display.flip()
    return True


#~ Simulation
def main() -> None:

    pygame.init()
    screen = pygame.display.set_mode([1000, 1000])

    BaseManager.register('DNS', DNS)
    BaseManager.register('Nodes', Nodes)
    mn= BaseManager()
    mn.start()

    # Create DNS server
    dns= mn.DNS()

    # Create nodes
    nodes= mn.Nodes([node.Node('192.168.1.1', dns), node.Node('192.168.1.2', dns), node.Node('192.168.1.3', dns)])
   
    # Start nodes
    processes= []
    for i in range(len(nodes.get_all())):
        processes.append(
            multiprocessing.Process(target= node.run, args=(nodes,i,dns))
        )
        processes[-1].daemon= True
        processes[-1].start()

    # Visualize whats going on
    while visualize(nodes, screen):
        # print([x.ip for x in nodes.get_all()])
        # print(dns.print_table())
        pass

    pygame.quit()


if (__name__=='__main__'):
    main()
