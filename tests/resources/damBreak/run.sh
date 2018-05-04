#!/bin/bash

cd ${0%/*} || exit 1    # Run from this directory

# create a file named `pbs_job_id`
# which contains the pbs id (example: "5309476.cx1b")
# use `tee` to retain stdout
qsub -k oe pbs.sh | tee pbs_job_id

jobid=`cat job_id`
echo "url is http://job-manager:5001/job/$jobid/status"
curl -X PATCH http://job-manager:5001/job/$jobid/status --data '{"job_status" : "QUEUED"}' -H "Content-type: application/json"
