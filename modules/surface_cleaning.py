import open3d as o3d
import pyvista as pv
import numpy as np
import os


class SurfaceCleaning:
    def __init__(self):
        self.mesh = None

    def mesh_cleaning(self, file_path):
        mesh_pv = pv.read(file_path)

        largest = mesh_pv.connectivity(largest=True)

        vertices = np.array(largest.points)
        triangles = np.array(largest.faces.reshape(-1, 4)[:, 1:4])

        colors = np.array(largest.point_data['RGB'])

        self.mesh = o3d.geometry.TriangleMesh()
        self.mesh.vertices = o3d.utility.Vector3dVector(vertices)
        self.mesh.triangles = o3d.utility.Vector3iVector(triangles)
        self.mesh.vertex_colors = o3d.utility.Vector3dVector(colors / 255.0)
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