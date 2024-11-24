#!/bin/sh
#
# Generate YAML files for signal and MC locations
#
# Use * or other glob wildcards for filenames
#
# Run with: source tests/runme.sh
eval "$(/vols/cms/pb4918/miniforge3/bin/conda shell.bash hook)"
conda activate icenet

ICEPATH="/vols/cms/pb4918/icenet_l1ds/icenet"
cd $ICEPATH
echo "$(pwd)"
source $ICEPATH/setenv.sh

# Training
python configs/l1ds/include/ymlgen.py --process 'QCD' --filerange '[0-20]' --outputfile configs/l1ds/include/QCD.yml
python configs/l1ds/include/ymlgen.py --process 'zprime' --filerange '[0-20]' --outputfile configs/l1ds/include/signal.yml

# Deployment
python configs/l1ds/include/ymlgen.py --process 'QCD' --filerange '[21-100000]' --outputfile configs/l1ds/include/QCD_deploy.yml
python configs/l1ds/include/ymlgen.py --process 'zprime' --filerange '[21-100000]' --outputfile configs/l1ds/include/signal_deploy.yml



