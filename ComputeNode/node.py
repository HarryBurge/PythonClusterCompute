#~ Imports
import socket
import multiprocessing

from ComputeNode import compute_manager, network_manager, reporting_manager
import fake_socket
import util

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

    def __init__(self, ip: str) -> None:
        self.ip= ip

        self.network_m= network_manager.NetworkManager()
        self.compute_m= compute_manager.ComputeManager()
        self.reporting_m= reporting_manager.ReportingManager()
        self.interupts= [[]]*5
        self.sockets= {OP_PORT : fake_socket.Socket()}
        self.sockets[OP_PORT].bind((ip, OP_PORT))
        self.sockets[OP_PORT].listen(5)


def connect_to_node(nodes, ind, target) -> bool:
    self= nodes.get(ind)

    # if (target==self.ip): return False

    # # Only needed in simulation
    # selport= None
    # for port in range(PORT_MIN, PORT_MAX+1):
    #     if (port not in self.sockets.keys()):
    #         selport= port
    #         break
    # else:
    #     return False

    # s= fake_socket.Socket()
    # s.bind((self.ip, selport))

    # try:
    #     s.connect((target, OP_PORT))
    #     self.sockets[selport]= s
    # except socket.timeout:
    #     return False

    return True


def step(nodes, ind) -> None:
    self= nodes.get(ind)

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

    self.ip= "176.112.12.12"

    target= nodes.get(1 if ind==0 else 0)
    target.ip= '8.8.8.8'
    nodes.set(1 if ind==0 else 0, target)
    nodes.set(ind, self)

    # TODO: Think about mutual exclusion jobs


def run(nodes, ind) -> None:
    while True:
        # nodes.get(ind).step(nodes)
        step(nodes, ind)

        
