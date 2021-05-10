#!/usr/bin/python3
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

# Import packages
import os
import re

import numpy as np
import pandas as pd


# Process string for numerical output
def strproc(string):
    """
    process the string input and splits
    :param string:
    :return:
    """
    split_kwrg = re.split('\s+', string)
    return list(filter(None, split_kwrg))


def split_data(df):
    """
    Splits the string in logical partitions
    :param df: dataframe that is affected due to wrong formatting
    :return: new DataFrame
    """
    new_data = []
    for i, row in enumerate(df.iloc[:].values):
        new_data.append(strproc(row[0]))
    return new_data


class GeoidIO:
    """
    Works on the geoid read and grid creation
    """

    def __init__(self, data_dir=None):
        self.data_dir = str(data_dir)
        self.header = {}
        self.data = []
        self.grid = None

    def read(self, file_name='geoid.gdf'):
        """
        Reads Geoid information from the file given
        :param file_name: String
        """
        with open(os.path.join(self.data_dir, file_name), 'r') as file:
            header = True
            for line in file:
                prc_line = strproc(line)
                if header and len(prc_line) > 0:
                    # If longitude parallel is obtained
                    if prc_line[0] == 'longitude_parallels':
                        self.header.update({'longitude_parallels': int(prc_line[1])})

                    # If latitude parallels encountered
                    if prc_line[0] == 'latitude_parallels':
                        self.header.update({'latitude_parallels': int(prc_line[1])})

                    # If latitude south limit is encountered
                    if prc_line[0] == 'latlimit_south':
                        self.header.update({'lat_min': float(prc_line[1])})
                    # If latitude north limit encountered
                    if prc_line[0] == 'latlimit_north':
                        self.header.update({'lat_max': float(prc_line[1])})

                    # If longitude west limit encountered
                    if prc_line[0] == 'longlimit_west':
                        self.header.update({'long_min': float(prc_line[1])})
                    # If longitude east limit encountered
                    if prc_line[0] == 'longlimit_east':
                        self.header.update({'long_max': float(prc_line[1])})

                    # If end of header
                    if prc_line[0].startswith('end_of_head'):
                        header = False
                elif len(prc_line) > 0:
                    self.data.append([float(prc_line[0]),
                                      float(prc_line[1]),
                                      float(prc_line[2])
                                      ])
            self.data = pd.DataFrame(self.data, columns=['long', 'lat', 'geoid'])

    def create_geoid_grid(self):
        """
        Creates geoid grid required for MDT and SSH grids
        """
        # Initiate grid
        self.grid = np.zeros([self.header['latitude_parallels'],
                              self.header['longitude_parallels'], 3])

        # Latitude grid values
        self.grid[:, :, 0] = np.reshape(self.data['lat'].values,
                                        [self.header['latitude_parallels'],
                                         self.header['longitude_parallels']])

        # Longitude grid values
        self.grid[:, :, 1] = np.reshape(self.data['long'].values,
                                        [self.header['latitude_parallels'],
                                         self.header['longitude_parallels']])

        # Geoid grid values
        self.grid[:, :, 2] = np.reshape(self.data['geoid'].values,
                                        [self.header['latitude_parallels'],
                                         self.header['longitude_parallels']])
