#~ Imports
import socket
import multiprocessing

from ComputeNode import compute_manager, network_manager, reporting_manager

#~ Consts
OP_PORT= 2000
PORT_MIN= 2001
PORT_MAX= 2005

#~ Node
class Node:

    ip: str

    network_m: network_manager.NetworkManager
    compute_m: compute_manager.ComputeManager
    reporting_m: reporting_manager.ReportingManager
    interupts: list # 2D List, first axis being priority in desending order
    sockets: dict # {<Port> : Socket object}

    def __init__(self, ip: str, dns: object) -> None:
        self.ip= ip

        self.network_m= network_manager.NetworkManager()
        self.compute_m= compute_manager.ComputeManager()
        self.reporting_m= reporting_manager.ReportingManager()
        self.interupts= [[]]*5
        self.sockets= {OP_PORT : (socket.socket(socket.AF_INET, socket.SOCK_STREAM), (None, None))}
        act= (socket.gethostbyname(socket.gethostname()), dns.next_actual_port())
        self.sockets[OP_PORT][0].bind(act)
        dns.set_actual_address((ip, OP_PORT), act)
        self.sockets[OP_PORT][0].listen(5)


    def connect_to_node(self, target, dns) -> bool:
        if (target==self.ip): return False

        # Only needed in simulation
        selport= None
        for port in range(PORT_MIN, PORT_MAX+1):
            if (port not in self.sockets.keys()):
                selport= port
                break
        else:
            return False

        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        act= (socket.gethostbyname(socket.gethostname()), dns.next_actual_port())
        s.bind(act)
        dns.set_actual_address((self.ip, selport), act)

        try:
            s.connect(dns.get_actual_address((target, OP_PORT)))
        except socket.timeout:
            return False

        self.sockets[selport]= (s, (target, OP_PORT))
        return True


    def step(self) -> None:
        pass
        # print(self.sockets[OP_PORT].getsockname())
        # print(socket.gethostbyname(socket.gethostname()))

    # conn,_= self.sockets[2000].accept()
    
    # # Only needed in simulation
    # selport= None
    # for port in range(PORT_MIN, PORT_MAX+1):
    #     if (port not in self.sockets.keys()):
    #         selport= port
    #         break
    # else:
    #     return False

    # # Only needed in simulation
    # conn.bind((self.ip, selport))

    # self.sockets[selport]= conn

    # TODO: Think about mutual exclusion jobs


def run(nodes, ind, dns) -> None:

    self= nodes.get(ind)
    print(self.connect_to_node('192.168.1.1', dns))
    nodes.set(ind, self)

    while True:
        self= nodes.get(ind)
        self.step()

        nodes.set(ind, self)

        
