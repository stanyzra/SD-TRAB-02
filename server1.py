import sys
import socket


def send_client_data(sk, protocolName):
    """
    Recebe os dados do cliente dependendo do protocolo
    """
    client_data = None
    client_addr = None
    if protocolName == "TCP":
        client_sk, client_addr = sk.accept()
        client_data = client_sk.recv(1024).decode()
        print(f"Received connection from {client_addr}")
        print(f"Data received: ")
        print(client_data)
        client_sk.send(f"{client_data} 1".encode())
    else:
        bytesAddressPair = sk.recvfrom(1024)
        client_data = bytesAddressPair[0]
        client_addr = bytesAddressPair[1]
        print(f"Received connection from {client_addr}")
        print(f"Data received: ")
        print(client_data)
        sk.sendto(f"{client_data} 1".encode(), client_addr)


def server():
    host = "localhost"
    port = 3001

    protocol = socket.SOCK_STREAM
    if len(sys.argv) < 2:
        print("Change the protocol using the command line argument 'udp' or 'tcp' (default is tcp)")
    else:
        userChoice = sys.argv[1]
        if userChoice.lower() == 'udp':
            protocol = socket.SOCK_DGRAM

    sk = socket.socket(socket.AF_INET, protocol)

    sk.bind((host, port))

    protocolName = "TCP" if protocol == socket.SOCK_STREAM else "UDP"
    print(
        f"Server 1 running and listening to {host}:{port} (protocol: {protocolName})")

    if protocolName == "TCP":
        sk.listen()
    while True:
        send_client_data(sk, protocolName)


if __name__ == "__main__":
    server()
