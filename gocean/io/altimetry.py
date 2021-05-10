# Copyright 2021 Shivam Pandey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import libraries
import glob
import os

import netCDF4 as nc
import numpy as np
from scipy.interpolate import griddata
from sklearn.neighbors import BallTree


class SSHIO:
    """
    Reads and interpolated the Sea Surface Height from netcdf files
    for SARAL and JASON2
    """

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.file_list = glob.glob(os.path.join(self.data_dir, '*', '*', '*.nc'))
        self.grid = None
        self.grid_filled = None
        self.mask = None

    def read(self, grid, fill_missing=True, sigma=2, rm_outlier=True):
        """
        Reads the data from file and fill the provided grid
        The grid should be similar to that of Geoid
        :param sigma:
        :param rm_outlier:
        :param grid: numpy grid with first 2 bands as lat long and the last one is geoid
        :param fill_missing: Bool if true, the missing values will be interpolated.
        """
        grid_shape = [grid.shape[0], grid.shape[1], 2]
        self.grid = np.zeros(grid_shape)

        # Initiate frequency of altimtery data
        frequency = self.grid[:, :, 0].flatten()
        mean_ssh = self.grid[:, :, 1].flatten()

        # Create latitude and longitude grid
        lat_long = np.concatenate(([grid[:, :, 0].flatten()], [grid[:, :, 1].flatten()]), axis=0).T

        # Ctreate ball search tree
        source_grid = BallTree(lat_long)

        # Load and interpolate the data
        for file in self.file_list:
            dataset = nc.Dataset(file, 'r')
            lat_long_query = np.concatenate(([dataset['glat.00'][:].data],
                                             [dataset['glon.00'][:].data]),
                                            axis=0).T
            ssh = np.array([dataset['ssh.33'][:].data], dtype=float).T
            idx = source_grid.query(lat_long_query, return_distance=False)

            frequency[idx] += 1
            mean_ssh[idx] = mean_ssh[idx] * (frequency[idx] - 1) / (frequency[idx]) + ssh / (frequency[idx])

        self.grid[:, :, 0] = np.reshape(frequency, grid_shape[:2])
        self.grid[:, :, 1] = np.reshape(mean_ssh, grid_shape[:2])

        if fill_missing:
            idx = np.where(frequency != 0)
            ll_coord = lat_long[idx]
            ssh_ll = mean_ssh[idx]

            # Statistical Outlier removal
            mu_ = np.mean(ll_coord, axis=0)
            std_ = np.std(ll_coord, axis=0)

            tr_map_1 = (ll_coord[:, 1] < mu_[1] + std_[1] * sigma) * (ll_coord[:, 1] > mu_[1] - std_[1] * sigma)
            tr_map_0 = (ll_coord[:, 0] < mu_[0] + std_[0] * sigma) * (ll_coord[:, 0] > mu_[0] - std_[0] * sigma)

            new_idx = np.where(tr_map_0 * tr_map_1)

            # Create the grid
            self.grid_filled = griddata(lat_long[idx][new_idx], mean_ssh[idx][new_idx], (grid[:, :, 0], grid[:, :, 1]))
            self.mask = np.isnan(self.grid_filled)
