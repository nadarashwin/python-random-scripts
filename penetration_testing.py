#!/usr/local/bin/python2.7
import socket
import threading

bind = "0.0.0.0"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind, port))
server.listen(5)
print "[*] Listening on {}:{}".format(bind, port)

def handle_clients(client_socket):
    request = client_socket.recv(1024)
    print "[*] Received: %s" %request
    client_socket.send("ACK!")
    client_socket.close()


while True:
    client, address = server.accept()
    print "Client is connected with {}:{}".format(address[0], address[1])
    client_handler = threading.Thread(target=handle_clients,args=(client,))
    client_handler.start()

