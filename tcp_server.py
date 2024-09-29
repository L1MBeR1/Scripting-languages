import socket


def start_tcp_server(host, port, stop_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f'TCP сервер ожидает подключения по адресу {host}:{port}')

    while not stop_event.is_set():
        server.settimeout(1)
        try:
            client, client_addr = server.accept()
            print(f'Клиент подключен: {client_addr}')
            while not stop_event.is_set():
                data = client.recv(1024)
                if data:
                    print(
                        f'Получено сообщение от клиента: {data.decode("utf-8")}'
                    )
                    client.sendall(data)
                    print('Сообщение было отправлено')
                else:
                    break
            client.close()
        except socket.timeout:
            continue
        except Exception as e:
            print(f'Ошибка: {e}')
            break

    server.close()
    print("TCP сервер был остановлен.")
