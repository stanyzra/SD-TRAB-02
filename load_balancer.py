# -*- coding: utf-8 -*-

import socket


def get_servers_index_by_type(servers):
    """Retorna uma lista com os índices dos servidores TCP e UDP"""
    tcp_servers_index = []
    udp_servers_index = []
    for i, server in enumerate(servers):
        host, port = server
        # args = socket.getaddrinfo(
        #     host, port, socket.AF_INET, socket.SOCK_STREAM)
        # for family, sktype, proto, canonname, sockaddr in args:
        sk_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sk_tcp.connect((host, port))
        except socket.error as e:
            try:
                sk_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sk_udp.sendto("Connection test".encode(), (host, port))
                data, address = sk_udp.recvfrom(1024)
            except socket.error:
                print(f"Server {i} ({host}:{port}) is not available")
            else:
                print(f"Server {i} ({host}:{port}) is available")
                udp_servers_index.append(servers.index(server))
            finally:
                sk_udp.close()
        else:
            tcp_servers_index.append(servers.index(server))
        finally:
            sk_tcp.close()
    return tcp_servers_index, udp_servers_index


def check_client_protocol(client_sk):
    if client_sk.type == socket.SOCK_STREAM:
        return "TCP"
    else:
        return "UDP"


def next_server(servers, actual_server_index):
    """Retorna o índice do próximo servidor"""
    return (actual_server_index + 1) % len(servers)


def is_server_available(server):
    """Verifica se o servidor passado por parâmetro está disponível"""
    host, port = server
    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for family, sktype, proto, canonname, sockaddr in args:
        sk = socket.socket(family, sktype, proto)
        try:
            print(f"Testing connection with {host}:{port}")
            sk.connect((host, port))
        except:
            print(f'## Couldn\'t connect to {host}:{port} ##\n')
            return False
        else:
            print(f"Connected with {host}:{port}")
            sk.close()
            return True


def check_servers(servers, actual_server_index):
    """Verifica a disponibilidade do servidor atual. Se sim, retorna seu index,
    se não, procura pelos próximos servidores e retorna o index do primeiro
    disponível encontrado.
    """
    if (not is_server_available(servers[actual_server_index])):
        has_one_server_disponible = False
        while has_one_server_disponible != True:
            actual_server_index = next_server(servers, actual_server_index)
            has_one_server_disponible = is_server_available(
                servers[actual_server_index])
    return actual_server_index


def start_lb(host, port, servers, actual_server_index):
    sk_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sk_tcp.bind((host, port))
    sk_tcp.listen()
    sk_udp.bind((host, port))

    tcp_servers_index, udp_servers_index = get_servers_index_by_type(
        servers)

    print(tcp_servers_index)
    print(udp_servers_index)
    print(f"Starting load balancer and listening on {host}:{port}")

    while True:
        client_sk, client_addr = sk_tcp.accept()
        print(f"Connection established with {client_addr}")
        # get_servers_index_by_type(servers)
        if check_client_protocol(client_sk) == "UDP":
            print("UDP client detected, forwarding data to server 1")
            serverAddr, serverPort = servers[0]
        else:
            print(
                "TCP client detected, iniciating load balancing with Round Robin algorithm")
            actual_server_index = check_servers(servers, actual_server_index)

            serverAddr, serverPort = servers[actual_server_index]

            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((serverAddr, serverPort))

            actual_server_index = next_server(servers, actual_server_index)
            actual_server_index = check_servers(servers, actual_server_index)
            serverAddr, serverPort = servers[actual_server_index]

        print(f"Forwarding connection to {serverAddr}:{serverPort}\n")
        server_sock.sendall(client_sk.recv(1024))
        client_sk.sendall(server_sock.recv(1024))

        client_sk.close()
        server_sock.close()


if __name__ == "__main__":
    host = "localhost"
    port = 3000

    servers = []
    for i in range(1, 4):
        servers.append((host, port + i))

    start_lb(host, port, servers, 0)
