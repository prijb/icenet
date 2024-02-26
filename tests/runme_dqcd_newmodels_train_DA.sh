#!/bin/sh
#
# Execute training and evaluation for the DQCD analysis
#
# Remember to execute first: runme_dqcd_vector_init_yaml.sh (only once, and just once)

source $HOME/setconda.sh
conda activate icenet

ICEPATH="/vols/cms/pb4918/icenet_v3/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

CONFIG="tune0_new_scouting.yml"
DATAPATH="/vols/cms/pb4918"

CONDITIONAL=0
MAX=2000000    # Tune according to maximum CPU RAM available

python analysis/dqcd.py --runmode genesis  --maxevents $MAX --inputmap mc_map__scenarioA_all_DA.yml --config $CONFIG --datapath $DATAPATH
python analysis/dqcd.py --runmode train    --maxevents $MAX --inputmap mc_map__scenarioA_all_DA.yml --modeltag scenarioA_all_DA --config $CONFIG --datapath $DATAPATH --use_conditional $CONDITIONAL
python analysis/dqcd.py --runmode eval     --maxevents $MAX --inputmap mc_map__scenarioA_all_DA.yml --modeltag scenarioA_all_DA --config $CONFIG --datapath $DATAPATH --use_conditional $CONDITIONAL
#python analysis/dqcd.py --runmode optimize --maxevents $MAX --inputmap mc_map__scenarioA_all_DA.yml --modeltag scenarioA_all_DA --config $CONFIG --datapath $DATAPATH --use_conditional $CONDITIONAL
