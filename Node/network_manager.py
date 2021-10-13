#~ Imports
import socket
import select
import enum
import datetime


#~ Consts
OP_PORT= 2000
HEADER_LENGTH= 10
class MSG_TAG(enum.Enum):
    INFO= 1
    GEN= 2

#~ NetworkManager
class NetworkManager:

    ip: str

    server_socket: socket.socket
    _sockets: list
    _other_nodes_info: dict

    def __init__(self, ip: str, dns: object) -> None:
        self.ip= ip

        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        act= (socket.gethostbyname(socket.gethostname()), dns.next_actual_port())
        self.server_socket.bind(act)
        self.server_socket.listen(5)
        dns.set_actual_address((ip, OP_PORT), act)

        self._sockets= []
        self._other_nodes_info= {}

    #~ Utils
    def is_connected_to(self, target: str) -> bool:
        for _, (tarip, _) in self._sockets:
            if (tarip == target): 
                return True
        return False

    def encode_msg(self, msg_tag: MSG_TAG, msg: str):
        return f'{msg_tag.name}:{len(msg):<{HEADER_LENGTH-len(msg_tag.name)}}{msg}'

    #~ Methods
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
            tar_act_address= dns.get_actual_address((target, OP_PORT))
            if (tar_act_address==None):
                return False
            s.connect(tar_act_address)
            self._sockets.append((s, (target, OP_PORT)))
        except socket.timeout:
            return False

        return True

    def message_handler(self, dns: object) -> None:
        socks= [sock for sock,_ in self._sockets]+[self.server_socket]
        read_sockets, _, exception_sockets= select.select(socks, [], socks, 0.05)
        # act_server_address= dns.get_fake_address((self.ip, OP_PORT))

        for n in read_sockets:
            if (n==self.server_socket):

                cl_socket, cl_address= self.server_socket.accept()
                self._sockets.append((cl_socket, dns.get_fake_address(cl_address)))

                # cl_socket.sendall(b'HI')

                print(f'{(self.ip, OP_PORT)} accepted connection from {dns.get_fake_address(cl_address)}')

            else:
                # print(f'{self.ip} recived {n.recv(4)}')
                pass

    def _node_info_recv(self, adress: tuple, msg: str) -> None:
        pass


    #~ Run