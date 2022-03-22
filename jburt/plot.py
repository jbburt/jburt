import pathlib
from typing import Tuple
from typing import Union

import matplotlib
import numpy as np
from matplotlib import image as mpimg
from matplotlib import pyplot as plt

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
    pdf = matplotlib.backends.backend_pdf.PdfPages(str(fout))
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


def prettify_legend(leg: matplotlib.legend.Legend, lw: int = 0, fc: str = 'none'):
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


def jitter(xc: Numeric,
           yc: Numeric,
           r: Numeric,
           n: int = 1
           ) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
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
