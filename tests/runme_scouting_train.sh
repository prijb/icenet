#!/bin/sh
#
# Execute training and evaluation for the Scouting analysis
#
# Run with: source tests/runme_scouting_train.sh

# Remember to execute first: runme_scouting_init_yaml.sh (only once, and just once)

#eval "$(/vols/cms/pb4918/miniforge3/bin/conda shell.bash hook)"
conda activate icenet

ICEPATH="/home/pb4918/Physics/Projects/HLTScouting/ML/Feb26/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

CONFIG="tune0.yml"
DATAPATH="/home/pb4918/Physics/Projects/HLTScouting/ML/Samples"

CONDITIONAL=0
MAX=10000000    # Tune according to maximum CPU RAM available


python analysis/scouting.py --runmode genesis --num_cpus 1 --maxevents $MAX --inputmap mc_map__scenarioA.yml --config $CONFIG --datapath $DATAPATH --use_cache 0
python analysis/scouting.py --runmode train --num_cpus 1 --maxevents $MAX --inputmap mc_map__scenarioA.yml --modeltag scenarioA --config $CONFIG --datapath $DATAPATH 
python analysis/scouting.py --runmode eval --num_cpus 1 --maxevents $MAX --inputmap mc_map__scenarioA.yml --modeltag scenarioA --config $CONFIG --datapath $DATAPATH 