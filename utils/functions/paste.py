import socket


def _netcat(host: str, port: int, content: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("UTF-8").strip("\n\x00")
        if not data:
            break
        return data, f"{data}/preview.png"
    s.close()


def paste(content: str):
    link, preview = _netcat("ezup.dev", 9999, content)
    return link, preview
