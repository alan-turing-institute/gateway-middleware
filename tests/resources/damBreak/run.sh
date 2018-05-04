#!/bin/bash

cd ${0%/*} || exit 1    # Run from this directory

# create a file named `pbs_job_id`
# which contains the pbs id (example: "5309476.cx1b")
# use `tee` to retain stdout
echo 'echo hello world > /tmp/hello.txt' > say_hello.sh
chmod a+x say_hello.sh
qsub -o /tmp/log1.txt -e /tmp/log2.txt say_hello.sh
echo "Did test hello"

qsub -o /tmp/logstdout.txt -e /tmp/logerr.txt  pbs.sh | tee pbs_job_id

jobid=`cat job_id`
echo "url is http://job-manager:5001/job/$jobid/status"
curl -X PATCH http://job-manager:5001/job/$jobid/status --data '{"job_status" : "QUEUED"}' -H "Content-type: application/json"
