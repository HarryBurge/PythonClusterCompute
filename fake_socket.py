import socket

class Socket:

    def __init__(self, simulation=None) -> None:
        self.simulation= simulation

        # Connection info
        self.selip= None
        self.selport= None

        self.tarip= None
        self.tarport= None

        self.buffer= ''

        # Listen info
        self.backlog_maxlen= None
        self.backlog= []
        self.listening= False

    def __str__(self) -> str:
        return f'{self.selip}:{self.selport}-{self.tarip}:{self.tarport}<>{self.buffer}'

    def bind(self, address) -> None:
        self.selip, self.selport= address

    def listen(self, backlog_maxlen):
        self.backlog_maxlen= backlog_maxlen if backlog_maxlen>0 else 0
        self.listening= True

    def accept(self):
        if (self.listening):
            while (len(self.backlog)==0):
                pass

            in_address= self.backlog.pop(0)

            temp= Socket(self.simulation)
            temp.tarip, temp.tarport= in_address

            return (temp, in_address)

        return None

    def connect(self, address): # TODO: Make timeout functionality
        self.tarip, self.tarport= address
        target= self.simulation.node_with_ip(self.tarip)

        # Target ip doesn't exist
        if (not target):
            return None

        try:
            tarsocket= target.sockets[self.tarport]
            if (
                tarsocket.listening and
                len(tarsocket.backlog)<tarsocket.backlog_maxlen 
            ):
                    tarsocket.backlog.append((self.selip, self.selport))
                    return

        # Target port doesn't exist
        except KeyError:
            pass

        raise socket.timeout()

    # def sim_sendall(self, ip, msg):
    #     if (ip==self.tarip):
    #         self.tarbuffer+= msg
    #         return None
    #     elif (ip==self.selip):
    #         self.selbuffer+= msg
    #         return None
    #     raise RuntimeError('IP specified is not set on either target or self')

    # def sim_recv(self, ip, buf_size):
    #     if (ip==self.tarip):
    #         temp= self.selbuffer[:buf_size]
    #         self.selbuffer[buf_size:]
    #         return temp
    #     elif (ip==self.selip):
    #         temp= self.tarbuffer[:buf_size]
    #         self.tarbuffer[buf_size:]
    #         return temp
    #     raise RuntimeError('IP specified is not set on either target or self')

