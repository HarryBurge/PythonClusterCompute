import socket
import select
import util

# IP = "127.0.0.1"
IP = socket.gethostname()
PORT = 1234


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen()

    # List of sockets for select.select()
    sockets_list = [server_socket]

    workers = {}
    interactors = {}

    print(f'Listening for connections on {IP}:{PORT}...')

    while True:

        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        # Iterate over notified sockets
        for notified_socket in read_sockets:

            # If notified socket is a server socket - new connection, accept it
            if notified_socket == server_socket:

                # Accept new connection
                node_socket, node_address = server_socket.accept()

                # Should send type of node
                node_info = util.receive_message(node_socket)

                # If False - node disconnected before sent type
                if node_info is False:
                    continue

                sockets_list.append(node_socket)

                if node_info['data'] == '{WORKER}':
                    workers[node_socket] = None

                elif node_info['data'] == '\{INTERACTOR\}':
                    interactors[node_socket] = None

                print('New {} connected from {}:{}'.format(node_info['data'], *node_address))
                node_socket.send(util.format_message('Connection accepted as {}'.format(node_info['data'])))

            # Else existing socket is sending a message
            else:
                pass

                # # Receive message
                # message = receive_message(notified_socket)

                # # If False, client disconnected, cleanup
                # if message is False:
                #     print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                #     # Remove from list for socket.socket()
                #     sockets_list.remove(notified_socket)

                #     # Remove from our list of users
                #     del clients[notified_socket]

                #     continue

                # # Get user by notified socket, so we will know who sent the message
                # user = clients[notified_socket]

                # print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                # # Iterate over connected clients and broadcast message
                # for client_socket in clients:

                #     # But don't sent it to sender
                #     if client_socket != notified_socket:

                #         # Send user and message (both with their headers)
                #         # We are reusing here message header sent by sender, and saved username header send by user when he connected
                #         client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        # Socket exceptions catch
        for notified_socket in exception_sockets:

            # Remove from list for socket.socket()
            sockets_list.remove(notified_socket)

            if notified_socket in workers.keys():
                del workers[notified_socket]

            if notified_socket in interactors.keys():
                del interactors[notified_socket]


if __name__ == '__main__':
    main()