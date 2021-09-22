#~ Imports
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from multiprocessing.managers import BaseManager
import multiprocessing


from ComputeNode import node

#~ Consts

#~ Sharedlistclass
class Nodes:
    def __init__(self, nodes):
        self._nodes= nodes
    def get(self, index):
        return self._nodes[index]
    def get_all(self):
        return self._nodes
    def get_ip_index(self, ip):
        for i in range(len(self._nodes)):
            if self._nodes[i].ip==ip:
                return i
        return None
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
        for port, socket in n.sockets.items():
            if (port!=2000):
                if (socket.tarport!=2000):
                    pygame.draw.line(screen, 
                        (255, 0, 0), 
                        rotate((500, 500), (500, 800), deg*int(socket.selip.split('.')[-1])),
                        rotate((500, 500), (500, 800), deg*int(socket.tarip.split('.')[-1])),
                        4
                    )
                else:
                    pygame.draw.line(screen, 
                        (0, 255, 0), 
                        rotate((500, 500), (500, 800), deg*int(socket.selip.split('.')[-1])),
                        rotate((500, 500), (500, 800), deg*int(socket.tarip.split('.')[-1])),
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

    BaseManager.register('Nodes', Nodes)
    mn= BaseManager()
    mn.start()

    # Create nodes
    nodes= mn.Nodes([node.Node('192.168.1.1'), node.Node('192.168.1.2')])
   
    # Start nodes
    processes= []
    for i in range(len(nodes.get_all())):
        processes.append(
            multiprocessing.Process(target= node.run, args=(nodes,i))
        )
        processes[-1].start()

    # Visualize whats going on
    while visualize(nodes, screen):
        print([x.ip for x in nodes.get_all()])
        pass

    pygame.quit()


if (__name__=='__main__'):
    main()
