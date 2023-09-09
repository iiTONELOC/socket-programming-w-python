from socket import socket, AF_INET, SOCK_STREAM
import sys 

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverPort = 3000
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)


#Establish the connection
print('Ready to serve...')
while True:
    connectionSocket, addr = serverSocket.accept()
    
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outPutData = f.read()
        
        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
        #Send the HTTP file
        connectionSocket.send(outPutData.encode())
        connectionSocket.send('\r\n'.encode())
        #Close client socket
        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send('<html><head></head><body><h1>\
                404 Not Found</h1></body></html>\r\n'.encode())
            
        connectionSocket.close()


    print('\nServer shutting down...')
    serverSocket.close()
    sys.exit()