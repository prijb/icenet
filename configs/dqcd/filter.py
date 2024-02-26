# Data filtering / triggering rules
# 
# Note! Physics observable (fiducial / kinematic) cuts are defined in cuts.py, not here.
#
# m.mieskolainen@imperial.ac.uk, 2022

import awkward as ak
import numpy as np
import numba

from icenet.tools import stx


def filter_nofilter(X, isMC=None, class_id=None, xcorr_flow=False):
    """ All pass
    """
    return ak.Array(np.ones(len(X), dtype=np.bool_)) # Note datatype np.bool_


def filter_standard(X, isMC=None, class_id=None, xcorr_flow=False):
    """ Basic filters.
    
    Args:
    	X : Awkward jagged array
    
    Returns:
        Passing indices mask (N)
    """
    global O; O = X  # __technical__ recast due to eval() scope

    names = ["O['HLT_Mu9_IP6_part0'] | "
             "O['HLT_Mu9_IP6_part1'] | "
             "O['HLT_Mu9_IP6_part2'] | "
             "O['HLT_Mu9_IP6_part3'] | "
             "O['HLT_Mu9_IP6_part4']"]

    #if isMC and class_id == 0:
    #    names += ["additional cut here"]
    #    names += ["additional cut here"]
    
    # Evaluate columnar cuts; Compute cutflow
    cuts  = [eval(names[i], globals()) for i in range(len(names))]
    mask  = stx.apply_cutflow(cut=cuts, names=names, xcorr_flow=xcorr_flow)

    return mask

# Add alternative filters here ...
def filter_scouting(X, isMC=None, class_id=None, xcorr_flow=False):
    """ Basic filters.
    
    Args:
    	X : Awkward jagged array
    
    Returns:
        Passing indices mask (N)
    """
    global O; O = X  # __technical__ recast due to eval() scope

    names = ["O['L1_DoubleMu_15_7'] | "
             "O['L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7'] | "
             "O['L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18'] | "
             "O['L1_DoubleMu4_SQ_OS_dR_Max1p2'] | "
             "O['L1_DoubleMu4p5_SQ_OS_dR_Max1p2']"]

    #if isMC and class_id == 0:
    #    names += ["additional cut here"]
    #    names += ["additional cut here"]
    
    # Evaluate columnar cuts; Compute cutflow
    cuts  = [eval(names[i], globals()) for i in range(len(names))]
    mask  = stx.apply_cutflow(cut=cuts, names=names, xcorr_flow=xcorr_flow)

    return mask
