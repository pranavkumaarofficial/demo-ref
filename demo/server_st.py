import streamlit as st
import socket
import threading
from queue import Queue

# Global Queue for communication between server and Streamlit app
message_queue = Queue()
result_queue = Queue()

# Function to handle client connections
def handle_client(conn, address):
    print("Connection from: " + str(address))

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("from connected user " + str(address) + ": " + str(data))
            #st.code(f"Received: {str(data)}")
            #st.write("Got it ")
            result_queue.put(f"Received: {str(data)}")
            # Add the received data to the message queue for Streamlit
            #message_queue.put(f"Received from {str(address)}: {str(data)}")

            message_queue.put(f"Received from {str(address)}")

            # Optionally, add your logic here to process data (if needed)

            conn.close()
            print("Connection from " + str(address) + " closed.")
            # Add connection closed message to the message queue for Streamlit
            #message_queue.put(f"Connection from {str(address)} closed.")

    except Exception as e:
        print(f"Error handling client {address}: {e}")
        conn.close()


    
    # conn.close()
    # print("Connection from " + str(address) + " closed.")
    # # Add connection closed message to the message queue for Streamlit
    #message_queue.put(f"Connection from {str(address)} closed")

def server_program(host, port):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, address))
            client_handler.daemon = True  # Set the thread as daemon
            client_handler.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

def streamlit_frontend():
    st.title("Server Application")

    # Input for server host and port
    st.sidebar.title("Connection")
    host = st.sidebar.text_input("Enter Server Host:", "0.0.0.0")
    port = st.sidebar.text_input("Enter Server Port:", "5000")

    # Button to start the server
    if st.sidebar.button("Start Server"):
        st.write("Server started on {}:{}".format(host, port))

        # Start the server in a separate thread
        server_thread = threading.Thread(target=server_program, args=(host, int(port)), daemon=True)
        server_thread.start()

        # Display connections and outputs
        while True:
            if(not message_queue.empty()) and (not result_queue.empty()):
                message = message_queue.get()
                result = result_queue.get()
                st.sidebar.code(message)
                st.code(result)

if __name__ == '__main__':
    streamlit_frontend()
