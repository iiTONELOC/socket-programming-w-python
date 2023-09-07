import random
from socket import socket, AF_INET, SOCK_DGRAM

def _stopServer(socket:socket)->None:
    '''
        This function stops the server
        
        args:
            socket: the socket to close
        
        returns: None
    '''
    
    try:
        # close the socket
        socket.close()
        print('\nClosing server...')
        exit(0)
    except Exception as e:
        print('Error closing socket: ', e)
        exit(1)


def startServer(host:str, port:int)->None:
    '''
        start a UDP server that listens on the specified port
        and sends the result to the client
        
        args:
            host: the host to listen on
            port: the port to listen on
        
        returns: None
    '''
    
    try:
        # create a UDP socket
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        
        # bind the socket to the host and port
        serverSocket.bind((host, port))
        
        # listen for incoming messages
        while True:
            # generate a random number between 0 and 10
            rand = random.randint(0, 10)
            
            # receive the message and address
            message, address = serverSocket.recvfrom(1024)
            
            # capitalize the message
            message = message.upper()
            
            # if rand is less than 4, then the packet was lost
            if rand < 4:
                continue
            
            # otherwise, send the message back to the client
            serverSocket.sendto(message, address)

    except KeyboardInterrupt:
        # close the socket
        _stopServer(serverSocket)
        
    except Exception as e:
        print('Error starting server: ', e)
        
        # check if the socket was created
        if 'serverSocket' in locals():
            # close the socket
            _stopServer(serverSocket)
        
    exit(1)