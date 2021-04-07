#~ Imports
import socket

#~ Consts
HEADER_SIZE = 10
PORT = 20000
IP = '192.168.0.1'

#~ Initilisations
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT)) # Should be ip

yn = True
while yn:
    try:
        msg = s.recv(8)
        print(msg.decode("utf-8"))
    except KeyboardInterrupt:
        yn = False


s.send(bytes(f'WORKER:<{HEADERSIZE}', 'utf-8'))

while True:
    msg = s.recv(HEADER_SIZE)
    message_length = int(message_header.decode('utf-8').strip())
    print(msg.recv(message_length))