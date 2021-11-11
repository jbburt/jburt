"""
Functions for filtering signals.
"""

from scipy.signal import butter
from scipy.signal import lfilter


def _butter_iir_coeffs(cutoff, fs, btype, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = _butter_iir_coeffs(cutoff, fs, btype='low', order=order)
    y = lfilter(b, a, data)
    return y


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = _butter_iir_coeffs(cutoff, fs, btype='high', order=order)
    y = lfilter(b, a, data)
    return y
