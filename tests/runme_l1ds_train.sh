#!/bin/sh
source ~/.bashrc
condainit
conda activate icenet
ICEPATH="/vols/cms/pb4918/icenet_l1ds"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

CONFIG="tune0.yml"
DATAPATH="/vols/cms/pb4918"

MAX=10000000 

python analysis/l1ds.py --runmode genesis --maxevents $MAX --inputmap mc_map__ztoqq.yml --config $CONFIG --datapath $DATAPATH
