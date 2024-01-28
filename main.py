from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from views.voxel_reduction_view import VoxelReductionView
from views.surface_construction_view import SurfaceConstructionView
from views.point_cloud_filtering_view import PointCloudFilteringView
from views.surface_cleaning_view import SurfaceCleaningView
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3DPointCraft")
        self.setFixedSize(700, 400)

        main_layout = QVBoxLayout(self)

        tab_widget = QTabWidget(self)

        voxel_reduction_view = VoxelReductionView()
        tab_widget.addTab(voxel_reduction_view, "Упрощение облака точек")

        point_cloud_filtering_view = PointCloudFilteringView()
        tab_widget.addTab(point_cloud_filtering_view, "Фильтр облака точек")

        surface_construction_view = SurfaceConstructionView()
        tab_widget.addTab(surface_construction_view, "Построение поверхности")

        surface_cleaning = SurfaceCleaningView()
        tab_widget.addTab(surface_cleaning, "Очистка поверхности")

        main_layout.addWidget(tab_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())