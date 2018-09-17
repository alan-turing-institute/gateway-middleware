#!/bin/bash

SIMULATE="Simulate"
STATE="$SIMULATE/state"

# save PBS_JOBID in state file via tee
qsub -o $SIMULATE/log.qsub.stdout -e $SIMULATE/log.qsub.stderr $SIMULATE/pbs.sh | tee $STATE/pbs_job_id

echo "Submitted job"
