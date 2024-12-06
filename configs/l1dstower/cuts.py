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
    names_global = ['O.nL1Jet > 1']
    cuts_global = [eval(name, globals()) for name in names_global]
    mask_global = stx.apply_cutflow(cut=cuts_global, names=names_global, xcorr_flow=xcorr_flow)

    # Jet cuts
    # Create cut strings
    cut_saturated = np.zeros(N, dtype=bool)
    cut_pt = np.zeros(N, dtype=bool)
    cut_eta = np.zeros(N, dtype=bool)
    cut_saturated[mask_global] = ak.sum(O.L1Jet.pt[mask_global] == 1023.5, -1) == 0
    cut_pt[mask_global] = np.logical_and(O.L1Jet.pt[mask_global, 0] > 30.0, O.L1Jet.pt[mask_global, 1] > 30.0)
    cut_eta[mask_global] = np.logical_and(np.abs(O.L1Jet.eta[mask_global, 0]) < 2.5, np.abs(O.L1Jet.eta[mask_global, 1]) < 2.5)
    names_jet = ['Saturated jet cut', 'Jet pT cut', 'Jet eta cut']
    cuts_jet = [cut_saturated, cut_pt, cut_eta]
    mask_jet  = stx.apply_cutflow(cut=cuts_jet, names=names_jet, xcorr_flow=xcorr_flow)

    return np.logical_and(mask_global, mask_jet)

#This saves events with at least one tower and throws away events with hot towers (iEt > 508)
def cut_tower(X, xcorr_flow=False):
    """ Tower cuts
    """
    global O; O = X  # __technical__ recast due to eval() scope
    
    N = len(O)

    # Global cuts
    # Create cut strings
    names_global = ['O.nL1EmulCaloTower > 0']
    cuts_global = [eval(name, globals()) for name in names_global]
    mask_global = stx.apply_cutflow(cut=cuts_global, names=names_global, xcorr_flow=xcorr_flow)

    # Tower cuts
    # Create cut strings
    cut_hot = np.zeros(N, dtype=bool)
    cut_hot[mask_global] = ak.sum(O.L1EmulCaloTower.iet[mask_global] > 508, -1) == 0
    names_tower = ['Hot tower cut']
    cuts_tower = [cut_hot]
    mask_tower  = stx.apply_cutflow(cut=cuts_tower, names=names_tower, xcorr_flow=xcorr_flow)

    return np.logical_and(mask_global, mask_tower)

#This saves events with at least one jet and throws away events with saturated jets (pt = 1023.5)
def cut_jet(X, xcorr_flow=False):
    """ Jet cuts
    """
    global O; O = X  # __technical__ recast due to eval() scope
    
    N = len(O)

    # Global cuts
    # Create cut strings
    names_global = ['O.nL1Jet > 0']
    cuts_global = [eval(name, globals()) for name in names_global]
    mask_global = stx.apply_cutflow(cut=cuts_global, names=names_global, xcorr_flow=xcorr_flow)

    # Jet cuts
    # Create cut strings
    cut_saturated = np.zeros(N, dtype=bool)
    cut_saturated[mask_global] = ak.sum(O.L1Jet.pt[mask_global] == 1023.5, -1) == 0
    names_jet = ['Saturated jet cut']
    cuts_jet = [cut_saturated]
    mask_jet  = stx.apply_cutflow(cut=cuts_jet, names=names_jet, xcorr_flow=xcorr_flow)

    return np.logical_and(mask_global, mask_jet)


