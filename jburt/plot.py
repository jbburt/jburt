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


def relative_luminance(rgb):
    # rgb = (r, g, b), where each element in [0, 255]
    def _transf(x):
        if x <= 10:
            return x / 3294.
        return (x / 269 + 0.0513) ** 2.4

    Rg, Gg, Bg = map(_transf, rgb)

    return 0.2126 * Rg + 0.7152 * Gg + 0.0722 * Bg


def contrast_ratio(rgb):
    # relative to white
    # \equiv (L1 + 0.05) / (L2 + 0.05)
    return 1.05 / (relative_luminance(rgb) + 0.05)


def unique_color_cmap(n, cmap='hsv'):
    """
    Return a function that maps each index in 0, ... n-1 to a unique color.

    Parameters
    ----------
    n : int
        number of unique colors
    cmap : str
        colormap name

    Returns
    -------
    callable
        matplotlib.colors.ScalarMappable object

    """
    import matplotlib.cm as cmx
    import matplotlib.colors as colors

    color_norm = colors.Normalize(vmin=0, vmax=n - 1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap=cmap)

    def map_index_to_rgb_color(index):
        """Generate cmx.ScalarMappable from integer index to unique color. """
        return scalar_map.to_rgba(index)

    return map_index_to_rgb_color


def generate_colors(cmap='Spectral', i=0, n=8):
    return plt.get_cmap(cmap)(i / float(n))


def adjust_luminosity(color, amount=0.75):
    """
    Adjust luminosity of a color.

    Source: https://stackoverflow.com/a/49601444/6447032

    Parameters
    ----------
    color : str or tuple
        hex string, matplotlib color string, or rgb tuple
    amount : float
        amount of adjustment; values above (below) 1 lighten (darken) color

    Returns
    -------
    str
        adjusted color as a hex string

    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    # noinspection PyTypeChecker
    tmp = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    return mc.rgb2hex(tmp)


def mix_colors(fc, bc, fc_alpha=0.5):
    """
    Combine two semi-transparent colors.

    Source: https://stackoverflow.com/a/34096666

    Parameters
    ----------
    fc : list[float]
        foreground color [r,g,b]
    bc : list[float]
        background color [r,g,b]
    fc_alpha : float, default 0.5
        alpha (transparency) of foreground color

    Returns
    -------
    list[float]
        [r,g,b,a] of the color produced by overlapping `cf` and `cb`

    """

    assert len(fc) == len(bc) == 3
    fc = list(fc) + [fc_alpha]
    bc = list(bc) + [1]
    a = bc[-1] + fc[-1] - bc[-1] * fc[-1]  # fixed alpha calculation
    r = (fc[0] * fc[-1] + bc[0] * bc[-1] * (1 - fc[-1])) / a
    g = (fc[1] * fc[-1] + bc[1] * bc[-1] * (1 - fc[-1])) / a
    b = (fc[2] * fc[-1] + bc[2] * bc[-1] * (1 - fc[-1])) / a
    return [r, g, b, a]


def rgb2hex(rgb: list, keep_alpha=False) -> str:
    return clrs.to_hex(rgb, keep_alpha=keep_alpha)


def hex2rgb(color: str):
    return clrs.to_rgb(color)


def n_hex_colors(N: int) -> list[str]:
    return [rgb2hex(generate_colors(DEFAULT_CMAP, i, N)) for i in range(N)]
