import pathlib

import matplotlib
from matplotlib import image as mpimg
from matplotlib import pyplot as plt

from .typing import PathLike


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
