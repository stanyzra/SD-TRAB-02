import socket


def server():
    host = "localhost"
    port = 3002

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sk.bind((host, port))
    sk.listen()

    print(f"Server 2 running and listening to {host}:{port}")

    while True:

        client_sk, client_addr = sk.accept()
        print(f"Received connection from {client_addr}")

        client_data = client_sk.recv(1024).decode()
        print(f"Data received: ")
        print(client_data)

        client_sk.send(f"{client_data} 2".encode())


if __name__ == "__main__":
    server()
