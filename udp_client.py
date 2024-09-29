import socket


def start_udp_client(host, port, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(message.encode('utf-8'), (host, port))
    print(f'Сообщение было отправлено на {host}:{port}')

    data, _ = client.recvfrom(1024)
    print(f"Получено сообщение от сервера: {data.decode('utf-8')}")

    client.close()
