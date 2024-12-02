import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QLabel, QComboBox, QFileDialog, QWidget, QLineEdit, QHBoxLayout, QSplitter, QFormLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.dates import DateFormatter

class DataVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Анализ данных")
        self.setGeometry(100, 100, 1200, 800)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.file_selection_layout = QHBoxLayout()
        self.load_button = QPushButton("Загрузить CSV файл")
        self.load_button.clicked.connect(self.load_data)
        self.file_selection_layout.addWidget(self.load_button)

        self.file_name_label = QLabel("")
        self.file_selection_layout.addWidget(self.file_name_label)
        self.file_selection_layout.setAlignment(Qt.AlignTop)

        self.main_layout.addLayout(self.file_selection_layout)

        self.file_selection_layout.setSpacing(10)
        self.file_selection_layout.setContentsMargins(10, 10, 10, 10)

        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)
        
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 10) 

        # (Статистика)
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)

        self.stats_title_label = QLabel("Статистика")
        self.stats_title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.left_layout.addWidget(self.stats_title_label)

        self.stats_label = QLabel("")
        self.left_layout.addWidget(self.stats_label)
        self.left_layout.setAlignment(Qt.AlignTop)


        self.splitter.addWidget(self.left_widget)

        # (Графики)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_layout.setAlignment(Qt.AlignTop)
        self.charts_title_label = QLabel("Графики")
        self.charts_title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.right_layout.addWidget(self.charts_title_label)

        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Линейный график", "Гистограмма", "Круговая диаграмма"])

        self.chart_type_combo.currentIndexChanged.connect(self.update_chart)
        self.right_layout.addWidget(self.chart_type_combo)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.right_layout.addWidget(self.canvas)

        self.form_layout = QFormLayout()

        self.date_label = QLabel("Date:")
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Введите Date (ГГГГ-ММ-ДД)")
        self.form_layout.addRow(self.date_label, self.date_input)

        self.value1_label = QLabel("Value1:")
        self.value1_input = QLineEdit()
        self.value1_input.setPlaceholderText("Введите Value1")
        self.form_layout.addRow(self.value1_label, self.value1_input)

        self.value2_label = QLabel("Value2:")
        self.value2_input = QLineEdit()
        self.value2_input.setPlaceholderText("Введите Value2")
        self.form_layout.addRow(self.value2_label, self.value2_input)

        self.category_label = QLabel("Category:")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Введите Category")
        self.form_layout.addRow(self.category_label, self.category_input)


        self.add_value_button = QPushButton("Добавить данные")
        self.add_value_button.clicked.connect(self.add_data)
        self.form_layout.addRow(self.add_value_button)

        self.right_layout.addLayout(self.form_layout)

        self.splitter.addWidget(self.right_widget)

        self.splitter.setSizes([self.width() // 3, 2 * self.width() // 3])

        self.data = None

        self.toggle_elements_visibility(False)

    def toggle_elements_visibility(self, visible):
        self.stats_label.setVisible(visible)
        self.stats_title_label.setVisible(visible)
        self.chart_type_combo.setVisible(visible)
        self.canvas.setVisible(visible)
        self.charts_title_label.setVisible(visible)

        self.date_label.setVisible(visible)
        self.date_input.setVisible(visible)
        self.value1_label.setVisible(visible)
        self.value1_input.setVisible(visible)
        self.value2_label.setVisible(visible)
        self.value2_input.setVisible(visible)
        self.category_label.setVisible(visible)
        self.category_input.setVisible(visible)
        self.add_value_button.setVisible(visible)


    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_name:
            self.data = pd.read_csv(file_name)

            self.file_name_label.setText(f"Файл: {file_name.split('/')[-1]}")

            stats = (
                f"Количество строк: {len(self.data)}\n"
                f"Количество столбцов: {len(self.data.columns)}\n\n"
                "Минимальные значения:\n" + self.data.min().to_string() + "\n\n"
                "Максимальные значения:\n" + self.data.max().to_string() + "\n\n"
                "Медианные значения:\n" + self.data.median(numeric_only=True).to_string() + "\n\n"
                "Средние значения:\n" + self.data.mean(numeric_only=True).to_string()
            )
            self.stats_label.setText(stats)

            self.toggle_elements_visibility(True)

            self.update_chart()


    def update_chart(self):
        if self.data is not None:
            if "Date" in self.data.columns:
                self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")

            self.data = self.data.sort_values(by="Date")

            chart_type = self.chart_type_combo.currentText()

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            if chart_type == "Линейный график" and "Date" in self.data.columns and "Value1" in self.data.columns:
                ax.plot(self.data["Date"], self.data["Value1"], marker="o")
                ax.set_title("Линейный график")
                ax.set_xlabel("Date")
                ax.set_ylabel("Value1")

                date_format = DateFormatter("%d-%m-%y")
                ax.xaxis.set_major_formatter(date_format)

                for label in ax.get_xticklabels():
                    label.set_rotation(10)
                    label.set_horizontalalignment('right')

            elif chart_type == "Гистограмма" and "Value2" in self.data.columns:
                sns.histplot(self.data["Value2"], bins=10, ax=ax, kde=True)
                ax.set_title("Гистограмма")

            elif chart_type == "Круговая диаграмма" and "Category" in self.data.columns:
                self.data["Category"].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
                ax.set_title("Круговая диаграмма")

            else:
                ax.text(0.5, 0.5, "Неверные столбцы для выбранного типа графика", horizontalalignment='center')

            self.canvas.draw()


    def add_data(self):
        if self.data is not None:
            try:
                date = self.date_input.text()
                value1 = float(self.value1_input.text())
                value2 = float(self.value2_input.text())
                category = self.category_input.text()

                new_row = {
                    "Date": date,
                    "Value1": value1,
                    "Value2": value2,
                    "Category": category
                }

                self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
                self.date_input.clear()
                self.value1_input.clear()
                self.value2_input.clear()
                self.category_input.clear()
                self.update_chart()
            except Exception as e:
                self.stats_label.setText(f"Error adding data: {e}")
        else:
            self.stats_label.setText("Please load data first.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataVisualizer()
    window.show()
    sys.exit(app.exec_())
