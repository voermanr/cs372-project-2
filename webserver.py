import os.path
import socket
import sys
import re


def parse_file_name(r: str):
    split_request = r.split("\r\n")
    split_request = split_request[0].split(' ')
    file_path = os.path.split(split_request[1])
    return file_path[1]


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

    request_buff = ''
    while True:
        request = connected_sock.recv(4096).decode()
        request_buff += request
        if re.search(r'\r\n\r\n', request):
            break

    file_name = parse_file_name(request_buff)

    print("file name: " + file_name)

    connected_sock.sendall(response)
    connected_sock.close()
