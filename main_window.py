from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QWidget,
    QMessageBox,
)
from PyQt5.QtSql import QSqlTableModel
from add_post_dialog import AddPostDialog


class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Управление записями")
        self.resize(600, 400)

        self.db_manager = db_manager

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Поиск по заголовку")

        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.search)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.load_data)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_dialog)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_post)

        self.table = QTableView(self)
        self.model = QSqlTableModel(self, self.db_manager.connection)
        self.model.setTable("posts")

        self.load_data()

        self.table.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.search_button)
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        """Загрузка данных из базы данных в таблицу."""
        if not self.model.select():
            print("Ошибка загрузки данных:", self.model.lastError().text())

    def search(self):
        """Поиск записей по заголовку."""
        search_term = self.search_field.text()
        if search_term:
            self.model.setFilter(f"title LIKE '%{search_term}%'")
        else:
            self.model.setFilter("")
        self.model.select()
        print(f"Поиск по заголовку: {search_term}")

    def open_add_dialog(self):
        """Открытие диалогового окна для добавления записи."""
        dialog = AddPostDialog(self.db_manager)
        if dialog.exec():
            self.load_data()

    def delete_post(self):
        """Удаление выбранной записи."""
        selected_index = self.table.currentIndex()
        if selected_index.row() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return

        confirm = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить выбранную запись?",
        )
        if confirm == QMessageBox.Yes:
            post_id = self.model.record(selected_index.row()).value("id")
            self.db_manager.delete_post(post_id)
            self.load_data()
