from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,  QLabel, QLineEdit, QPushButton,
                             QTextBrowser, QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from modules.voxel_reduction import VoxelReduction
import os
import sys
import random


class VoxelReductionView(QWidget):
    def __init__(self):
        super().__init__()
        self.path_file = None
        self.initUI()


    def initUI(self):
        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(main_layout)

        voxel_layout = QHBoxLayout()

        self.btn_open_file = QPushButton("Выбрать файл .pts")
        self.btn_open_file.clicked.connect(self.select_file)
        self.btn_start = QPushButton("Старт")
        self.btn_start.clicked.connect(self.start)

        self.lb_voxel = QLabel("Размер вокселя в мм: ")

        self.le_voxel = QLineEdit()

        self.lb_state = QLabel("Состояние: ")

        instructions = QTextBrowser()
        instructions.insertPlainText('''Шаг 1:  Выбор файла облака точек
- В интерфейсе программы выберите опцию "Выбрать PTS", затем укажите файл формата PTS, содержащий облако точек.

Шаг 2:  Ввод значений вокселя
- Укажите значения вокселя в миллиметрах в соответствующем поле ввода. Эти значения определяют размер вокселей для уменьшения облака точек.

Шаг 3:  Выполнение воксельного понижения и сохранение
- Нажмите кнопку "Старт". Программа автоматически предложит сохранить итоговый файл без необходимости указывать расширение. Программа обработает облако точек, используя введенные значения вокселя.
 ''')

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        voxel_layout.addWidget(self.lb_voxel)
        voxel_layout.addWidget(self.le_voxel)

        main_layout.addWidget(self.btn_open_file, 0, 0)
        main_layout.addLayout(voxel_layout, 1, 0)
        main_layout.addWidget(self.btn_start, 2, 0)
        main_layout.addWidget(instructions, 0, 1, 6, -1)
        main_layout.addWidget(self.progress_bar, 7, 0)
        main_layout.addWidget(self.lb_state, 7, 1, 1, -1)
        self.setFixedSize(700, 300)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл .pts", "", "PTS Files (*.pts)")

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

        path_file_res, _ = QFileDialog.getSaveFileName(self, "Сохранить файл .pts", "", "PTS Files (*.pts)",
                                                       options=options)

        return path_file_res + '.pts'

    def start(self):

        voxel = self.le_voxel.text()

        if self.path_file is None:
            self.show_message_box("Ошибка", "Выберете файл")
            self.lb_state.setText("Состояние: ")
            self.progress_bar.setValue(0)
            self.repaint()
            return

        try:
            voxel = float(voxel)
        except Exception as e:
            self.show_message_box("Ошибка", "Введите значение Вокселя или значение Вокселя не корректное")
            self.lb_state.setText("Состояние: ")
            self.progress_bar.setValue(0)
            self.repaint()
            return

        path_file_res = self.get_path_file_res()

        self.progress_bar.setValue(random.randint(31, 50))
        self.repaint()

        folder_path = os.path.dirname(path_file_res)

        path_file_intermediate = os.path.join(folder_path, 'intermediate.pts')


        try:
            self.lb_state.setText("Состояние: Упращение облака точек")
            self.repaint()
            voxel_reduction = VoxelReduction(self.path_file, path_file_res, path_file_intermediate)
            voxel_reduction.start(voxel)
            self.progress_bar.setValue(random.randint(51, 90))
            self.repaint()

        except Exception as e:
            self.show_message_box("Ошибка", "Ошибка вычислений")
            os.remove(path_file_intermediate)
            self.progress_bar.setValue(0)
            self.lb_state.setText("Состояние: ")
            self.repaint()
            return

        os.remove(path_file_intermediate)
        self.lb_state.setText(f"Состояние: Упращение облака точек выполнено путь {path_file_res}")
        self.progress_bar.setValue(100)
        self.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VoxelReductionView()
    window.show()
    sys.exit(app.exec_())