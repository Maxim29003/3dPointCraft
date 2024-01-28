from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,  QLabel, QLineEdit, QPushButton,
                             QTextBrowser, QProgressBar, QFileDialog, QMessageBox)
import sys
from modules.point_cloud_filtering import PointCloudFiltering
import random


class PointCloudFilteringView(QWidget):
    def __init__(self):
        super().__init__()
        self.point_cloud_filtering = PointCloudFiltering()
        self.path_file = None
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout()

        self.setLayout(main_layout)
        number_neighbors_layout = QHBoxLayout()
        multiplier_layout = QHBoxLayout()

        self.btn_open_file = QPushButton("Выбрать файл")
        self.btn_open_file.clicked.connect(self.select_file)
        self.btn_start = QPushButton("Старт")
        self.btn_start.clicked.connect(self.start)
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.save)
        self.btn_review = QPushButton("Просмотр")
        self.btn_review.clicked.connect(self.review)

        self.lb_multiplier = QLabel("Множитель: ")
        self.le_multiplier = QLineEdit()

        self.lb_number_neighbors = QLabel("Количесвто соседей: ")
        self.le_number_neighbors = QLineEdit()

        self.lb_state = QLabel("Состояние: ")

        instructions = QTextBrowser()
        instructions.insertPlainText('''Шаг 1:  Выбор файла облака точек
- В интерфейсе программы выберите опцию "Выбрать файл", затем укажите файл формата PTS, PCD, PLY, содержащий облако точек.

Шаг 2:  Ввод Количества соседей  (целое число)
- Укажите количество соседей, которые будут использованы для оценки статистических характеристик каждой точки. Большее значение обычно увеличит чувствительность к выбросам.

Шаг 3:  Ввод Множителя  (целое число)
- Укажите коэффициент множителя, используемого для вычисления порога определения выбросов. Больший множитель делает алгоритм менее чувствительным к выбросам.

Шаг 4:  Выполнение удаления статистических выбросов в облаке точек.
- Нажмите кнопку "Старт". Программа выполнит удаление статистических выбросов в облаке точек.

Шаг 5:  Просмотр
- Нажмите кнопку "Просмотр". Программа откроет окно просмотра. Красные точки обозначают шум и будут удалены.

Шаг 6:  Сохранение
- Нажмите кнопку "Сохранить". При сохранении необходимо добавить расширение файла (.pts, .ply, .pcd).
         ''')

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        number_neighbors_layout.addWidget(self.lb_number_neighbors)
        number_neighbors_layout.addWidget(self.le_number_neighbors)

        multiplier_layout.addWidget(self.lb_multiplier)
        multiplier_layout.addWidget(self.le_multiplier)

        main_layout.addWidget(self.btn_open_file, 0, 0)
        main_layout.addLayout(number_neighbors_layout, 1, 0)
        main_layout.addLayout(multiplier_layout, 2, 0)
        main_layout.addWidget(self.btn_start, 3, 0)
        main_layout.addWidget(self.btn_review, 4, 0)
        main_layout.addWidget(self.btn_save, 5, 0)
        main_layout.addWidget(instructions, 0, 1, 6, -1)
        main_layout.addWidget(self.progress_bar, 6, 0)
        main_layout.addWidget(self.lb_state, 6, 1, 1, -1)

        self.setFixedSize(700, 300)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл .pts, .pcd .ply ",
            "",
            "PTS Files (*.pts);;PCD Files (*.pcd);;PLY Files (*.ply)"
        )

        if file_name:
            self.lb_state.setText(f"Состояние: Выбранный файл: {file_name}")
            self.repaint()
            self.path_file = file_name

    def get_path_file_res(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        path_file_res, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл .pts",
            "",
            "PTS Files (*.pts);;PCD Files (*.pcd);;PLY Files (*.ply)",
            options=options
        )

        return path_file_res

    def start(self):
        self.lb_state.setText("Состояние: Фильтрация облака точек")
        self.progress_bar.setValue(random.randint(30, 70))
        self.repaint()

        if self.path_file is None:
            self.show_message_box("Ошибка", "Выберете файл")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        try:
            number_neighbors = int(self.le_number_neighbors.text())
        except Exception as e:
            self.show_message_box("Ошибка", "Количесвто соседей введено не корректно ")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        try:
            multiplier = int(self.le_multiplier.text())
        except Exception as e:
            self.show_message_box("Ошибка", "Множитель введен не корректно ")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        self.point_cloud_filtering.open_pcd(self.path_file)
        self.point_cloud_filtering.filter_pcd(number_neighbors, multiplier)

        self.lb_state.setText("Состояние: Фильтрация облака точек завершина")
        self.progress_bar.setValue(100)
        self.repaint()

    def show_message_box(self, title, text):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setStandardButtons(QMessageBox.Ok)
        result = message_box.exec_()

    def review(self):
        self.lb_state.setText("Состояние: Отрытие окак просмотра")
        self.repaint()
        res_view = self.point_cloud_filtering.output_pcd()
        if res_view is None:
            self.show_message_box("Ошибка", "Ошибка просмотра")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
        else:
            self.lb_state.setText("Состояние: Окно просмотра открыто")
            self.repaint()

    def save(self):
        self.lb_state.setText("Состояние: Сохранение ...")
        self.repaint()
        path_save = self.get_path_file_res()
        res_save = self.point_cloud_filtering.save_pcd(path_save)

        if res_save is None:
            self.show_message_box("Ошибка", "Ошибка сохранения")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
        else:
            self.point_cloud_filtering.save_pcd(path_save)
            self.lb_state.setText(f"Состояние: Сохранение завершино путь {path_save}")
            self.repaint()

