#!/bin/bash

# create a file named `pbs_job_id`
# which contains the pbs id (example: "5309476.cx1b")
# use `tee` to retain stdout
qsub -k oe pbs.sh | tee pbs_job_id

jobid=`cat job_id`
curl -X PATCH http://job-manager:5001/job/$jobid/status --data '{"status" : "QUEUED"}' -H "Content-type: application/json"
