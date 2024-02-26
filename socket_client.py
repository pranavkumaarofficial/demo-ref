# import socket


# def client_program():
#     host = socket.gethostname()  # as both code is running on same pc
#     port = 5000  # socket server port number

#     client_socket = socket.socket()  # instantiate
#     client_socket.connect((host, port))  # connect to the server

#     message = input(" -> ")  # take input

#     while message.lower().strip() != 'bye':
#         client_socket.send(message.encode())  # send message
#         data = client_socket.recv(1024).decode()  # receive response

#         print('Received from server: ' + data)  # show in terminal

#         message = input(" -> ")  # again take input

#     client_socket.close()  # close the connection


# if __name__ == '__main__':
#     client_program()





import socket

def client_program():
    # Ask the user to input the server's IP address
    server_ip = input("Enter the server's IP address: ")
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((server_ip, port))  # connect to the server using the provided IP

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
