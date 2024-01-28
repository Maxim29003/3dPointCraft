import open3d as o3d
import numpy as np
from skimage.measure import marching_cubes
from scipy.interpolate import NearestNDInterpolator
import os


class SurfaceConstruction:
    def __init__(self):
        self.pcd = None
        self.mesh = None

    def open_pcd(self, path_file):
        self.pcd = o3d.io.read_point_cloud(path_file)

    def create_mesh(self, resolution, filter_value):

        points = np.asarray(self.pcd.points)
        colors = np.asarray(self.pcd.colors)

        min_bound = np.min(points, axis=0)
        max_bound = np.max(points, axis=0)
        grid_shape = ((max_bound - min_bound) / resolution).astype(int) + 1
        grid = np.zeros(grid_shape, dtype=bool)
        indices = ((points - min_bound) / resolution).astype(int)
        grid[indices[:, 0], indices[:, 1], indices[:, 2]] = True

        vertices, faces, _, _ = marching_cubes(grid, level=0)

        interp = NearestNDInterpolator(indices, colors)
        interp_colors = interp(vertices)

        self.mesh = o3d.geometry.TriangleMesh()
        self.mesh.vertices = o3d.utility.Vector3dVector(vertices * resolution + min_bound)
        self.mesh.triangles = o3d.utility.Vector3iVector(faces)
        self.mesh.vertex_colors = o3d.utility.Vector3dVector(interp_colors)
        self.mesh = self.mesh.filter_smooth_simple(number_of_iterations=filter_value)
        self.mesh.compute_vertex_normals()

    def output_mesh(self):
        if self.mesh is None:
            return None
        o3d.visualization.draw_geometries([self.mesh])
        return 0

    def save_mesh(self, path_save):
        file_extension = os.path.splitext(path_save)[1]
        extensions = [".stl", ".ply", ".obj", ".gltf", ".glb"]
        if file_extension in extensions and self.mesh is not None:
            o3d.io.write_triangle_mesh(path_save, self.mesh)
            return 0

        else:
            return None













