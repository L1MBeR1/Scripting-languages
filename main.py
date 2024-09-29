import threading
from tcp_server import start_tcp_server
from tcp_client import start_tcp_client
from udp_server import start_udp_server
from udp_client import start_udp_client


def main():
    host = "127.0.0.1"
    port = 60000
    stop_event = threading.Event()

    while True:
        print("\nВыберите опцию:")
        print("1. Запустить TCP сервер")
        print("2. Запустить UDP сервер")
        print("3. Запустить TCP клиент")
        print("4. Запустить UDP клиент")
        print("5. Выход")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            tcp_server_thread = threading.Thread(
                target=start_tcp_server, args=(host, port, stop_event)
            )
            tcp_server_thread.start()
        elif choice == "2":
            udp_server_thread = threading.Thread(
                target=start_udp_server, args=(host, port, stop_event)
            )
            udp_server_thread.start()
        elif choice == "3":
            message = input('Введите сообщение для TCP клиента: ')
            start_tcp_client(host, port, message)
        elif choice == "4":
            message = input('Введите сообщение для UDP клиента: ')
            start_udp_client(host, port, message)
        elif choice == "5":
            print("Выход...")
            stop_event.set()
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
