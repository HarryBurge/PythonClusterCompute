from cluster_node import Node
from sim_port import Port

import pygame
import math
import threading


class Sim:

    def __init__(self):

        self.nodes = {}

        for i in range(10):
            self.nodes[f"192.168.0.{i}"] = Node(self, f"192.168.0.{i}")


    def run(self, screen, clock):

        for k,d in self.nodes.items():
            tom = threading.Thread(target=Node.run, args=(d,))
            tom.setDaemon = True
            tom.start()
        
        while True:

            screen.fill((0,0,0))

            # for k,d in self.nodes.items():
            #     print(f"Node {d.ip}")
            #     print(str(d))

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
            clock.tick(60)


    def connect_ip_port(self, selip, selport, tarip, tarport):
        try:

            if self.nodes[tarip].ports[tarport].target==None and self.nodes[selip].ports[selport].target==None:

                self.nodes[selip].ports[selport].target= self.nodes[tarip].ports[tarport]
                self.nodes[tarip].ports[tarport].target= self.nodes[selip].ports[selport].target
            
            else:
                raise ConnectionRefusedError

        except:
            raise ConnectionRefusedError



if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    Sim().run(screen, clock)