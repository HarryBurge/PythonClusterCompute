from cluster_node import Node
from sim_port import Port

import pygame
import math

class Sim:

    def __init__(self):

        self.nodes = {}

        for i in range(10):
            self.nodes[f"192.168.0.{i}"] = Node(self, f"192.168.0.{i}")


    def run(self, screen, clock):
        
        for k,d in self.nodes.items():
            d.run1()

        for k,d in self.nodes.items():
            d.run2()

        # for k,d in self.nodes.items():
        #     print(f"Node {k}")
        #     print(d)
        #     print("\n")

        while True:

            num = len(self.nodes.keys())
            size = int(math.sqrt(num))
            middle = 250 - (size * 100)/2

            for k,d in self.nodes.items():
                for pk, pd in d.ports.items():

                    if pd.target != None:
                        start = int(k.split(".")[-1])
                        end = int(pd.target.node.ip.split(".")[-1])

                        pygame.draw.line(screen, (0, 255, 0), (middle+(start%size)*100, middle+(start//size)*100), (middle+(end%size)*100, middle+(end//size)*100))

            for k,d in self.nodes.items():
                pygame.draw.circle(screen, (0, 0, 255), (middle+(int(k.split(".")[-1])%size)*100, middle+(int(k.split(".")[-1])//size)*100), 20)

            pygame.display.update()
            clock.tick(15)

    def connect_ip_port(self, node, selport, ip, port):
        try:

            # Establish connection - If target is listening
            if self.nodes[ip].ports[port].target == None:

                node.ports[selport] = Port(node, selport)
                node.ports[selport].set_target(self.nodes[ip].ports[port])
                self.nodes[ip].ports[port].set_target(node.ports[selport])

        except KeyError:
            raise ConnectionRefusedError


    def visualise(self):
        pass



if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    Sim().run(screen, clock)