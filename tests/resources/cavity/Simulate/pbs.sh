#!/bin/bash
echo "INFO: Start PBS"

. /opt/conda/etc/profile.d/conda.sh
conda activate base

set -o xtrace

# kill all child processes on exit
# note: this is likely handled automatically by the schedular
trap "exit" INT TERM
trap "kill 0" EXIT

set -vx

TMPDIR="/tmp/pbs.$PBS_JOBID"  # emulate cluster TMPDIR

echo "INFO: Emulating computation in TMPDIR=$TMPDIR"
mkdir -p $TMPDIR

cd $TMPDIR

# copy files to temporary run dir
cp -r $PBS_O_WORKDIR/* $TMPDIR

SIMULATE="$TMPDIR/Simulate"
STATE="$SIMULATE/state"
JOB_ID=`cat $STATE/job_id`


echo $PBS_JOBID > $STATE/pbs_job_id

# update status in manager to RUNNING
curl -X PATCH http://manager:5001/job/$JOB_ID/status \
  --data '{"status" : "RUNNING"}' \
  -H "Content-type: application/json"

# set env vars for openfoam
source /opt/openfoam5/etc/bashrc
# run simulation
chmod a+x Allrun
./Allrun

# artificial delay, useful for testing front-end features
sleep 1

# update job status to FINALIZING - this will get us some json containing Azure
# details (account name, container name, SAS token) which we put in a json file.
curl -X PATCH http://manager:5001/job/$JOB_ID/status \
  --data '{"status" : "FINALIZING"}' \
  -H "Content-type: application/json" | tee $STATE/store.json


# update metrics
METRICS="$SIMULATE/metrics.py"
chmod +x $METRICS
echo "INFO: Calling $METRICS from $PWD"
$METRICS

# Run the metrics script
METRICS_SCRIPT="$SIMULATE/metrics.sh"
chmod u+x $METRICS_SCRIPT
echo "INFO: Calling $METRICS_SCRIPT"
$METRICS_SCRIPT

# Run the storage script, giving it the current directory as an argument
STORAGE_SCRIPT="$SIMULATE/store.sh"

chmod u+x $STORAGE_SCRIPT
echo "INFO: Calling $STORAGE_SCRIPT $TMPDIR"
$STORAGE_SCRIPT $TMPDIR

OUTPUTS_SCRIPT="$SIMULATE/outputs.py"
chmod u+x $OUTPUTS_SCRIPT
echo "INFO: Calling $OUTPUTS_SCRIPT"
$OUTPUTS_SCRIPT

# artificial delay, useful for testing front-end features
sleep 1

# update job status to COMPLETED
curl -X PATCH http://manager:5001/job/$JOB_ID/status \
  --data '{"status" : "COMPLETED"}' \
  -H "Content-type: application/json"

echo "INFO: End PBS"
