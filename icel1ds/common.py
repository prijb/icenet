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
        for i, subproc_key in enumerate(proc):
            print(f"Subproc {subproc_key}")
            subproc = proc[subproc_key]
            dataset = subproc['path'] + '/' + subproc['files']
            print("Subproc")
            print(subproc)
            print("Dataset")
            print(dataset)
            fnames = io.glob_expand_files(datasets=dataset, datapath=root_path)
            print("Reading from:")
            print(fnames)
        #Debug stop

        #X[key], Y[key], W[key], _, INFO[key] = iceroot.read_multiple(class_id=class_id,
        #    process_func=process_root, processes=proc, root_path=root_path, param=param,
        #    num_cpus=args['num_cpus'])

    return {'X':X, 'Y':Y, 'W':W, 'ids': ak.fields(X), 'info': INFO}


def process_root(X, args, ids=None, isMC=None, return_mask=False, class_id=None, **kwargs):
    """
    Apply selections to the data
    """
    stats = {'filterfunc': None, 'cutfunc': None}

    X_final = copy.deepcopy(X)
    ids = copy.deepcopy(ids)

    #Pass through
    return X_final, ids, stats
