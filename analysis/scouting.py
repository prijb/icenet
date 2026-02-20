# Scouting steering code

import sys
sys.path.append(".")

# Configure plotting backend
import matplotlib
matplotlib.use('Agg')

from icenet.tools import process
from icescouting import common

def main():
    args, runmode = process.generic_flow(rootname='scouting', func_loader=common.load_root_file, func_factor=common.splitfactor)

    # TO DO: Introduce optimization like in DQCD


if __name__ == '__main__' :
    main()