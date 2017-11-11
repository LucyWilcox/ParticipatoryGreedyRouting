from __future__ import print_function, division

import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from scipy.signal import convolve2d


class CityViewer:
    """Generates an animated view of an array image."""

    cmap = plt.get_cmap('YlOrRd')
    
    options = dict(interpolation='none', alpha=0.8,
                   vmin=0, vmax=9)

    def __init__(self, viewee):
        self.viewee = viewee
        self.im = None
        self.hlines = None
        self.vlines = None

    # TODO: should this really take iters?
    def step(self, iters=1):
        """Advances the viewee the given number of steps."""
        for i in range(iters):
            self.viewee.step()

    def draw(self, grid=False):
        """Draws the array and any other elements.
        
        grid: boolean, whether to draw grid lines
        """
        for loc in self.viewee.has_wifi_spaces:
            self.viewee.array[loc] = 5
        self.draw_array(self.viewee.array, origin='lower')
        self.draw_agents()
        plt.show()

    def draw_agents(self):
        """Plots the agents.
        """
        xs_c, xs_u, xs_s, ys_c, ys_u, ys_s = self.get_coords()

        self.points_c = plt.plot(xs_c, ys_c, '.', color='red')[0]
        self.points_u = plt.plot(xs_u, ys_u, '.', color='blue')[0]
        self.points_s = plt.plot(xs_s, ys_s, 'o', color='red')[0]
        
    
    def get_coords(self):
        """Gets the coordinates of the agents.
        
        Transforms from (row, col) to (x, y).
        
        returns: tuple of sequences, (xs, ys)
        """
        connected_routers = self.viewee.has_wifi_routers
        unconnected_routers = self.viewee.no_wifi_routers
        c_rows, c_cols = np.transpose([router.loc for router in connected_routers])

        u_rows, u_cols = np.transpose([router.loc for router in unconnected_routers])

        s_rows, s_cols = np.transpose([loc for loc in self.viewee.super_routers_loc])

        xs_c = c_cols + 0.5
        ys_c = c_rows + .05

        xs_u = u_cols + 0.5
        ys_u = u_rows + 0.5

        xs_s = s_cols + 0.5
        ys_s = s_rows + 0.5

        return xs_c, xs_u, xs_s, ys_c, ys_u, ys_s

    def draw_array(self, array=None, cmap=None, **kwds):
        """Draws the cells."""
        # Note: we have to make a copy because some implementations
        # of step perform updates in place.
        if array is None:
            array = self.viewee.array
        a = array.copy()
        cmap = self.cmap if cmap is None else cmap

        n, m = a.shape
        plt.axis([0, m, 0, n])
        plt.xticks([])
        plt.yticks([])

        options = self.options.copy()
        options['extent'] = [0, m, 0, n]
        options.update(kwds)
        self.im = plt.imshow(a, cmap, **options)

    def draw_grid(self):
        """Draws the grid."""
        a = self.viewee.array
        n, m = a.shape
        lw = 2 if m < 10 else 1
        options = dict(color='white', linewidth=lw)

        rows = np.arange(1, n)
        self.hlines = plt.hlines(rows, 0, m, **options)

        cols = np.arange(1, m)
        self.vlines = plt.vlines(cols, 0, n, **options)