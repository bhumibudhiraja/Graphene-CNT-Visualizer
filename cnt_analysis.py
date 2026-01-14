import numpy as np
from cnt_utils import cnt_type, cnt_diameter, cnt_bandgap

def generate_cnt_data(n_max=20):
    """
    Generate CNT data for many (n,m) combinations.
    Returns lists: diameter, bandgap, type, (n,m)
    """
    diameters = []
    bandgaps = []
    types = []
    labels = []

    for n in range(1, n_max + 1):
        for m in range(0, n + 1):  # m <= n
            ttype = cnt_type(n, m)
            d = cnt_diameter(n, m)
            Eg = cnt_bandgap(n, m)

            diameters.append(d)
            bandgaps.append(Eg)
            types.append(ttype)
            labels.append((n, m))

    return np.array(diameters), np.array(bandgaps), np.array(types), labels
