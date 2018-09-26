#!/bin/bash

SIMULATE="simulate"
STATE="$SIMULATE/state"

# save PBS_JOBID in state file via tee
qsub -o log.qsub.stdout -e log.qsub.stderr pbs.sh | tee $STATE/pbs_job_id

echo "Submitted job"
