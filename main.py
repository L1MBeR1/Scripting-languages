import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from database_manager import DatabaseManager

def main():
    db_manager = DatabaseManager('posts.db')
    db_manager.create_table()


    app = QApplication(sys.argv)
    main_window = MainWindow(db_manager)
    main_window.show()

    exit_code = app.exec_()
    db_manager.close_connection()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
