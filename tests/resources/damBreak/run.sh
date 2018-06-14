#!/bin/bash

cd ${0%/*} || exit 1    # Run from this directory

# create a file named `pbs_job_id`
# which contains the pbs id (example: "5309476.cx1b")
# use `tee` to retain stdout

qsub -o /tmp/logstdout.txt -e /tmp/logerr.txt  pbs.sh | tee pbs_job_id

echo "Submitted job"
