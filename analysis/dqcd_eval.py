# DQCD [EVALUATION] code
#
# Mikael Mieskolainen, 2022
# m.mieskolainen@imperial.ac.uk

# icenet system paths
import sys
sys.path.append(".")

# icenet
from icenet.tools import process
from icenet.tools import reweight
from icenet.tools import io

# icedqcd
from icedqcd import common
from configs.dqcd.mvavars import *

import os.path
import pickle

# Main function
#
def main() :

    args, cli      = process.read_config(config_path='./configs/dqcd')

    args_hash      = io.make_hash_sha256(args)
    cache_filename = f'./tmp/{args_hash}.data'

    if not os.path.exists(cache_filename):
        data      = io.IceTriplet(func_loader=common.load_root_file, files=args['root_files'],
                        load_args={'entry_start': 0, 'entry_stop': args['maxevents'], 'args': args},
                        class_id=[0,1], frac=args['frac'], rngseed=args['rngseed'])
        
        with open(cache_filename, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)      
    else:
        with open(cache_filename, 'rb') as handle:
            print(__name__ + f'. loading from cache file {cache_filename}')
            data = pickle.load(handle)


    ### Imputation
    #imputer   = pickle.load(open(args["modeldir"] + '/imputer.pkl', 'rb')) 
    #features  = globals()[args['imputation_param']['var']]
    #data, _   = process.impute_datasets(data=data, features=features, args=args['imputation_param'], imputer=imputer)
    

    ### Compute reweighting weights for the evaluation (before split&factor !)
    if args['eval_reweight']:
        tst_weights,_ = reweight.compute_ND_reweights(x=data.tst.x, y=data.tst.y, ids=data.ids, args=args['reweight_param'])
    else:
        tst_weights = None
    
    ### Split and factor data
    data, data_deps, data_kin = common.splitfactor(data=data, args=args)
    
    # Evaluate classifiers
    process.evaluate_models(data=data, data_kin=data_kin, data_deps=data_deps, weights=tst_weights, args=args)
    
    print(__name__ + ' [Done]')


if __name__ == '__main__' :

   main()

