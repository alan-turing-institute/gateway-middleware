#!/bin/bash

echo "INFO: Activating base conda environment"
. /opt/conda/etc/profile.d/conda.sh
conda activate base

echo "INFO: Activating openfoam5 environment"
export TERM=xterm
source /opt/openfoam5/etc/bashrc

echo "INFO: Calling main.py from $PBS_O_WORKDIR"

cd $PBS_O_WORKDIR
python entry.py