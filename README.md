Skimmed down version of Icenet repository with retention of parts for JPsi fitting used for EXO-24-008 and EXO-24-016 

For the full repository including modules for ML training and inference, refer to:

https://github.com/mieskolainen/icenet

## Setup 

Clone the repo 
```
git clone git@github.com:prijb/icenet.git -b tnp_fit 
cd icenet
```

Dependencies are installed as follows
```
conda env create -f environment.yml
```

Initialise env
```
conda activate icenet_fit
source setenv.sh
```

## Running the fitter

The fitter takes histograms produced in the format of the output from the [Spark TnP](https://gitlab.cern.ch/cms-muonPOG/spark_tnp) `tnp_fitter flatten` script. Fitting is configured using yml files with `configs/peakfit/tune_scouting.yml` as an example.

Fits are run using `icefit/peakfit.py` with an example command as follows
```
python icefit/peakfit.py --analyze --group --inputfile configs/peakfit/tune_scouting.yml
```

Function defintions and the actual fitting are implemented in `icefit/icepeak.py` while `icefit/peakfit.py` performs file reading and job execution.

