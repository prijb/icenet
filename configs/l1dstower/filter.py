# Data filtering / triggering rules
#
# Note! Physics observable (fiducial / kinematic) cuts are defined in cuts.py, not here.
#
#

import awkward as ak
import numpy as np
import numba

from icenet.tools import stx

def filter_nofilter(X, isMC=None, class_id=None, xcorr_flow=False):
    """ All pass
    """
    return ak.Array(np.ones(len(X), dtype=np.bool_)) # Note datatype np.bool_