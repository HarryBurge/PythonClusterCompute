#~ Imports

#~ Constants

#~ Port
class Port:

    def __init__(self, portnum, network):
        
        self.portnum= portnum
        self.network= network

        self.targetip= None
        self.targetport= None
        self.buffer= []

    
    def read(self):
        if (len(self.buffer) != 0):
            return self.buffer.pop(0)
        return False


    def send(self, msg):
        if (self.network.tcp(self.targetip, self.targetport, msg) != False):
            return True
        return False


    def receive(self, msg):
        self.buffer.append(msg)