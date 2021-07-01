#~ Imports
from cluster_node import Node

#~ Constants
NUM_NODES= 3

#~ Sim
class Sim:

    def __init__(self):

        self.nodes= {}

        for i in range(NUM_NODES):
            self.nodes[f'192.168.1.{i}']= Node(f'192.168.1.{i}')


    def tcp(self, tarip, tarport, msg):
        
        if (
            tarip in self.nodes.keys() and 
            tarport in self.nodes[tarip].ports.keys() and 
            self.nodes[tarip].ports[tarport].targetip != None and 
            self.nodes[tarip].ports[tarport].targetport != None
        ):
            self.nodes[tarip].ports[tarport].receive(msg)
        else:
            return False


    def run(self):
        
        while True:
            for k,d in self.nodes.items():
                d.step()




if __name__ == '__main__':
    sim= Sim()
    sim.run()