#!/bin/sh
#
# Generate dynamic YAML files
#
# Use * or other glob wildcards for filenames
#
# Run with: source runme.sh
# This is for scouting

source $HOME/setconda.sh
conda activate icenet

ICEPATH="/vols/cms/pb4918/icenet_v3/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

# Training
python configs/dqcd/include/ymlgen_scouting.py --process 'QCD'       --filerange '[0-100]' --outputfile configs/dqcd/include/QCD_newmodels.yml
python configs/dqcd/include/ymlgen_scouting.py --process 'scenarioA' --filerange '[0-60]' --outputfile configs/dqcd/include/scenarioA.yml

# Training (Domain Adaptation)
python configs/dqcd/include/ymlgen_scouting.py --process 'data'    --filerange '[0-20]'  --outputfile configs/dqcd/include/data_DA.yml

# Deployment
python configs/dqcd/include/ymlgen_scouting.py --process 'QCD'       --filerange '[101-100000]' --outputfile configs/dqcd/include/QCD_newmodels_deploy.yml
python configs/dqcd/include/ymlgen_scouting.py --process 'scenarioA' --filerange '[21-100000]' --outputfile configs/dqcd/include/scenarioA_deploy.yml
