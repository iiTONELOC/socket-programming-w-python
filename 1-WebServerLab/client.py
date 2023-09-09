from socket import socket, AF_INET, SOCK_STREAM
import sys

if len(sys.argv) != 4:
    print("Required arguments: server_host server_port filename")
    sys.exit(1)

try:
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    #  create TCP socket for server
    client_socket = socket(AF_INET, SOCK_STREAM)

    # connect to server
    client_socket.connect((server_host, server_port))

    #  send HTTP request to server
    request = "GET /" + filename + " HTTP/1.1\r\n\r\n"

    client_socket.send(request.encode())

    #  receive HTTP response from server and display
    response = client_socket.recv(1024)

    print(response.decode())

    #  close connection
    client_socket.close()
    
except IOError:
    print("Error: file not found")
    sys.exit(1)
    
except Exception as e:
    print(e)
    sys.exit(1)

# exit the program
sys.exit(0)
