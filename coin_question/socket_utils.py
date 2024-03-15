import socket


def read_line(sock: socket.socket) -> bytes:
    """
    Read a line from the socket until we reach a newline
    """
    line = b""
    while True:
        part = sock.recv(1)
        if part == b"":
            break
        elif part != b"\n":
            line += part
        elif part == b"\n":
            break
    return line
