#~ Imports
from multiprocessing import managers
import os
from socket import socket
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
import time
from pathos.multiprocessing import Pool
from multiprocessing.managers import BaseManager

from ComputeNode import node

#~ Consts

#~ Simulation
class Simulation:

    def __init__(self) -> None:
        self.nodes= []
        # self._screen= pygame.display.set_mode([1000,1000])

    def get_nodes(self) -> list:
        return self.nodes

    def add_nodes(self, nodes) -> None:
        self.nodes+=nodes

    def node_with_ip(self, ip) -> node.Node:
        for node in self.nodes:
            if node.ip==ip: 
                return node
        return None

    # def tcp(self, ip1, port1, ip2, port2, msg) -> bool:
    #     create_node= self.node_with_ip(ip1)
    #     target_node= self.node_with_ip(ip2)

    #     if (create_node and port1 in create_node.sockets.keys() and 
    #         target_node and port2 in target_node.sockets.keys()
    #     ):
    #         target_node.sockets[port2].buffer+= msg
    #         return True
    #     return False

    def visuals(self) -> bool:
        time.sleep(0.5)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return False

        self._screen.fill((255,255,255))
        
        def rotate(origin, point, angle):
            ox, oy = origin
            px, py = point

            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            return qx, qy

        deg= 2*math.pi/len(self.nodes)

        for node in self.nodes:
            for port, socket in node.sockets.items():
                if (port!=2000):
                    if (socket.tarport!=2000):
                        pygame.draw.line(self._screen, 
                            (255, 0, 0), 
                            rotate((500, 500), (500, 800), deg*int(socket.selip.split('.')[-1])),
                            rotate((500, 500), (500, 800), deg*int(socket.tarip.split('.')[-1])),
                            4
                        )
                    else:
                        pygame.draw.line(self._screen, 
                            (0, 255, 0), 
                            rotate((500, 500), (500, 800), deg*int(socket.selip.split('.')[-1])),
                            rotate((500, 500), (500, 800), deg*int(socket.tarip.split('.')[-1])),
                            4
                        )


        for node in self.nodes:
            pygame.draw.circle(self._screen, 
                                (0, 0, 255), 
                                rotate((500, 500), 
                                (500, 800), 
                                deg*int(node.ip.split('.')[-1])), 
                                25
            )

        pygame.display.flip()
        return True

    def run(self) -> None:
        self.add_nodes([node.Node('192.168.1.1', self), node.Node('192.168.1.2', self)])
        self.nodes[0].connect_to_node('192.168.1.2')


        p= Pool()

        # while self.visuals(screen):
        for i in range(2):
            time.sleep(0.5)

            self.nodes= p.map(node.Node.step, self.nodes)

            for i, j in enumerate(self.nodes):
                for com in j._push_changes:
                    exec(com)
                
                self.nodes[i]._push_changes= []
                self.nodes[i]._simulation= self


if __name__=='__main__':
    # pygame.init()

    BaseManager.register('Simulation', Simulation)
    manager= BaseManager()
    manager.start()

    s= manager.Simulation()
    # s.run()

    print(s.get_nodes())

    # pygame.quit()