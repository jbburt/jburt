import pathlib

import numpy as np
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .types import Numeric
from .types import PathLike


def aggregate(root_dir: PathLike, fname: str, figsize=(9, 9)):
    """
    Create multi-page PDF of all PNG files in a directory.

    Parameters
    ----------
    root_dir: str or pathlib.Path
        directory containing images; also where output is saved
    fname : str
        name of output file
    figsize: tuple
        image (width, height)

    """
    if not isinstance(root_dir, pathlib.Path):
        root_dir = pathlib.Path(root_dir)
    fout = root_dir.joinpath(fname).with_suffix('.pdf')
    files = list(root_dir.glob('*.png'))
    if not files:
        raise RuntimeError(f'no png images exist in {str(root_dir)}')
    pdf = PdfPages(str(fout))
    for file in files:
        if file.suffix not in ['.pdf', '.png']:
            continue
        fig, ax = plt.subplots(figsize=figsize)
        img = mpimg.imread(file)
        ax.imshow(img)
        ax.axis('off')
        pdf.savefig(fig)
        plt.close(fig)
    pdf.close()


def prettify_legend(leg, lw: int = 0, fc: str = 'none'):
    """
    Prettify legend.

    Parameters
    ----------
    leg: matplotlib.legend.Legend
        legend
    lw : int, optional (default 0)
        bbox line width
    fc : str, optional (default 'none')
        facecolor

    """
    leg.get_frame().set_facecolor(fc)
    leg.get_frame().set_linewidth(lw)


def jitter(xc: Numeric, yc: Numeric, r: Numeric, n: int = 1):
    """
    Use a random angle to jitter an object's anchor point.

    Parameters
    ----------
    xc : Numeric
        x center
    yc : Numeric
        y center
    r : Numeric
        radius
    n : int, optional (default 1)
        number of samples to generate

    Returns
    -------
    float or (n,) np.ndarray
        x-jittered
    float or (n,) np.ndarray
        y-jittered

    """
    theta = np.random.rand(n) * 2 * np.pi
    xd = r * np.cos(theta)
    yd = r * np.sin(theta)
    return xc + xd, yc + yd


def despine(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def detach(ax, amount=10):
    ax.spines['left'].set_position(('outward', amount))
    ax.spines['bottom'].set_position(('outward', amount))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def ticks_outward(ax):
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', direction='out')


def update_style(ax, figbg='w', axbg='#e2e2e2', textcolor='k', gridcolor='w'):
    for side in ['top', 'right', 'bottom', 'left']:
        ax.spines[side].set_visible(False)
    ax.grid(axis='both', color=gridcolor, linestyle='-', linewidth=1, alpha=0.5)
    ax.tick_params(axis='both', which='both', bottom=False, top=False,
                   left=False, right=False, labelbottom=True, length=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', colors=textcolor)
    ax.xaxis.label.set_color(textcolor)
    ax.yaxis.label.set_color(textcolor)
    ax.title.set_color(textcolor)
    ax.figure.figure.set_facecolor(figbg)
    ax.set_facecolor(axbg)
