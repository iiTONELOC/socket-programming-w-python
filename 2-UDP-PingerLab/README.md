# UDP Pinger

## Lab 2: UDP Pinger Lab

## Description

> In this lab, you will learn the basics of socket programming for UDP in Python. You will learn how to send and receive datagram packets using UDP sockets and also, how to set a proper socket timeout. Throughout the lab, you will gain familiarity with a Ping application and its usefulness in computing statistics such as packet loss rate.
> You will first study a simple Internet ping server written in Python, and implement a corresponding client. The functionality provided by these programs is similar to the functionality provided by standard ping programs available in modern operating systems. However, these programs use a simpler protocol, UDP, rather than the standard Internet Control Message Protocol (ICMP) to communicate with each other. The ping protocol allows a client machine to send a packet of data to a remote machine, and have the remote machine return the data back to the client unchanged (an action referred to as echoing). Among other uses, the ping protocol allows hosts to determine round-trip times to other machines.
> You are given the complete code for the Ping server below. Your task is to write the Ping client.(Kurose & Ross, 2023)

## Table of Contents

- [Provided Server Code](#provided-server-code)
- [Modified Server Code](#modified-server-code)
- [Packet Loss](#packet-loss)
- [Client Code Instructions](#client-code)
- [Proposed Solution Usage](#proposed-solution-usage)
- [Example Output](#proposed-solution-example-output)
- [Optional Exercises](#optional-exercises)

## Provided Server Code

> The following code fully implements a ping server. You need to compile and run this code before running your client program. You do not need to modify this code.
> In this server code, 30% of the client’s packets are simulated to be lost. You should study this code carefully, as it will help you write your ping client.
>
> ```py
> # UDPPingerServer.py
> # We will need the following module to generate randomized lost packets
> import random
> from socket import *
> # Create a UDP socket
> # Notice the use of SOCK_DGRAM for UDP packets
> serverSocket = socket(AF_INET, SOCK_DGRAM)
> # Assign IP address and port number to socket
> serverSocket.bind(('', 12000))
> while True:
>    # Generate random number in the range of 0 to 10
>    rand = random.randint(0, 10)
>    # Receive the client packet along with the address it is coming from
>    message, address = serverSocket.recvfrom(1024)
>    # Capitalize the message from the client
>    message = message.upper()
>    # If rand is less is than 4, we consider the packet lost and do not respond
>    if rand < 4:
>        continue
>
>    # Otherwise, the server responds
>    serverSocket.sendto(message, address)
> ```
>
> (Kurose & Ross, 2023)

### Modified Server Code

The starter code was modified to be modular; here, we create startServer and \_stopServer functions.

The startServer method is self-contained and will call \_stopServer automatically. This makes
usage much easier as the invoker only needs to know about the startServer function

```py
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
```

> The server sits in an infinite loop listening for incoming UDP packets. When a packet comes in and if a randomized integer is .greater than or equal to 4, the server simply capitalizes the encapsulated data and sends it back to the client.(Kurose & Ross, 2023)

## Packet Loss

> UDP provides applications with an unreliable transport service. Messages may get lost in the network due to router queue >overflows, faulty hardware or some other reasons. Because packet loss is rare or even non-existent in typical campus networks, >the server in this lab injects artificial loss to simulate the effects of network packet loss. The server creates a variable >randomized integer which determines whether a particular incoming packet is lost or not.(Kurose & Ross, 2023)

## Client Code

> You need to implement the following client program.
> The client should send 10 pings to the server. Because UDP is an unreliable protocol, a packet sent from the client to the server may be lost in the network, or vice versa. For this reason, the client cannot wait indefinitely for a reply to a ping message. You should get the client wait up to one second for a reply; if no reply is received within one second, your client program should assume that the packet was lost during transmission across the network. You will need to look up the Python documentation to find out how to set the timeout value on a datagram socket.
> Specifically, your client program should:
> (1) send the ping message using UDP (Note: Unlike TCP, you do not need to establish a connection first, since UDP is a connectionless protocol.)
> (2) print the response message from server, if any
> (3) calculate and print the round trip time (RTT), in seconds, of each packet, if server responses
> (4) otherwise, print “Request timed out”
> During development, you should run the UDPPingerServer.py on your machine, and test your client by sending packets to localhost (or, 127.0.0.1).
> After you have fully debugged your code, you should see how your application communicates across the network with the ping server and ping client running on different machines.(Kurose & Ross, 2023)

### Message Format

> The ping messages in this lab are formatted in a simple way. The client message is one line, consisting of ASCII characters in the following format:
> Ping sequence_number time
> where sequence_number starts at 1 and progresses to 10 for each successive ping message sent by the client, and time is the time when the client sends the message.(Kurose & Ross, 2023)

## Proposed Solution Usage

For right now the program does not accept any arguments and pings port 12001 on localHost.

The script is meant to be ran as a module

```bash
python 2-UDP\ PingerLab
```

So if you want to run the program from within the direction you need to run the `__main__.py` file

```bash
python __main__.py
```

### Proposed Solution Example Output

```bash
Pinging localhost:12001 10 times...

Request timed out
PING 2 RTT:0.0007460117340087891
PING 3 RTT:0.00045013427734375
PING 4 RTT:0.0004191398620605469
PING 5 RTT:0.0003707408905029297
PING 6 RTT:0.0003571510314941406
PING 7 RTT:0.00038623809814453125
PING 8 RTT:0.0003821849822998047
Request timed out
PING 10 RTT:0.000377655029296875

Closing client...
Stopping server...
```

## Optional Exercises

`Note: These are not yet implemented`

> 1.  Currently, the program calculates the round-trip time for each packet and prints it out individually. Modify this to correspond to the way the standard ping program works. You will need to report the minimum, maximum, and average RTTs at the end of all pings from the client. In addition, calculate the packet loss rate (in percentage).
> 2.  Another similar application to the UDP Ping would be the UDP Heartbeat. The Heartbeat can be used to check if an application is up and running and to report one-way packet loss. The client sends a sequence number and current timestamp in the UDP packet to the server, which is listening for the Heartbeat (i.e., the UDP packets) of the client. Upon receiving the packets, the server calculates the time difference and reports any lost packets. If the Heartbeat packets are missing for some specified period of time, we can assume that the client application has stopped. Implement the UDP Heartbeat (both client and server). You will need to modify the given UDPPingerServer.py, and your UDP ping client.(Kurose & Ross, 2023)

## References

Kurose, J., & Ross, K. (2023). Programming Assignments. Computer Network Research Group - UMass Amherst.
Retrieved September 8, 2023, from [https://gaia.cs.umass.edu/kurose_ross/programming.php](https://gaia.cs.umass.edu/kurose_ross/programming.php)

## LICENSE

This project is Licensed by the [MIT LICENSE](../LICENSE).

## Back to Main

[Click here to go back](../README.md)
