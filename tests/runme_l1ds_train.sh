#!/bin/sh
#source ~/.bashrc
#condainit
conda activate icenet
#ICEPATH="/vols/cms/pb4918/icenet_l1ds"
#ICEPATH="/home/pb4918/Physics/Projects/L1Scouting/Icenet/icenet"
ICEPATH="."
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

#Setting a temporary RAY DIR for local debugging
export RAY_TMPDIR=/home/pb4918/tmp

CONFIG="tune0.yml"
#DATAPATH="/vols/cms/pb4918"
DATAPATH="/home/pb4918/Physics/Projects/L1Scouting/Icenet/TestStash"

MAX=10000000 

python analysis/l1ds.py --runmode genesis --maxevents $MAX --inputmap mc_map__ztoqq_local.yml --config $CONFIG --datapath $DATAPATH --use_cache 0
python analysis/l1ds.py --runmode train --maxevents $MAX --inputmap mc_map__ztoqq_local.yml --modeltag ztoqq_local --config $CONFIG --datapath $DATAPATH 

