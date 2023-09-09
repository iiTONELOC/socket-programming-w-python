from threader import ThreadManager
from server import startServer
from client import pingServer

def main()->None:
    '''
        This is the main entry point of the program
        
        The main function is responsible for starting the server and client
        programs
        
        The server listens on a provided port for incoming messages at a 
        specified host
        
        The client pings the server a specified number of times and prints
        the RTT of each message
        
        args: None
        
        returns: None
    '''
    
    #  TODO: add command line arguments to read the host, port, and number of
    # times to ping
    udpServerHost = 'localhost'
    udpServerPort = 12001
    numTimesToPing = 10

    serverThreadName = 'UDPServerThread-'+udpServerHost+':'+str(udpServerPort)
    clientThreadName = 'UDPClientThread-'+udpServerHost+':'+str(udpServerPort)

    
    # start the server using the thread manager
    serverThreadManager = ThreadManager(target=startServer,
                                            args=(udpServerHost,
                                                udpServerPort)
                                            , name=serverThreadName)
        
    serverThreadManager.start()
        
    
    # start the client using the thread manager
    clientThreadManager = ThreadManager(target=pingServer,
                                            args=(numTimesToPing,
                                                udpServerHost,
                                                udpServerPort)
                                            , name=clientThreadName)
        
    clientThreadManager.start()
    # wait for the client to finish
    clientThreadManager.thread.join()
    
    # stop the server, the client closes automatically
    # the server runs on a loop so it needs to be stopped 
    # manually, We wait 1.5 seconds for a graceful shutdown then we stop it
    # forcefully
    print('Stopping server...')
    serverThreadManager.stop(timeout=1.5)

if __name__ == '__main__':
    main()
    