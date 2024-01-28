from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,  QLabel, QLineEdit, QPushButton,
                             QTextBrowser, QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from modules.surface_cleaning import SurfaceCleaning
import sys
import random


class SurfaceCleaningView(QWidget):
    def __init__(self):
        super().__init__()
        self.surface_cleaning = SurfaceCleaning()
        self.path_file = None
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(main_layout)

        self.btn_open_file = QPushButton("Выбрать файл ")
        self.btn_open_file.clicked.connect(self.select_file)
        self.btn_start = QPushButton("Старт")
        self.btn_start.clicked.connect(self.start)
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.save)
        self.btn_review = QPushButton("Просмотр")
        self.btn_review.clicked.connect(self.review)


        self.lb_state = QLabel("Состояние: ")

        instructions = QTextBrowser()
        instructions.insertPlainText('''Шаг 1:  Выбор файла поверхности
В интерфейсе программы выберите опцию "Выбрать файл", затем укажите файл формата PLY  содержащий поверхность.

Шаг 2:  Выполнение удаления выбросов в поверхности.
Нажмите кнопку "Старт" для удаления выбросов в поверхности.

Шаг 3:  Просмотр
Нажмите кнопку "Просмотр". Программа откроет окно просмотра, где можно будет увидеть поверхность.

Шаг 4:  Сохранение
Нажмите кнопку "Сохранить". При сохранении необходимо добавить расширение файла .ply.''')

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)


        main_layout.addWidget(self.btn_open_file, 0, 0)
        main_layout.addWidget(self.btn_start, 1, 0)
        main_layout.addWidget(self.btn_review, 2, 0)
        main_layout.addWidget(self.btn_save, 3, 0)
        main_layout.addWidget(instructions, 0, 3, 6, -1)
        main_layout.addWidget(self.progress_bar, 7, 0)
        main_layout.addWidget(self.lb_state, 7, 1, 1, -1)
        self.setFixedSize(700, 300)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "PLY Files (*.ply)")

        if file_name:
            self.lb_state.setText(f"Состояние: Выбранный файл: {file_name} ")
            self.repaint()
            self.path_file = file_name

    def show_message_box(self, title, text):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setStandardButtons(QMessageBox.Ok)
        result = message_box.exec_()

    def get_path_file_res(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        path_file_res, _ = QFileDialog.getSaveFileName(self, "Сохранить файл ", "", "PLY Files (*.ply)",
                                                       options=options)

        return path_file_res

    def start(self):
        self.lb_state.setText("Состояние: Очистка поаерхности ... ")
        self.repaint()

        if self.path_file is None:
            self.show_message_box("Ошибка", "Выберете файл")
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        self.progress_bar.setValue(random.randint(31, 50))
        self.repaint()

        try:
            self.surface_cleaning.mesh_cleaning(self.path_file)
        except Exception as e:
            self.progress_bar.setValue(0)
            self.show_message_box("Ошибка", "Ошибка в вычислениях")
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return



        self.lb_state.setText("Состояние: Очистка поаерхности завершина")
        self.progress_bar.setValue(100)
        self.repaint()

    def review(self):
        self.lb_state.setText("Состояние: Отрытие окак просмотра")
        self.repaint()

        res_review = self.surface_cleaning.output_mesh()

        if res_review is None:
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
        res_save = self.surface_cleaning.save_mesh(path_save)

        if res_save is None:
            self.show_message_box("Ошибка", "Ошибка сохранения")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
        else:
            self.surface_cleaning.save_mesh(path_save)
            self.lb_state.setText(f"Состояние: Сохранение завершино путь {path_save}")
            self.repaint()


