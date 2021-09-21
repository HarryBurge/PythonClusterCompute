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

    _simulation: object # Simulation object
    _push_changes: list # List of simulation commands that need to be execed

    network_m: network_manager.NetworkManager
    compute_m: compute_manager.ComputeManager
    reporting_m: reporting_manager.ReportingManager
    interupts: list # 2D List, first axis being priority in desending order
    sockets: dict # {<Port> : Socket object}

    def __init__(self, ip: str, simulation: object=None) -> None:
        self.ip= ip

        self._simulation= simulation
        self._push_changes= []

        self.network_m= network_manager.NetworkManager()
        self.compute_m= compute_manager.ComputeManager()
        self.reporting_m= reporting_manager.ReportingManager()
        self.interupts= [[]]*5
        self.sockets= {OP_PORT : fake_socket.Socket(simulation)}
        self.sockets[OP_PORT].bind((ip, OP_PORT))
        self.sockets[OP_PORT].listen(5)


    def connect_to_node(self, target) -> bool:
        if (target==self.ip): return False

        # Only needed in simulation
        selport= None
        for port in range(PORT_MIN, PORT_MAX+1):
            if (port not in self.sockets.keys()):
                selport= port
                break
        else:
            return False

        s= fake_socket.Socket(self._simulation)
        s.bind((self.ip, selport))

        try:
            s.connect((target, 2000))
            self.sockets[selport]= s
        except socket.timeout:
            return False

        return True


    def step(self) -> None:
        conn, address= self.sockets[2000].accept()
        
        # Only needed in simulation
        selport= None
        for port in range(PORT_MIN, PORT_MAX+1):
            if (port not in self.sockets.keys()):
                selport= port
                break
        else:
            return False

        # Only needed in simulation
        conn.bind((self.ip, selport))
        self._push_changes.append(f'self.node_with_ip("{address[0]}").sockets[{address[1]}].tarport= {selport}')

        self.sockets[selport]= conn

        return self

        
