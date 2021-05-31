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
    

    def run(self):
        pass