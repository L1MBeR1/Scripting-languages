import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from database_manager import DatabaseManager

def main():
    db_manager = DatabaseManager('posts.db')
    db_manager.create_table()

    if db_manager.is_table_empty():
        db_manager.fetch_and_save_posts()

    posts = db_manager.fetch_all_posts()
    if posts is None or len(posts) == 0:
        print("Таблица не существует или данные отсутствуют.")
    else:
        print("Таблица с записями существует")

    app = QApplication(sys.argv)
    main_window = MainWindow(db_manager)
    main_window.show()

    exit_code = app.exec_()
    db_manager.close_connection()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
