#!/bin/bash





echo "Start PBS"

# kill all child processes on exit
# note: this is likely handled automatically by the schedular
trap "exit" INT TERM
trap "kill 0" EXIT

set -vx

# emulate running in TMPDIR 
TMPDIR="/tmp/pbs.$PBS_JOBID"

echo $TMPDIR

mkdir -p $TMPDIR

cp -r $PBS_O_WORKDIR/* $TMPDIR  # TODO explicitly copy only required files
cd $TMPDIR

jobid=`cat job_id`

# update status in job-manager to RUNNING
curl -X PATCH http://job-manager:5001/job/$jobid/status --data '{"job_status" : "RUNNING"}' -H "Content-type: application/json"

# set env vars for openfoam
source /opt/openfoam5/etc/bashrc
# run simulation
chmod a+x Allrun
./Allrun

sleep 20
# update job status to FINALIZING - this will get us some json containing Azure
# details (account name, container name, SAS token) which we put in a txt file.
curl -X PATCH http://job-manager:5001/job/$jobid/status --data '{"job_status" : "FINALIZING"}' -H "Content-type: application/json" | tee output_token.txt

# Run the storage script, giving it the current directory as an argument
STORAGE_SCRIPT="${TMPDIR}/store_output_azure.sh"
chmod u+x $STORAGE_SCRIPT
echo "Calling $STORAGE_SCRIPT $TMPDIR"
$STORAGE_SCRIPT $TMPDIR

sleep 20

# update job status to COMPLETED
curl -X PATCH http://job-manager:5001/job/$jobid/status --data '{"job_status" : "COMPLETED"}' -H "Content-type: application/json" 

echo "End PBS"
