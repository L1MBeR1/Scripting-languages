from db import create_database, fetch_and_save_posts, get_posts_by_user


def main():
    while True:
        print("\nВыберите действие:")
        print("1. Создать базу данных")
        print("2. Получить данные с сервера и сохранить в базу данных")
        print("3. Чтение данных из базы по user_id")
        print("4. Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            create_database()
        elif choice == '2':
            fetch_and_save_posts()
        elif choice == '3':
            user_id = input("Введите user_id для получения постов: ")
            get_posts_by_user(user_id)
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
