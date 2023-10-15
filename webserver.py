import os.path
import socket
import sys
import re


port = 28333


def parse_file_name(r: str):
    split_request = r.split("\r\n")
    split_request = split_request[0].split(' ')
    file_path = os.path.split(split_request[1])
    return file_path[1]


if len(sys.argv) > 1:
    port = int(sys.argv[1])


def parse_mime_type(f: str):
    mime_types = {'.txt': b'text/plain', '.html': b'text/html', '.ico': b'image/x-icon', '': b'application/octet-stream'}
    return mime_types[os.path.splitext(f)[1]]


def read_file(fn: str):
    try:
        with open(fn) as fp:
            data = fp.read()  # Read entire file
            return data

    except:
        return False


socks = socket.socket()
socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socks.bind(('', port))
socks.listen()

while True:
    incoming = socks.accept()
    connected_sock = incoming[0]

    # print(str(incoming[1][0]) + ":" + str(incoming[1][1]) + " connected...")

    response = b''
    request_buff = ''
    while True:
        request = connected_sock.recv(4096).decode()
        request_buff += request
        if re.search(r'\r\n\r\n', request):
            break

    file_name = parse_file_name(request_buff)

    mime_type = parse_mime_type(file_name)

    # print("file name: " + file_name + ', mime type: ' + str(mime_type.decode()))

    payload = read_file(file_name)

    if payload:
        response = b'HTTP/1.1 200 OK\r\n'

        # content type
        response += b'Content-Type: ' + mime_type + b'\r\n'

        # content length
        response += b'Content-Length: ' + str(len(payload)).encode() + b'\r\n'

        # connection close
        response += b'Connection: close\r\n\r\n'

        # payload
        response += payload.encode() + b'\r\n'

    if not payload:
        response = b"HTTP/1.1 404 Not Found\r\n" \
                   b"Content-Type: text/plain\r\n" \
                   b"Content-Length: 13\r\n" \
                   b"Connection: close\r\n" \
                   b"\r\n" \
                   b"404 not found"

    connected_sock.sendall(response)
    connected_sock.close()
