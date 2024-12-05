# L1DS (towers) steering code

import sys
sys.path.append(".")

# Configure plotting backend
import matplotlib
matplotlib.use('Agg')

from icenet.tools import process
from icel1dstower import common

def main():
    args, runmode = process.generic_flow(rootname='l1dstower', func_loader=common.load_root_file, func_factor=common.splitfactor)


if __name__ == '__main__' :
    main()