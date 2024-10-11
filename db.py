import sqlite3
import requests


def create_database():
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT
    )
    '''
    )

    connection.commit()
    connection.close()
    print("База данных и таблица 'posts' успешно созданы.")


def fetch_and_save_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    if response.status_code == 200:
        posts = response.json()
        print("Данные успешно получены с сервера.")

        connection = sqlite3.connect('posts.db')
        cursor = connection.cursor()

        for post in posts:
            cursor.execute(
                '''
            INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)
            ''',
                (post['id'], post['userId'], post['title'], post['body']),
            )

        connection.commit()
        connection.close()
        print(f"Сохранено {len(posts)} постов в базу данных.")
    else:
        print("Ошибка при получении данных:", response.status_code)


def get_posts_by_user(user_id):
    connection = sqlite3.connect('posts.db')
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM posts WHERE user_id = ?
        ''',
        (user_id,),
    )

    rows = cursor.fetchall()
    connection.close()

    if rows:
        print(f"\nПосты пользователя с user_id = {user_id}:")
        for post in rows:
            print("-" * 40)
            print(f"Post ID: {post[0]}")
            print(f"User ID: {post[1]}")
            print(f"Title: {post[2]}")
            print(f"Body: {post[3]}\n")
        print("-" * 40)
        print(f"\nВсе посты пользователя с user_id = {user_id} выведены.")
    else:
        print(f"\nПосты пользователя с user_id = {user_id} не найдены.")
