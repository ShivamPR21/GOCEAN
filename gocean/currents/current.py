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
    :param mdt:
    :param ll_grid:
    :return:
    """
    row, col = mdt.shape
    # new_grid_phi_prev = np.zeros([row + 1, col])
    # new_grid_phi_prev[1:, :] = mdt
    #
    # new_grid_phi_next = np.zeros([row + 1, col])
    # new_grid_phi_next[:-1, :] = mdt
    #
    # d_grid_phi = new_grid_phi_prev - new_grid_phi_next
    # d_grid_phi = d_grid_phi[1:, :]

    omega_e = 0.000072722  # rad/s
    r = 6378000  # m
    gamma = 9.8  # m/s^2

    phi_grid = np.array(ll_grid[:, :, 0], dtype=float)
    # print(phi_grid.shape)
    #
    # scale_factor = gamma / (r * 2 * omega_e * np.sin(phi_grid * np.pi / 180))
    # u = scale_factor * d_grid_phi * 180 / (0.1 * np.pi)
    #
    # new_grid_lambda_prev = np.zeros([row, col + 1])
    # new_grid_lambda_prev[:, 1:] = mdt
    #
    # new_grid_lambda_next = np.zeros([row, col + 1])
    # new_grid_lambda_next[:, :-1] = mdt
    #
    # d_grid_lambda = new_grid_lambda_prev - new_grid_lambda_next
    # d_grid_lambda = d_grid_lambda[:, 1:]
    #
    # omega_e = 0.000072722  # rad/s
    # r = 6378000  # m
    # gamma = 9.8  # m/s^2
    #
    f = 2*omega_e * np.sin(phi_grid * np.pi / 180)
    scale_factor = gamma / (r * f)
    # v = scale_factor * d_grid_lambda * 180 / (0.1 * np.pi)

    d_phi = 0.1*np.pi/180

    v, u = np.gradient(mdt, d_phi, edge_order=2)
    v *= scale_factor/np.cos(phi_grid * np.pi / 180)
    u *= -scale_factor

    return u, v
