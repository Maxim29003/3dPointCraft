import open3d as o3d
import os


class PointCloudFiltering:
    def __init__(self):
        self.pcd = None
        self.filtered_pcd = None
        self.outliers = None

    def open_pcd(self, path_file):
        self.pcd = o3d.io.read_point_cloud(path_file)

    def filter_pcd(self, number_neighbors, multiplier):
        filter_pcd = self.pcd.remove_statistical_outlier(number_neighbors, multiplier)
        self.outliers = self.pcd.select_by_index(filter_pcd[1], invert=True)
        self.outliers.paint_uniform_color([1, 0, 0])
        self.filtered_pcd = filter_pcd[0]

    def output_pcd(self):
        if self.filtered_pcd is None and self.outliers is None:
            return None
        else:
            o3d.visualization.draw_geometries([self.filtered_pcd, self.outliers])
            return 0

    def save_pcd(self, path_save):
        file_extension = os.path.splitext(path_save)[1]
        extensions = [".pts", ".ply", ".pcd"]
        if file_extension in extensions and self.filtered_pcd is not None:
            o3d.io.write_point_cloud(path_save, self.filtered_pcd)
            return 0
        else:
            return None




