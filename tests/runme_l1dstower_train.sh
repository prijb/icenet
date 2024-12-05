#!/bin/sh

#lx04 version
#eval "$(/vols/cms/pb4918/miniforge3/bin/conda shell.bash hook)"
#conda activate icenet
#ICEPATH="/vols/cms/pb4918/icenet_l1ds/icenet"
#cd $ICEPATH
#echo "$(pwd)"
#source $ICEPATH/setenv.sh
#DATAPATH="/vols/cms/pb4918/StoreNTuple/L1Scouting/Icenet"


#Local PC version 
conda activate icenet
ICEPATH="/home/pb4918/Physics/Projects/L1Scouting/Icenet/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh
CONFIG="tune0.yml"
DATAPATH="/home/pb4918/Physics/Projects/L1Scouting/Icenet/TestStash"

MAX=10000000 

python analysis/l1dstower.py --runmode genesis --num_cpus 4 --maxevents $MAX --inputmap mc_map__suep_local.yml --config $CONFIG --datapath $DATAPATH --use_cache 0
python analysis/l1dstower.py --runmode train --num_cpus 4 --maxevents $MAX --inputmap mc_map__suep_local.yml --modeltag suep --config $CONFIG --datapath $DATAPATH
python analysis/l1dstower.py --runmode eval --num_cpus 4 --maxevents $MAX --inputmap mc_map__suep_local.yml --modeltag suep --config $CONFIG --datapath $DATAPATH