# Basic kinematic fiducial cuts, use only variables available in real data.
#
# m.mieskolainen@imperial.ac.uk, 2022

import awkward as ak
import numpy as np
import numba
import matplotlib.pyplot as plt

from icenet.tools import stx

def cut_nocut(X, xcorr_flow=False):
    """ No cuts
    """
    return ak.Array(np.ones(len(X), dtype=np.bool_)) # Note datatype np.bool_

def cut_fiducial(X, xcorr_flow=False):
    """ Basic fiducial (kinematic) selections.
    
    Args:
        X:          Awkward jagged array
        xcorr_flow: cut N-point cross-correlations
    
    Returns:
        Passing indices mask (N)
    """
    global O; O = X  # __technical__ recast due to eval() scope
    
    N = len(O)

    # Global cuts
    # Create cut strings
    names_global = ['O.nJet > 1']
    cuts_global = [eval(name, globals()) for name in names_global]
    mask_global = stx.apply_cutflow(cut=cuts_global, names=names_global, xcorr_flow=xcorr_flow)

    # Jet cuts
    # Create cut strings
    cut_pt = np.zeros(N, dtype=bool)
    cut_eta = np.zeros(N, dtype=bool)
    cut_pt[mask_global] = np.logical_and(O.Jet.pt[mask_global, 0] > 30.0, O.Jet.pt[mask_global, 1] > 30.0)
    cut_eta[mask_global] = np.logical_and(np.abs(O.Jet.eta[mask_global, 0]) < 2.5, np.abs(O.Jet.eta[mask_global, 1]) < 2.5)

    names_jet = ['Jet pT cut', 'Jet eta cut']
    cuts_jet = [cut_pt, cut_eta]
    mask_jet  = stx.apply_cutflow(cut=cuts_jet, names=names_jet, xcorr_flow=xcorr_flow)

    return np.logical_and(mask_global, mask_jet)