#~ Info
__authour__ = 'Harry Burge'
__created__ = '31/05/2021'
__doc__ = 'Holds the class for simulated nodes'

#~ Imports


#~ Node
class Node:

    # [<sel port>, <tar ip>, <tar port>, []]
    connections= []

    def __init__(self, network, ip):
        self.network= network
        self.ip= ip
        self.connections.append(['20000', None, None, []])


    def __str__(self):
        line= 'Node {}: ['.format(self.ip)

        for selport, tarip, tarport in self.connections:

            if tarip!=None and tarport!=None:
                line+= '{}-{}:{},'.format(selport, tarip, tarport)
            else:
                line+= 'Listening'

        return line+']'
    

    def run(self):

        self.connections.append(['20001', None, None, []])
        
        # while True:
        for i in range(3):
            
            if self.network.connect_node_to_node(self.ip, '20001', '192.168.0.0', '20000'):
                return True