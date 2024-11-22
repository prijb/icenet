# Common input and data reading routines for L1DS

import numpy as np
import copy
import os

import ray
from tqdm import tqdm

import time
import multiprocessing
from importlib import import_module

from icenet.tools import io, aux, prints, iceroot
from icenet.algo import analytic
from icefit import dequantize
import awkward as ak

# ------------------------------------------
from icenet import print
# ------------------------------------------

# GLOBALS
from configs.l1ds.cuts import *
from configs.l1ds.filter import *

def load_root_file(root_path, ids=None, entry_start=0, entry_stop=None, maxevents=None, args=None):
    """ Loads the root files
    
    Args:
        root_path: path to root files
    
    Returns:
        X:     jagged columnar data
        Y:     class labels
        W:     event weights
        ids:   columnar variables string (list)
        info:  trigger, MC xs, pre-selection acceptance x efficiency information (dict)
    """

    #Debug
    print("\nInput YAML")
    print(args)
    #Debug stop

    inputvars = import_module("configs." + args["rootname"] + "." + args["inputvars"])

    if type(root_path) is list:
        root_path = root_path[0] # Remove [] list
    
    # -----------------------------------------------

    param = {
        "tree":        "scNtuplizer/Events",
        "entry_start": entry_start,
        "entry_stop":  entry_stop,
        "maxevents":   maxevents,
        "args":        args,
        "load_ids":    inputvars.LOAD_VARS
    }

    INFO = {}
    X = {}
    Y = {}
    W = {}

    # =================================================================

    #Input from the mc_input.yml file
    for key in args["input"].keys():
        class_id = int(key.split("_")[1])
        proc     = args["input"][key]

        #Debug
        #print(proc)
        #Iterate over processes
        print(f"\nKey {key}")
        #for i, subproc_key in enumerate(proc):
        #    print(f"Subproc {subproc_key}")
        #    subproc = proc[subproc_key]
        #    dataset = subproc['path'] + '/' + subproc['files']
        #    print("Subproc")
        #    print(subproc)
        #    print("Dataset")
        #    print(dataset)
        #    fnames = io.glob_expand_files(datasets=dataset, datapath=root_path)
        #    print("Reading from:")
        #    print(fnames)
        #Debug stop

        X[key], Y[key], W[key], _, INFO[key] = iceroot.read_multiple(class_id=class_id,
            process_func=process_root, processes=proc, root_path=root_path, param=param,
            num_cpus=args['num_cpus'])
        
        #Debug
        #print("X:")
        #print(X[key])
        #print("Y:")
        #print(Y[key])
        #print("W:")
        #print(W[key])
        #print("INFO:")
        #print(INFO[key])
        #Debug stop

    sig_class = f"class_1" # ** HARDCODED DEFINITION **
    
    # Probability per event entry, float64 needed for precision
    # See: https://stackoverflow.com/questions/46539431/np-random-choice-probabilities-do-not-sum-to-1
    p = ak.to_numpy(W[sig_class]).squeeze().astype('float64')
    p = p / np.sum(p)

    # =================================================================
    # *** Finally combine ***
    
    X = ak.concatenate(X.values(), axis=0)
    Y = ak.concatenate(Y.values(), axis=0)
    W = ak.concatenate(W.values(), axis=0)

    # ** Crucial -- randomize order to avoid problems with other functions **
    rand = np.random.permutation(len(X))
    
    X    = X[rand]
    Y    = Y[rand]
    W    = W[rand]

    print(f'Event counts per class')
    unique, counts = np.unique(Y, return_counts=True)
    print(np.asarray((unique, counts)).T)
    

    return {'X':X, 'Y':Y, 'W':W, 'ids': ak.fields(X), 'info': INFO}


def process_root(X, args, ids=None, isMC=None, return_mask=False, class_id=None, **kwargs):
    """
    Apply selections to the data
    """

    FILTERFUNC = globals()[args['filterfunc']]    
    CUTFUNC    = globals()[args['cutfunc']]

    #Debug
    #print(f"FILTERFUNC: {FILTERFUNC}")
    #print(f"CUTFUNC: {CUTFUNC}")
    #Debug stop


    stats = {'filterfunc': None, 'cutfunc': None}

    # @@ Filtering done here @@
    fmask = FILTERFUNC(X=X, isMC=isMC, class_id=class_id, xcorr_flow=args['xcorr_flow'])
    stats['filterfunc'] = {'before': len(X), 'after': sum(fmask)}

    print(f'isMC = {isMC} | <filterfunc>  before: {len(X)}, after: {sum(fmask)} events ({sum(fmask)/(len(X)+1E-12):0.6f})', 'green')
    prints.printbar()

    X_new = X[fmask]

    # @@ Observable cut selections done here @@
    cmask = CUTFUNC(X=X_new, xcorr_flow=args['xcorr_flow'])
    stats['cutfunc'] = {'before': len(X_new), 'after': sum(cmask)}

    print(f"isMC = {isMC} | <cutfunc>     before: {len(X_new)}, after: {sum(cmask)} events ({sum(cmask)/(len(X_new)+1E-12):0.6f}) \n", 'green')
    prints.printbar()
    io.showmem()

    X_final = X_new[cmask]

    #Debug
    #print(f"nJet before cuts: {X.nJet[:10].to_list()}")
    #print(f"Jet pT before cuts: {X.Jet.pt[:10].to_list()}")
    #print(f"Jet eta before cuts: {X.Jet.eta[:10].to_list()}")
    #print("")
    #print(f"nJet after cuts: {X_final.nJet[:10].to_list()}")
    #print(f"X pT after cuts: {X_final.Jet.pt[:10].to_list()}")
    #print(f"X eta after cuts: {X_final.Jet.eta[:10].to_list()}")
    #Debug stop

    #Pass through
    #X_final = copy.deepcopy(X)
    #ids = copy.deepcopy(ids)

    if return_mask == False:
        return X_final, ids, stats
    else:
        fmask_np = fmask.to_numpy()
        fmask_np[fmask_np] = cmask # cmask is evaluated for which fmask == True
        
        return fmask_np


def splitfactor(x, y, w, ids, args, skip_graph=True, use_dequantize=True):
    """
    Transform data into different datatypes.
    
    Args:
        data:  jagged arrays
        args:  arguments dictionary
    
    Returns:
        dictionary with different data representations
    """
    inputvars = import_module("configs." + args["rootname"] + "." + args["inputvars"])
    
    data = io.IceXYW(x=x, y=y, w=w, ids=ids)

    if data.y is not None:
        data.y = ak.to_numpy(data.y).astype(np.float32)
    
    if data.w is not None:
        data.w = ak.to_numpy(data.w).astype(np.float32)

    # -------------------------------------------------------------------------

    ### Pick activate variables out
    scalar_vars = aux.process_regexp_ids(all_ids=aux.unroll_ak_fields(x=x, order='first'),  ids=eval('inputvars.' + args['inputvar_scalar']))
    jagged_vars = aux.process_regexp_ids(all_ids=aux.unroll_ak_fields(x=x, order='second'), ids=eval('inputvars.' + args['inputvar_jagged']))

    # -------------------------------------------------------------------------
    ### Pick kinematic variables out
    data_kin = None
    
    if inputvars.KINEMATIC_VARS is not None:
        
        kinematic_vars = aux.process_regexp_ids(all_ids=aux.unroll_ak_fields(x=x, order='first'),
                                                ids=inputvars.KINEMATIC_VARS)

        print(kinematic_vars)
        
        data_kin       = copy.deepcopy(data)
        data_kin.x     = aux.ak2numpy(x=data.x, fields=kinematic_vars)
        data_kin.ids   = kinematic_vars
    
    #-------------------------------------------------------------------------
    ## Tensor representation
    data_tensor = None
    
    # -------------------------------------------------------------------------
    ## Turn jagged data to a "long-vector" zero-padded matrix representation
    
    data.x, data.ids = aux.jagged_ak_to_numpy(arr=data.x, scalar_vars=scalar_vars,
                        jagged_vars=jagged_vars, jagged_maxdim=args['jagged_maxdim'],
                        null_value=args['imputation_param']['fill_value'])
    io.showmem()
    
    # -------------------------------------------------------------------------

    return {'data':        data,
            'data_MI':     None,
            'data_kin':    data_kin,
            'data_deps':   None,
            'data_tensor': None,
            'data_graph':  None}
