#~ Imports
from cluster_node import *
import pygame
import math

#~ Constants
NUM_NODES= 3

#~ Sim
class Sim:
    '''
    '''
    nodes: dict

    def __init__(self) -> None:
        self.nodes= {}

        for i in range(NUM_NODES):
            self.nodes[f'192.168.1.{i}']= Node(self, f'192.168.1.{i}')


    # Funcs
    def tcp(
        self, selip: str, selport: str, tarip: str, tarport: str, msg: str
    ) -> bool:
        
        if (
            tarip != selip and
            tarip in self.nodes.keys() and 
            tarport in self.nodes[tarip].ports.keys() and
            self.nodes[tarip].ports[tarport].targetip in [None, selip] and 
            self.nodes[tarip].ports[tarport].targetport in [None, selport]
        ):
            self.nodes[tarip].ports[tarport].receive(msg)
            return True
        
        return False
    #~

    def visuals(self, screen: object) -> bool:

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

        deg= 2*math.pi/len(self.nodes)

        for k,d in self.nodes.items():
            for kp,dp in d.ports.items():
                if (dp.targetip==None):
                    pygame.draw.line(screen, 
                                    (255, 0, 0), 
                                    rotate((500, 500), (500, 800), deg*int(d.ip.split('.')[-1])),
                                    (500, 500),
                                    4
                    )
                else:
                    colour= (0, 0, 0)
                    if (dp.targetport in [LISTEN_PORT, INTIAL_PORT]): colour= (255, 0, 0)

                    pygame.draw.line(screen, 
                                    colour, 
                                    rotate((500, 500), (500, 800), deg*int(d.ip.split('.')[-1])),
                                    rotate((500, 500), (500, 800), deg*int(dp.targetip.split('.')[-1])),
                                    4
                    )

        for k,d in self.nodes.items():
            pygame.draw.circle(screen, 
                                (0, 0, 255), 
                                rotate((500, 500), 
                                (500, 800), 
                                deg*int(d.ip.split('.')[-1])), 
                                25
            )

        pygame.display.flip()
        return True


    def run(self, screen: object) -> None:
        
        while self.visuals(screen):
            for k,d in self.nodes.items():
                d.step()

                print(d)
                print()
            print('-----------------------------------------')
            input()




if __name__ == '__main__':
    pygame.init()
    screen= pygame.display.set_mode([1000,1000])
    # screen= 'tom'

    sim= Sim()
    sim.run(screen)

    pygame.quit()