#~ Imports

#~ Constants

#~ Port
class Port:
    '''
    Simulates a port which can send a recieve messages via tcp connections
    - Messages:
        - Has buffer of equal to constant in cluster node
        - Type, 3 letter which represent type of packet:
            - GEN, general message
            - INT, intialisation messages
            - NWP, new port and switch (Usually as part of intialisation)
        - Message body
    '''
    portnum: str
    network: object
    targetip: str
    targetport: str
    buffer: list

    def __init__(self, portnum: str, network: object) -> None:
        self.portnum= portnum
        self.network= network

        self.targetip= None
        self.targetport= None
        self.buffer= []


    def __str__(self) -> str:
        return (
            f'{self.portnum}:{self.targetip}-{self.targetport}-->'
            f'{[x.strip() for x in self.buffer]}'
            )

    
    # Func
    def is_empty(self) -> bool:
        if (len(self.buffer) == 0): return True
        return False


    def read(self) -> str:
        if (not self.is_empty()):
            return self.buffer[0]
        
        raise IndexError('Nothing to read in buffer')


    def pop(self) -> str:
        if (not self.is_empty()):
            return self.buffer.pop(0)
        
        raise IndexError('Nothing to pop in buffer')


    def send(self, msg: str) -> bool:
        if (self.network.tcp(self.targetip, self.targetport, msg) != False):
            return True
        return False


    def receive(self, msg: str) -> None:
        self.buffer.append(msg)
    #~