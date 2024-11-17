import requests
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord

class DatabaseManager:
    def __init__(self, db_name):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        
        if not self.db.open():
            print("Не удалось открыть базу данных!")
        else:
            print("База данных открыта успешно!")

    def close_connection(self):
        self.db.close()

    @property
    def connection(self):
        return self.db

    def create_table(self):
        query = QSqlQuery(self.db)
        query.exec_(
            '''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                body TEXT
            )
            '''
        )

    def is_table_empty(self):
        query = QSqlQuery(self.db)
        query.exec_("SELECT COUNT(*) FROM posts")
        if query.next():
            count = query.value(0)
            return count == 0
        return True

    def fetch_posts(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            print("Данные успешно получены с сервера.")
            return posts
        else:
            print("Ошибка при получении данных:", response.status_code)
            return []

    def save_posts(self, posts):
        query = QSqlQuery(self.db)

        for post in posts:
            query.prepare(
                '''
                INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)
                '''
            )
            query.addBindValue(post['id'])
            query.addBindValue(post['userId'])
            query.addBindValue(post['title'])
            query.addBindValue(post['body'])
            query.exec_()

        print(f"Сохранено {len(posts)} постов в базу данных.")
    
    def fetch_all_posts(self):
        query = QSqlQuery(self.db)
        query.exec_("SELECT * FROM posts")

        posts = []
        while query.next():
            record = query.record()
            post = {record.fieldName(i): record.value(i) for i in range(record.count())}
            posts.append(post)

        return posts

    def add_post(self, user_id, title, body):
        query = QSqlQuery(self.db)
        query.prepare(
            "INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)"
        )
        query.addBindValue(user_id)
        query.addBindValue(title)
        query.addBindValue(body)
        query.exec_()

    def delete_post(self, post_id):
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM posts WHERE id = ?")
        query.addBindValue(post_id)
        query.exec_()
