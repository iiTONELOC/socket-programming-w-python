import time
from socket import socket, AF_INET, SOCK_DGRAM


def getRTT(currentTime: float)->float:
    '''
        This function calculates the RTT of a message
        This is the Round Trip Time or the time it takes for a message to be sent
        and received back
        
        args:
            message: the message to calculate the RTT of
        
        returns: the RTT of the message
    '''
    return time.time() - currentTime


def pingServer(numberOfTimes:int, serverName:str, serverPort:int):
    '''
        This function pings a server a specified number of times
        For each ping, the RTT is calculated and printed
        
        If the packet was lost, then "Request timed out" is printed
        
        args:
            numberOfTimes: the number of times to ping the server
            serverName: the name of the server to ping
            serverPort: the port on the server to ping

        returns: None
    '''
    
    # create a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    # set timeout to 1 second
    clientSocket.settimeout(1)
    
    print('Pinging ' + serverName + ':' + str(serverPort) + ' ' + str(numberOfTimes) + ' times...\n')
    
    # ping numberOfTimes times
    for i in range(1, numberOfTimes + 1):
        # format the message
        message = 'Ping ' + str(i) + ' RTT'
        currentTime = time.time()
        
        # send the message
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        
        try:
            # receive the message
            modifiedMessage, _ = clientSocket.recvfrom(1024)
            modifiedMessage = modifiedMessage.decode()
            # calculate the RTT
            RTT = getRTT(currentTime)
            
            # print the response message and RTT
            print(modifiedMessage, RTT, sep=':')
            
        except Exception as e:
            print ("Request timed out")
    
    # close the socket
    print('\nClosing client...')
    clientSocket.close()
    exit(0)