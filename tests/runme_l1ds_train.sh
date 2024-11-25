#!/bin/sh
eval "$(/vols/cms/pb4918/miniforge3/bin/conda shell.bash hook)"
conda activate icenet
ICEPATH="/vols/cms/pb4918/icenet_l1ds/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

#Setting a temporary RAY DIR for local debugging
#export RAY_TMPDIR=/home/pb4918/tmp

CONFIG="tune0.yml"
DATAPATH="/vols/cms/pb4918/StoreNTuple/L1Scouting/Icenet"
#DATAPATH="/home/pb4918/Physics/Projects/L1Scouting/Icenet/TestStash"

MAX=10000000 

python analysis/l1ds.py --runmode genesis --num_cpus 1 --maxevents $MAX --inputmap mc_map__ztoqq.yml --config $CONFIG --datapath $DATAPATH --use_cache 1
python analysis/l1ds.py --runmode train --num_cpus 1 --maxevents $MAX --inputmap mc_map__ztoqq.yml --modeltag ztoqq --config $CONFIG --datapath $DATAPATH 
python analysis/l1ds.py --runmode eval --num_cpus 1 --maxevents $MAX --inputmap mc_map__ztoqq.yml --modeltag ztoqq --config $CONFIG --datapath $DATAPATH 

