#!/bin/bash

echo "INFO: Start store"

set -o xtrace

SIMULATE="Simulate"
STATE="$SIMULATE/state"
CONFIG="$STATE/store.json"
JOB_ID=$(cat $STATE/job_id)


JOB_STORAGE_TOKEN=$(cat $CONFIG | jq -r '.data.token')
ACCOUNT=$(cat $CONFIG | jq -r '.data.account')
CONTAINER=$(cat $CONFIG | jq -r '.data.container')
BLOB=$(cat $CONFIG | jq -r '.data.blob')

LOCKDIR='.lock_storage_sync'

mkdir $LOCKDIR  || {
    echo "ERROR: lock directory exists. exiting"
    exit 1
}

# remove lock directory
trap "rmdir $LOCKDIR" EXIT INT KILL TERM

# zip files to /tmp/output_<job_id>.zip
zip -r /tmp/output_${JOB_ID}.zip ./*  # TODO keep within pbs dir (i.e. mv after creation)

# transfer files to cloud storage
CMD="az storage blob upload \
--container-name $CONTAINER \
--file /tmp/output_${JOB_ID}.zip \
--account-name $ACCOUNT \
--sas-token '$JOB_STORAGE_TOKEN' \
--name '$BLOB' "

# HACK wrap command in bash (otherwise not working)
echo $CMD > $STATE/store_cmd.sh
bash $STATE/store_cmd.sh | tee $STATE/log.store_cmd

echo "INFO: End store"
