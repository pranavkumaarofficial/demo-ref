# import socket


# def server_program():
#     # get the hostname
#     host = socket.gethostname()
#     port = 5000  # initiate port no above 1024 #can modify this to find out what port the server is using 

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(2)
#     conn, address = server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print("from connected user: " + str(data))
#         data = input(' -> ')
#         conn.send(data.encode())  # send data to the client

#     conn.close()  # close the connection


# if __name__ == '__main__':
#     server_program()







# import socket
# import threading

# def handle_client(conn, address):
#     print("Connection from: " + str(address))
    
#     while True:
#         data = conn.recv(1024).decode()
#         if not data:
#             break
#         print("from connected user " + str(address) + ": " + str(data))
#         data = input(' -> ')
#         conn.send(data.encode())
    
#     print("Connection from " + str(address) + " closed.")
#     conn.close()

# def server_program():
#     host = '0.0.0.0'
#     port = 5000

#     server_socket = socket.socket()
#     server_socket.bind((host, port))
#     server_socket.listen(5)

#     print("Server listening on {}:{}".format(host, port))

#     try:
#         while True:
#             conn, address = server_socket.accept()
#             client_handler = threading.Thread(target=handle_client, args=(conn, address))
#             client_handler.start()

#     except KeyboardInterrupt:
#         print("Server shutting down...")
#         server_socket.close()

# if __name__ == '__main__':
#     server_program()





import socket
import threading

def handle_client(conn, address):
    print("Connection from: " + str(address))
    
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user " + str(address) + ": " + str(data))
        data = input(' -> ')
        conn.send(data.encode())
    
    print("Connection from " + str(address) + " closed.")
    conn.close()

def server_program():
    host = '0.0.0.0'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server listening on {}:{}".format(host, port))

    try:
        while True:
            conn, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, address))
            client_handler.daemon = True  # Set the thread as daemon
            client_handler.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == '__main__':
    server_program()
