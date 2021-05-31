#~ Info
__authour__ = 'Harry Burge'
__created__ = '31/05/2021'
__doc__ = 'Creates a simulation of a running cluster'

#~ Imports
from node import Node

import threading


#~ Sim
class Sim:
    
    nodes= {}

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


    def connect_node_to_node(self, ip1, port1, ip2, port2):
        # Check both ports are clear then connect them
        try:
            if self.nodes[ip1].connections[port1]==None and self.nodes[ip2].connections[port2]==None:
                self.nodes[ip1].connections[port1]= (ip2, port2, [])
                self.nodes[ip2].connections[port2]= (ip1, port2, [])
                return True

        # If either port doesn't exist
        except AttributeError:
            pass

        return False

        

        




if __name__=='__main__':
    sim= Sim()
    sim.run()