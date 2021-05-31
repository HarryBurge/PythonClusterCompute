#~ Info
__authour__ = 'Harry Burge'
__created__ = '31/05/2021'
__doc__ = 'Holds the class for simulated nodes'

#~ Imports


#~ Node
class Node:

    # sel port : (<tar ip>, <tar port>, [] or None
    connections= {}

    def __init__(self, network, ip):
        self.network= network
        self.ip= ip
        self.connections['20000']= None


    def __str__(self):
        line= 'Node {}: ['.format(self.ip)

        for k,d in self.connections.items():

            if d!=None:
                line+= '{}-{}:{},'.format(k, d[0], d[1])
            else:
                line+= 'Listening'

        return line+']'
    

    def run(self):

        self.connections['20001']= None
        
        # while True:
        for i in range(1):
            
            if self.network.connect_node_to_node(self.ip, '20001', '192.168.0.0', '20000'):
                return True