#~ Imports

#~ Constants

#~ Port
class Port:

    def __init__(self, portnum):
        
        self.portnum= portnum
        self.targetip= None
        self.targetport= None
        self.buffer= []

    
    def read(self):
        pass


    def send(self, msg):
        pass