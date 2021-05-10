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

import numpy as np


def decompose(mdt, ll_grid):
    """
    Decompose the mdt in current components
    :param mdt: mean dynamic topography
    :param ll_grid: lat-long grid
    :return: current components -u, v
    """

    # Define variables
    omega_e = 0.000072722  # rad/s
    r = 6378000  # m
    gamma = 9.8  # m/s^2

    # Define the grid required
    phi_grid = np.array(ll_grid[:, :, 0], dtype=float)

    # Get the scale factor
    f = 2 * omega_e * np.sin(phi_grid * np.pi / 180)
    scale_factor = gamma / (r * f)

    # Phi differential
    d_phi = 0.1

    # current components
    v, u = np.gradient(mdt, d_phi, edge_order=2)
    v *= scale_factor / np.cos(phi_grid * np.pi / 180)
    u *= -scale_factor

    # Return components
    return -u, v
