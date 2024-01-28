import pandas as pd
import dask.dataframe as dd
import threading


class VoxelReduction:
    def __init__(self, path_to_initial_file, path_to_result_file, path_to_intermediate_file):
        self.lock = threading.Lock()
        self.ddf = dd.read_csv(path_to_initial_file, sep=' ', header=None, skiprows=1)
        self.amount = 0
        self.path_to_result_file = path_to_result_file
        self.path_to_intermediate_file = path_to_intermediate_file

    def voxel_downsizing(self, df, voxel_size):
        num_columns = df.shape[1]
        df['voxel_x'] = ((df[0] // voxel_size) * voxel_size).round(6)
        df['voxel_y'] = ((df[1] // voxel_size) * voxel_size).round(6)
        df['voxel_z'] = ((df[2] // voxel_size) * voxel_size).round(6)

        if num_columns == 7:
            df_downsampled = df.groupby(['voxel_x', 'voxel_y', 'voxel_z'])[[4, 5, 6]].mean().astype(int).reset_index()
        elif num_columns == 6:
            df_downsampled = df.groupby(['voxel_x', 'voxel_y', 'voxel_z'])[[3, 4, 5]].mean().astype(int).reset_index()
        elif num_columns == 10:
            df_downsampled = df.groupby(['voxel_x', 'voxel_y', 'voxel_z'])[[3, 4, 5]].mean().astype(int).reset_index()

        df_downsampled = df_downsampled.drop_duplicates()



        with self.lock:
            self.amount += len(df_downsampled)
            df_downsampled.to_csv(self.path_to_intermediate_file, mode='a', sep=' ', header=None, index=None)

    def save(self):
        with open(self.path_to_result_file, 'w') as file:
            file.write(f"{self.amount - 2}\n")

        chunksize = 10000

        for chunk in pd.read_csv(self.path_to_intermediate_file, chunksize=chunksize, skiprows=1):
            chunk.to_csv(self.path_to_result_file, mode='a', index=None, header=None)

    def start(self, voxel):
        res = self.ddf.map_partitions(self.voxel_downsizing, voxel).compute()
        self.save()




