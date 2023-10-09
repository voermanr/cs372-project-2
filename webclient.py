import socket
import sys

domain = ''
port = 80
request = 'GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n'

if len(sys.argv) > 1:
    domain = sys.argv[1]

if len(sys.argv) > 2:
    port = int(sys.argv[2])

destination = (domain, port)

socks = socket.socket()
socks.connect(destination)
socks.sendall(request.encode('ISO-8859-1'))

response = socks.recv(4096).decode()
while len(response) > 0:
    response = socks.recv(4096).decode()

socks.close()
