#~ Imports
import socket
import select
import enum
import datetime


#~ Consts
SEND_INFO_PEROID= 100000
OP_PORT= 2000
HEADER_LENGTH= 10
class MSG_TAG(enum.Enum):
    INFO= 1

#~ Utils
def encode_msg(msg_tag: MSG_TAG, msg: str):
    return f'{msg_tag.name}:{len(msg):<{HEADER_LENGTH-len(msg_tag.name)-1}}{msg}'.encode('utf-8')

def recv_and_decode_msg(sock: socket.socket):
    message_header= sock.recv(HEADER_LENGTH).decode('utf-8')
    msg_type, msg_len= message_header.strip().split(':')

    msg_type= MSG_TAG[msg_type]
    msg_len= int(msg_len)

    msg= sock.recv(msg_len).decode('utf-8')

    return msg_type, msg


#~ NetworkManager
class NetworkManager:

    ip: str

    server_socket: socket.socket
    _sockets: list
    _other_nodes_info: dict
    _last_info_send: datetime.datetime

    def __init__(self, ip: str, dns: object) -> None:
        self.ip= ip

        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        act= (socket.gethostbyname(socket.gethostname()), dns.next_actual_port())
        self.server_socket.bind(act)
        self.server_socket.listen(5)
        dns.set_actual_address((ip, OP_PORT), act)

        self._sockets= []
        self._other_nodes_info= {}
        self._last_info_send= datetime.datetime.now()

    #~ Utils
    def is_connected_to(self, target: str) -> bool:
        for _, (tarip, _) in self._sockets:
            if (tarip == target): 
                return True
        return False

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


    def info_to_connected_nodes(self) -> None:
        if ((datetime.datetime.now()-self._last_info_send).microseconds > SEND_INFO_PEROID):
            self._last_info_send= datetime.datetime.now()
            for sock, _ in self._sockets:
                sock.sendall(encode_msg(MSG_TAG.INFO, '10'))


    def message_handler(self, dns: object) -> None:
        socks= [sock for sock,_ in self._sockets]+[self.server_socket]
        read_sockets, _, exception_sockets= select.select(socks, [], socks, 0.05)

        for n in read_sockets:
            if (n==self.server_socket):

                cl_socket, cl_address= self.server_socket.accept()
                self._sockets.append(
                    (cl_socket, dns.get_fake_address(cl_address))
                )

                print(f'{(self.ip, OP_PORT)} accepted connection from {dns.get_fake_address(cl_address)}')

            else:
                msg_type, msg= recv_and_decode_msg(n)

                if (msg_type==MSG_TAG.INFO):
                    self._info_recv(dns.get_fake_address(n.getpeername()), msg)
                else:
                    raise RuntimeError('Unspecifed message was recieved')

    #~~ Message Handler Sub Functions
    def _info_recv(self, address: tuple, msg: str) -> None:
        try:
            self._other_nodes_info[address][0]= float(msg)
            self._other_nodes_info[address][1]= datetime.datetime.now()
        except KeyError:
            self._other_nodes_info[address]= [
                float(msg), datetime.datetime.now(), datetime.datetime.now()
                ]
    #~~


    #~ Run