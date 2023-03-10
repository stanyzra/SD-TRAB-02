import sys
import socket


def server():
    host = "localhost"
    port = 3002

    protocol = socket.SOCK_STREAM
    if len(sys.argv) < 2:
        print("Change the protocol using the command line argument 'udp' or 'tcp' (default is tcp)")
    else:
        userChoice = sys.argv[1]
        if userChoice.lower() == 'udp':
            protocol = socket.SOCK_DGRAM

    sk = socket.socket(socket.AF_INET, protocol)

    sk.bind((host, port))
    sk.listen()

    protocolName = "TCP" if protocol == socket.SOCK_STREAM else "UDP"
    print(
        f"Server 2 running and listening to {host}:{port} (protocol: {protocolName})")

    while True:

        client_sk, client_addr = sk.accept()
        print(f"Received connection from {client_addr}")

        client_data = client_sk.recv(1024).decode()
        print(f"Data received: ")
        print(client_data)

        client_sk.send(f"{client_data} 2".encode())


if __name__ == "__main__":
    server()
