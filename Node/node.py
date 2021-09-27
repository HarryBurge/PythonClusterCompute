#~ Imports
import socket
import select
import time

from Node import compute_manager, network_manager, reporting_manager

#~ Consts
OP_PORT= 2000

#~ Node
class Node:

    ip: str

    network_m: network_manager.NetworkManager
    compute_m: compute_manager.ComputeManager
    reporting_m: reporting_manager.ReportingManager
    interupts: list # 2D List, first axis being priority in desending order
    server_socket: socket.socket
    sockets: list

    def __init__(self, ip: str, dns: object) -> None:
        self.ip= ip

        self.network_m= network_manager.NetworkManager()
        self.compute_m= compute_manager.ComputeManager()
        self.reporting_m= reporting_manager.ReportingManager()
        self.interupts= [[]]*5

        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        act= (socket.gethostbyname(socket.gethostname()), dns.next_actual_port())
        self.server_socket.bind(act)
        self.server_socket.listen(5)
        dns.set_actual_address((ip, OP_PORT), act)

        self.sockets= []


    def connect_to_node(self, target: str, dns: object) -> bool:
        if (target==self.ip): return False

        # Only needed in simulation
        selport= dns.next_fake_port(self.ip)
        if (selport==None): return False

        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        act= (socket.gethostbyname(socket.gethostname()), dns.next_actual_port())
        s.bind(act)
        dns.set_actual_address((self.ip, selport), act)

        try:
            s.connect(dns.get_actual_address((target, OP_PORT)))
            self.sockets.append((s, (target, OP_PORT)))
        except socket.timeout:
            return False

        return True


    def step(self, dns: object) -> None:

        socks= [sock for sock,_ in self.sockets]+[self.server_socket]
        read_sockets, _, exception_sockets= select.select(socks, [], socks)
        act_server_address= dns.get_fake_address((self.ip, OP_PORT))

        for n in read_sockets:
            if (n==self.server_socket):

                cl_socket, cl_address= self.server_socket.accept()
                self.sockets.append((cl_socket, dns.get_fake_address(cl_address)))

                # cl_socket.sendall(b'HI')

                print(f'{(self.ip, OP_PORT)} accepted connection from {dns.get_fake_address(cl_address)}')

            else:
                # print(n.recv(4))
                pass


        






def run(nodes, ind, dns) -> None:

    self= nodes.get(ind)
    if (self.ip=='192.168.1.2'):
        time.sleep(1)
        self.connect_to_node('192.168.1.1', dns)
    nodes.set(ind, self)

    while True:
        self= nodes.get(ind)
        self.step(dns)
        nodes.set(ind, self)
        
