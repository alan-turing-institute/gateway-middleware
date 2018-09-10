#!/bin/bash

echo "INFO: Start metrics"

set -o xtrace

SIMULATE="Simulate"
STATE="$SIMULATE/state"
CONFIG="$STATE/store.json"
JOB_ID=$(cat $STATE/job_id)

FNAME="metrics.json"

JOB_STORAGE_TOKEN=$(cat $CONFIG | jq -r '.data.token')
ACCOUNT=$(cat $CONFIG | jq -r '.data.account')
CONTAINER=$(cat $CONFIG | jq -r '.data.container')
BLOB="$JOB_ID/$FNAME"

# LOCKDIR='.lock_storage_sync'

# mkdir $LOCKDIR  || {
#     echo "ERROR: lock directory exists. exiting"
#     exit 1
# }

# # remove lock directory
# trap "rmdir $LOCKDIR" EXIT INT KILL TERM

# transfer files to cloud storage
CMD="az storage blob upload \
--container-name $CONTAINER \
--file $FNAME \
--account-name $ACCOUNT \
--sas-token '$JOB_STORAGE_TOKEN' \
--name '$BLOB' "




# HACK wrap command in bash (otherwise not working)
echo $CMD > $STATE/metrics_cmd.sh
bash $STATE/metrics_cmd.sh | tee $STATE/log.metrics_cmd

echo "INFO: End metrics"
