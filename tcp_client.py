import socket


def start_tcp_client(host, port, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))
    print(f'Клиент подключён к {host}:{port}')

    client.sendall(message.encode('utf-8'))

    data = client.recv(1024)
    print(f"Получено сообщение от сервера: {data.decode('utf-8')}")

    client.close()
