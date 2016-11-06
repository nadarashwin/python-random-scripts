#!/usr/local/bin/python2.7
import socket
import sys

def socket_create():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print msg + " socket error"

def socket_bind():
    try:
        global host
        global port
        global s
        print "binding socket to port:" + str(port)
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print msg + " socket bind"

def socket_accept():
    conn, address = s.accept()
    print "address" + str(address)
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:
        cmd = raw_input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024))
            print client_response

def main():
    socket_create()
    socket_bind()
    socket_accept()

main()









