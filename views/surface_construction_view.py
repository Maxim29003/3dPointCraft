from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,  QLabel, QLineEdit, QPushButton,
                             QTextBrowser, QProgressBar, QCheckBox, QMessageBox, QFileDialog)

from modules.surface_construction import SurfaceConstruction
import sys
import random

class SurfaceConstructionView(QWidget):
    def __init__(self):
        super().__init__()
        self.surface_construction = SurfaceConstruction()
        self.path_file = None
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout()

        self.setLayout(main_layout)

        mesh_size_layout = QHBoxLayout()
        filter_layout = QHBoxLayout()


        self.btn_open_file = QPushButton("Выбрать файл")
        self.btn_open_file.clicked.connect(self.select_file)
        self.btn_start = QPushButton("Старт")
        self.btn_start.clicked.connect(self.start)
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.save)
        self.btn_review = QPushButton("Просмотр")
        self.btn_review.clicked.connect(self.review)

        self.lb_mesh_size = QLabel("Размер вокселя в мм : ")
        self.le_mesh_size = QLineEdit()

        self.lb_filter = QLabel("Значение фильтра: ")
        self.le_filter = QLineEdit()

        self.lb_state = QLabel("Состояние: ")

        instructions = QTextBrowser()
        instructions.insertPlainText('''Шаг 1:  Выбор файла облака точек
В интерфейсе программы выберите опцию "Выбрать файл", затем укажите файл формата PTS, PCD, PLY, содержащий облако точек.

Шаг 2:  Ввод значений вокселя
Укажите значения вокселя в миллиметрах в соответствующем поле ввода.

Шаг 3:  Ввод значения фильтра (целое число, большее или равное единице)
Фильтр предназначен для сглаживания поверхности.

Шаг 4:  Построение поверхности
Нажмите кнопку "Старт". Программа выполнит построение поверхности.

Шаг 5:  Просмотр
Нажмите кнопку "Просмотр". Программа откроет окно просмотра, где можно будет увидеть поверхность.

Шаг 6:  Сохранение
Нажмите кнопку "Сохранить". При сохранении необходимо добавить расширение файла (.ply, .obj, .gltf, .glb, .stl).
        ''')

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        mesh_size_layout.addWidget(self.lb_mesh_size)
        mesh_size_layout.addWidget(self.le_mesh_size)

        filter_layout.addWidget(self.lb_filter)
        filter_layout.addWidget(self.le_filter)

        main_layout.addWidget(self.btn_open_file, 0, 0)
        main_layout.addLayout(mesh_size_layout, 1, 0)
        main_layout.addLayout(filter_layout, 2, 0)
        main_layout.addWidget(self.btn_start, 3, 0)
        main_layout.addWidget(self.btn_review, 4, 0)
        main_layout.addWidget(self.btn_save, 5, 0)
        main_layout.addWidget(instructions, 0, 1, 6, -1)
        main_layout.addWidget(self.progress_bar, 6, 0)
        main_layout.addWidget(self.lb_state, 6, 1)

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
            "STL Files (*.stl);;PLY Files (*.ply);;OBJ Files (*.obj);;GLTF Files (*.gltf);;GLB Files (*.glb)",
            options=options
        )

        return path_file_res

    def start(self):
        self.lb_state.setText("Состояние: Создание поверхности ... ")
        self.repaint()

        if self.path_file is None:
            self.show_message_box("Ошибка", "Выберете файл")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        try:
            mesh_size = float(self.le_mesh_size.text())
        except Exception as e:
            self.show_message_box("Ошибка", "Размер сетки введен не корректно ")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        try:
            filter_value = int(self.le_filter.text())
        except Exception as e:
            self.show_message_box("Ошибка", "Значение филльтра введено не корректно ")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        self.progress_bar.setValue(random.randint(20, 60))
        self.repaint()

        try:
            self.surface_construction.open_pcd(self.path_file)
            self.surface_construction.create_mesh(mesh_size, filter_value)
        except Exception as e:
            self.progress_bar.setValue(0)
            self.show_message_box("Ошибка", "Ошибка в вычислениях")
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        self.lb_state.setText("Состояние: Поверхность создана ")
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
        res_review = self.surface_construction.output_mesh()

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

        res_save = self.surface_construction.save_mesh(path_save)

        if res_save is None:
            self.show_message_box("Ошибка", "Ошибка сохранения")
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()

        else:
            self.surface_construction.save_mesh(path_save)
            self.lb_state.setText(f"Состояние: Сохранение завершино путь {path_save}")
            self.repaint()

