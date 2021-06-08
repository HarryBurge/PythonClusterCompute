#~ Info
__authour__ = 'Harry Burge'
__created__ = '31/05/2021'
__doc__ = 'Holds the class for simulated nodes'

#~ Imports
import random
import time


#~ Node
class Node:

    def __init__(self, network, ip):
        self.network= network
        self.ip= ip
        # <sel port> : [<tar ip>, <tar port>, []]
        self.connections= {'20000' : [None, None, []]}


    def __str__(self):
        line= 'Node {}: ['.format(self.ip)

        for selport,(tarip, tarport, buffer) in self.connections.items():

            if tarip!=None and tarport!=None:
                line+= '{}-{}:{},'.format(selport, tarip, tarport)
            else:
                line+= 'Listening'

        return line+']'
    

    def run(self):

        self.connections['20001']= [None, None, []]
        
        while True:
            
            time.sleep(0.5)

            if self.network.connect_node_to_node(self.ip, '20001', '192.168.0.{}'.format(random.randint(0, 10)), '20000'):
                return True