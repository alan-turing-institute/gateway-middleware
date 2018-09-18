#!/bin/bash

echo "INFO: stop.sh"

set -o xtrace

SIMULATE="Simulate"
STATE="$SIMULATE/state"

PBS_JOB_ID=$(cat $STATE/pbs_job_id)
qdel $PBS_JOB_ID
