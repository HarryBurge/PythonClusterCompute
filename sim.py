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
        
        while True:

            screen.fill((0,0,0))

            for k,d in self.nodes.items():
                d.run1()

            for k,d in self.nodes.items():
                d.run2()

            for k,d in self.nodes.items():
                print(f"Node {d.ip}")
                print(str(d))

            def rotate(angle):
                s = math.sin(angle)
                c = math.cos(angle)
                return (250 + 150*c - 0*s, 250 + 150*s + 0*c)

            num = len(self.nodes.keys())
            angle = 2*math.pi/num

            # Draw connections
            for k,d in self.nodes.items():
                for pk, pd in d.ports.items():
                    if pd.target != None:
                        start = int(k.split(".")[-1])
                        end = int(pd.target.node.ip.split(".")[-1])

                        pygame.draw.line(screen, (255, 255, 255), rotate(start*angle), rotate(end*angle), 4)

            # Draw nodes
            for k,d in self.nodes.items():
                ind = int(k.split(".")[-1])
                pygame.draw.circle(screen, (0, 0, 255), rotate(ind*angle), 20)

            pygame.display.update()
            clock.tick(2)


    def connect_ip_port(self, node, selport, ip, port):
        try:

            # Establish connection - If target is listening
            if self.nodes[ip].ports[port].target == None:
                self.nodes[ip].ports[port].set_target(node.ports[selport])
                node.ports[selport].set_target(self.nodes[ip].ports[port])

        except:
            raise ConnectionRefusedError



if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    Sim().run(screen, clock)