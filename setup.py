
import open3d as o3d

pcd = o3d.io.read_point_cloud("C:\\Users\\Maxim\\Desktop\\res_2.pts")

o3d.io.write_point_cloud("C:\\Users\\Maxim\\Desktop\\res_2.pcd", pcd)