#~ Info
__authour__ = 'Harry Burge'
__created__ = '31/05/2021'
__doc__ = 'Creates a simulation of a running cluster'

#~ Imports
from node import Node

import threading
import pygame
import math


#~ Sim
class Sim:
    
    nodes= {}
    screen= pygame.display.set_mode((500, 500))
    clock= pygame.time.Clock()

    def __init__(self):
        # Init nodes
        for i in range(10):
            self.nodes['192.168.0.{}'.format(i)]= Node(self, '192.168.0.{}'.format(i))


    def run(self):
        # Run nodes in diffrent threads
        for k,d in self.nodes.items():
            t= threading.Thread(target=Node.run, args=(d,))
            t.setDaemon= True
            t.start()

        # Drawing
        diff_angle= 2*math.pi/len(self.nodes.keys())
        s_colour= (255, 255, 0)
        e_colour= (255, 255, 255)

        n_colour= (0, 0, 255)

        def rotate(angle):
            s = math.sin(angle)
            c = math.cos(angle)
            return (250 + 150*c - 0*s, 250 + 150*s + 0*c)

        while True:
            self.screen.fill((0,0,0))

            # Draw connections
            for k,d in self.nodes.items():
                for pk,pd in d.connections.items():

                    if pd!=None:
                        start= int(k.split('.')[-1])
                        end= int(pd[0].split('.')[-1])

                        if pk=='20000' or pk=='20001':
                            pygame.draw.line(self.screen, s_colour, rotate(start*diff_angle), rotate(end*diff_angle), 4)
                        else:
                            pygame.draw.line(self.screen, e_colour, rotate(start*diff_angle), rotate(end*diff_angle), 4)

            # Draw nodes
            for k,d in self.nodes.items():
                ind= int(k.split('.')[-1])
                pygame.draw.circle(self.screen, n_colour, rotate(ind*diff_angle), 20)

            pygame.display.update()
            self.clock.tick(60)

            print(self.nodes['192.168.0.0'])

 
    def connect_node_to_node(self, ip1, port1, ip2, port2):
        # Check both ports are clear then connect them
        try:
            if self.nodes[ip1].connections[port1]==None and self.nodes[ip2].connections[port2]==None:
                self.nodes[ip1].connections[port1]= (ip2, port2, [])
                self.nodes[ip2].connections[port2]= (ip1, port1, [])
                return True

        # If either port doesn't exist
        except AttributeError:
            pass

        return False

        

        




if __name__=='__main__':
    pygame.init()
    sim= Sim()
    sim.run()