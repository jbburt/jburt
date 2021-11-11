"""
Utility functions for processing signals/waveforms.
"""

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.signal import welch

from .typing import Numeric


def fwhm_spline(waveform: np.ndarray, upsample: int = 100) -> float:
    """
    Compute full width at half-max using cubic spline interpolation.

    Parameters
    ----------
    waveform : (N,) np.ndarray
        template waveform
    upsample : int
        upsampling factor. for upsample=100 (default), the result will be at
        1/100th the resolution of samples in `waveform`

    Returns
    -------
    float
        full width at half max, in units of input samples

    """
    spline = CubicSpline(x=np.arange(waveform.size), y=waveform)
    xs = np.arange(0, waveform.size + 1. / upsample, 1. / upsample)
    waveform_upsampled = spline(xs)
    peakidx = np.abs(waveform_upsampled).argmax()

    # flip if the peak is negative
    if waveform_upsampled[peakidx] < 0:
        waveform_upsampled *= -1

    # find right-hand half max
    peakheight = np.abs(waveform_upsampled[peakidx])
    rdelta = waveform_upsampled[peakidx:] - peakheight / 2
    rwidth = np.where(rdelta < 0)[0][0]  # drops below half-max

    # find left half-max
    ldelta = waveform_upsampled[peakidx::-1] - peakheight / 2
    lwidth = np.where(ldelta < 0)[0][0]
    return (lwidth + rwidth) / upsample


def find_peak_freq(signal: np.ndarray, sfreq: Numeric,
                   nperseg: int = None, noverlap: int = None) -> float:
    """
    Find peak frequency component of a signal.

    Parameters
    ----------
    signal: (N,) np.ndarray
        signal to process
    sfreq: int
        sampling frequency
    nperseg : int, optional (default None)
        Length of each Welch segment. Defaults to 256.
    noverlap : int, optional
        Number of points to overlap between segments. If `None`,
        ``noverlap = nperseg // 2``. Defaults to `None`.

    Returns
    -------
    float
        frequency with most spectral power

    """
    freq, power = welch(
        signal, fs=sfreq, window="hann",
        nperseg=nperseg, noverlap=noverlap, scaling='spectrum'
    )
    return freq[power.argmax()]
