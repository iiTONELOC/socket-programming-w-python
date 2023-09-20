import sys
import time
from socket import socket, AF_INET, SOCK_DGRAM

from threader import ThreadManager
from server import startServer
from client import getRTT

NUM_PINGS = 10

ping_results = []
min_rtt = 0
max_rtt = 0
avg_rtt = 0
num_packets_lost = 0

def secondsToMilliseconds(seconds, roundTo=3):
    '''
        This function is responsible for converting seconds to milliseconds

        args:
            seconds: the number of seconds to convert to milliseconds

        return:
            the number of milliseconds
    '''
    return round(seconds * 1000, roundTo)

def calculateMinRTT():
    '''
        This function is responsible for calculating the minimum RTT
    '''
    global min_rtt, ping_results

    min_rtt = min(ping_results)
    return min_rtt

def calculateMaxRTT():
    '''
        This function is responsible for calculating the maximum RTT
    '''
    global max_rtt, ping_results

    max_rtt = max(ping_results)
    return max_rtt

def calculateAvgRTT():
    '''
        This function is responsible for calculating the average RTT
    '''
    global avg_rtt, ping_results

    avg_rtt = sum(ping_results) / len(ping_results)
    return avg_rtt

def calculatePacketLossRate():
    '''
        This function is responsible for calculating the packet loss rate
    '''
    global num_packets_lost, ping_results

    return (num_packets_lost / NUM_PINGS) * 100

def displayResults():
    try:
        ms = ' milliseconds'
        # print out the Minimum RTT, Maximum RTT, and Average RTT and Packet Loss Rate
        print('\nMinimum RTT: ' + str(secondsToMilliseconds(calculateMinRTT())) + ms)
        print('Maximum RTT: ' + str(secondsToMilliseconds(calculateMaxRTT())) + ms)
        print('Average RTT: ' + str(secondsToMilliseconds(calculateAvgRTT())) + ms)
        print('Packet Loss Rate: ' + str(calculatePacketLossRate()) + '%\n')
    except Exception as _:
        print('No results to display')

def pingServer(serverName:str|int, serverPort:int):
    '''
        This function is responsible for pinging the server 10 times

        Calculate the RTT for each ping, and storing the results into
        the ping_results list

        args:
            serverName: the name of the server
            serverPort: the port number of the server
    '''

    # create a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    # set the timeout to 1 second
    clientSocket.settimeout(1)

    print('Pinging ' + serverName + ':' + str(serverPort) + ' ' + str(NUM_PINGS) + ' times...\n')

    for i in range(1, NUM_PINGS+1):

        currentTime = time.time()

        #create a message 64 bytes in length
        messageToSend = bytes(64)

        # send the message to the server
        clientSocket.sendto(messageToSend, (serverName, serverPort))

        try:
            # receive the message from the server
            message,_ = clientSocket.recvfrom(1024)
            message = message.decode()

            # calculate the RTT
            RTT = getRTT(currentTime)
            global ping_results
            # store the RTT into the ping_results list
            ping_results.append(RTT)

            #  pint the number of bytes sent to what host and port and the RTT in milliseconds

            RTT_in_ms = secondsToMilliseconds(RTT)

            print(str(len(message)) + ' bytes from ' + serverName + ':' + str(serverPort) + ' RTT: ' + str(RTT_in_ms) + ' ms')

        except Exception as _:
            print('Request ' + str(i) +' timed out')
            global num_packets_lost
            num_packets_lost += 1

    # close the socket
    clientSocket.close()


def main():
    serverName = 'localhost'
    serverPort = 12000

    # create a thread manager for the server
    serverThreadName = 'UDP-Server'
    serverThreadManager = ThreadManager(target=startServer,args=(serverName,serverPort), name=serverThreadName)

    #create a thread manger for the client
    clientThreadName = 'UDP-Client'
    clientThreadManager = ThreadManager(target=pingServer,args=(serverName,serverPort), name=clientThreadName)

    # start the server
    serverThreadManager.start()

    # start the client
    clientThreadManager.start()

    # wait for the client to finish
    clientThreadManager.thread.join()

    # the server will have to be forced to stop
    serverThreadManager.stop(timeout=1)

    # display the results
    displayResults()


if __name__ == '__main__':
    main()
    sys.exit(0)
