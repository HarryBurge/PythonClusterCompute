import socket

HEADER_LENGTH = 10


def receive_message(node_socket):

    try:
        message_header = node_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': node_socket.recv(message_length).decode('utf-8')}

    except:
        return False

def format_message(message):
    message_temp = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    return message_header + message_temp