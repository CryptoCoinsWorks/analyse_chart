import pandas as pd
import numpy as np
from scipy import signal
from pprint import pprint

def zig_zag(values, distance=2.1):
    peaks_up, _ = signal.find_peaks(values, prominence=1, distance=distance)
    peaks_down, _ = signal.find_peaks(-values, prominence=1, distance=distance)

    indexs = [i for i in peaks_up]
    indexs.extend([i for i in peaks_down])
    indexs.sort()

    return indexs