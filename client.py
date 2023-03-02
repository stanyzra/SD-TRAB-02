import socket


def client():
    host = "localhost"
    port = 3000

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((host, port))
    sk.sendall("Hello, world".encode())
    data = sk.recv(1024)

    print(f"Received {data.decode()}")


if __name__ == "__main__":
    client()
