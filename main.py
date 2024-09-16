from api import get_user_posts, create_post, update_post


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Выполнить GET-запрос для вывода постов с чётным userId")
        print("2. Выполнить POST-запрос для создания поста")
        print("3. Выполнить PUT-запрос для обновления поста")
        print("4. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            get_user_posts()
        elif choice == '2':
            create_post()
        elif choice == '3':
            update_post()
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
