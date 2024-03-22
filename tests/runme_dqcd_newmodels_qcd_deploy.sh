#!/bin/sh
#
# Execute distributed deployment for the DQCD analysis
# Run with: source runme.sh

# Remember to execute first: runme_dqcd_newmodels_init_yaml.sh (only once, and just once)

source $HOME/setconda.sh
conda activate icenet

ICEPATH="/vols/cms/pb4918/icenet_singlebdt/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

CONFIG="tune0_new_scouting.yml"
DATAPATH="/vols/cms/pb4918"
CONDITIONAL=0

python analysis/dqcd_deploy.py --runmode deploy --use_conditional $CONDITIONAL --inputmap 'include/QCD_new_deploy.yml' --modeltag scenarioA_all_DA --grid_id $GRID_ID --grid_nodes $GRID_NODES --config $CONFIG --datapath $DATAPATH
