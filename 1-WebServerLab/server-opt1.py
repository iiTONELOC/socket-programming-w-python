from socket import socket, AF_INET, SOCK_STREAM
import threading
import sys

# Function to handle client requests
def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        with open(filename[1:], 'rb') as f:
            outPutData = f.read()

        # Send HTTP headers
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

        # Send the content of the requested file to the client
        connectionSocket.sendall(outPutData)
        connectionSocket.close()
    except IOError:
        # Send '404 Not Found' response
        not_found_response = 'HTTP/1.1 404 Not Found\r\n\r\n<html><head>\
            </head><body><h1>404 Not Found</h1></body></html>\r\n'
        connectionSocket.send(not_found_response.encode())
        connectionSocket.close()


try:
    # Create a server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverPort = 3000
    serverSocket.bind(('localhost', serverPort))
    # Listen for incoming connections
    # This sets the maximum number of clients that can be waiting to connect to 5,
    # after which point the OS will stop queuing up new connections.
    serverSocket.listen(5)

    print('Server is ready to receive requests...')
    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()
        print(f'Connection from {addr[0]}:{addr[1]}')

        # Create a thread to handle the client request
        client_thread = threading.Thread(target=handle_client, args=(
            connectionSocket,))
        client_thread.start()

except KeyboardInterrupt:
    print('\nServer shutting down...')
    serverSocket.close()
    sys.exit()
    
except OSError:
    if serverSocket:
        serverSocket.close()
    
    print('Socket already in use. Or the server is already running. Try again later.')
    sys.exit()

except Exception as e:
    print(e)
    sys.exit()