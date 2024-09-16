import requests


def get_user_posts():
    response = requests.get('https://jsonplaceholder.typicode.com/posts')

    if response.status_code == 200:
        posts = response.json()
        even_user_posts = [post for post in posts if post['userId'] % 2 == 0]
        for post in even_user_posts:
            print(
                f"User ID: {post['userId']}, Post ID: {post['id']}, Title: {post['title']}"
            )
    else:
        print("Не удалось получить посты с сервера.")


def create_post():
    new_post = {
        'title': 'Тестовый пост',
        'userId': 1,
    }

    response = requests.post(
        'https://jsonplaceholder.typicode.com/posts', json=new_post
    )

    if response.status_code == 201:
        created_post = response.json()
        print("Созданный пост:", created_post)
    else:
        print("Не удалось создать пост.")


def update_post():
    updated_post = {
        'title': 'Обновлённый пост',
        'userId': 1,
    }

    post_id = 1
    response = requests.put(
        f'https://jsonplaceholder.typicode.com/posts/{post_id}',
        json=updated_post,
    )

    if response.status_code == 200:
        updated_post = response.json()
        print("Обновленный пост:", updated_post)
    else:
        print("Не удалось обновить пост.")
