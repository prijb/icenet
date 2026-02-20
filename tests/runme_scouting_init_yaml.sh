#!/bin/sh
#
# Generate dynamic YAML files
#
# Use * or other glob wildcards for filenames
#
# Run with: source tests/runme.sh

#eval "$(/vols/cms/pb4918/miniforge3/bin/conda shell.bash hook)"
conda activate icenet

ICEPATH="/home/pb4918/Physics/Projects/HLTScouting/ML/Feb26/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

# Training
python configs/scouting/include/ymlgen.py --process 'Signal_ScenarioA' --filerange '[0-50]' --outputfile configs/scouting/include/scenarioA.yml
python configs/scouting/include/ymlgen.py --process 'DileptonMinBias' --filerange '[0-100]' --outputfile configs/scouting/include/dileptonminbias.yml