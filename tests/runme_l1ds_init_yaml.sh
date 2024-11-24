#!/bin/sh
#
# Generate YAML files for signal and MC locations
#
# Use * or other glob wildcards for filenames
#
# Run with: source tests/runme.sh

conda activate icenet

ICEPATH="/home/pb4918/Physics/Projects/L1Scouting/Icenet/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

# Training
python configs/l1ds/include/ymlgen.py --process 'QCD' --filerange '[0-20]' --outputfile configs/l1ds/include/QCD.yml
python configs/l1ds/include/ymlgen.py --process 'zprime' --filerange '[0-20]' --outputfile configs/l1ds/include/signal.yml

# Deployment
python configs/l1ds/include/ymlgen.py --process 'QCD' --filerange '[21-100000]' --outputfile configs/l1ds/include/QCD_deploy.yml
python configs/l1ds/include/ymlgen.py --process 'zprime' --filerange '[21-100000]' --outputfile configs/l1ds/include/signal_deploy.yml



