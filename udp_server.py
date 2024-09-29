import socket


def start_udp_server(host, port, stop_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print(f"UDP сервер ожидает подключения по адресу {host}:{port}")

    while not stop_event.is_set():
        server.settimeout(1)
        try:
            data, addr = server.recvfrom(1024)
            print(f"Получено сообщение от клиента: {data.decode('utf-8')}")
            server.sendto(data, addr)
            print('Сообщение было отправлено')
        except socket.timeout:
            continue
        except Exception as e:
            print(f'Ошибка: {e}')
            break

    server.close()
    print("UDP сервер был остановлен.")
