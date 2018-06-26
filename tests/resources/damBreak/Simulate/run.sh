#!/bin/bash

MANAGER="Simulate"

# save PBS_JOBID in state file via tee
qsub -o $MANAGER/log.qsub.stdout -e $MANAGER/log.qsub.stderr $MANAGER/pbs.sh | tee $MANAGER/log.run

echo "Submitted job"
