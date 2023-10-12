import socket
import sys
import re

port = 28333
response = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!\r\n'

if len(sys.argv) > 1:
    port = int(sys.argv[1])

socks = socket.socket()
socks.bind(('', port))
socks.listen()

while True:
    incoming = socks.accept()
    connected_sock = incoming[0]
    print(str(incoming[1][0]) + ":" + str(incoming[1][1]) + " connected...")

    request = connected_sock.recv(4096).decode()
    while not re.search(r'\r\n\r\n', request):
        request = connected_sock.recv(4096).decode()

    connected_sock.sendall(response)
    connected_sock.close()
