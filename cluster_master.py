#~ Imports
import socket

#~ Consts
HEADER_SIZE = 10
PORT = 20000
IP = '192.168.0.1'

#~ Initilisations
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((socket.gethostname(), PORT)) # Should be ip
s.listen()

worker_nodes = {}
interractors = {}


#~ New connection
def new_connection(clientsocket, address):
    try:
        message_header = clientsocket.recv(HEADER_SIZE)
        clienttype = message_header.decode('utf-8').strip()

        if clienttype == 'WORKER':
            worker_nodes[address] = clientsocket
        elif clienttype == 'INTERACTOR':
            interractors[address] = clientsocket
        else:
            print(f'Bad starting connection from {address}')
            msg = "Bad starting connection to server, please specify in header whether you are 'WORKER' or 'INTERACTOR'"
            clientsocket.send(bytes(f'{len(msg):<{HEADERSIZE}}'+msg, 'utf-8'))
            return False

        return True

    except:
        # Something went wrong
        return False



while True:
    clientsocket, address = s.accept()
    print('Test')
    print(new_connection(clientsocket, address))
    # clientsocket.send(bytes("Hey there!!!","utf-8"))