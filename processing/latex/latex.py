from math import pi, sin, cos, sqrt

import os
import pylab
from matplotlib.font_manager import FontProperties
from pylab import meshgrid, linspace, contourf, savefig, clf, plt


class Latex:
    def __init__(self):
        pass

    def plot_graph(self, fig):
        fig.canvas.set_window_title('Window 3D')

    def create_table(self):
        pass

    def create_diagram(self):
        fig_width_pt = 246.0  # Get this from LaTeX using \showthe\columnwidth
        inches_per_pt = 1.0 / 72.27  # Convert pt to inch
        golden_mean = (sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
        fig_width = fig_width_pt * inches_per_pt  # width in inches
        fig_height = fig_width * golden_mean  # height in inches
        fig_size = [fig_width, fig_height]
        params = {'backend': 'ps',
                  'axes.labelsize': 10,
                  'text.fontsize': 10,
                  'legend.fontsize': 10,
                  'xtick.labelsize': 8,
                  'ytick.labelsize': 8,
                  'text.usetex': False,
                  'figure.figsize': fig_size}
        pylab.rcParams.update(params)
        # Generate data
        x = pylab.arange(-2 * pi, 2 * pi, 0.01)
        y1 = x
        y2 = x+2
        # Plot data
        # Plot data
        pylab.figure(1)
        pylab.clf()
        pylab.axes([0.125, 0.2, 0.95 - 0.125, 0.95 - 0.2])
        pylab.plot(x, y1, 'g:', label='sin(x)')
        pylab.plot(x, y2, '-b', label='cos(x)')
        pylab.xlabel('x (radians)')
        pylab.ylabel('y')
        font = FontProperties(size='x-small');
        pylab.legend(loc=0, prop=font);
        #pylab.legend()

        # parent_path = os.path.abspath(os.path.join("../statistics/", os.pardir))
        # pylab.savefig(parent_path + '/statistics/latex/fig.eps')

        # x, y = meshgrid(*(linspace(-1, 1, 500),) * 2)
        # z = sin(20 * x ** 2) * cos(30 * y)
        # c = contourf(x, y, z, 50)
        # savefig('full_vector.pdf')
        # clf()
        # c = contourf(x, y, z, 50, rasterized=True)
        # savefig('rasterized.pdf')

        return pylab.figure(1)