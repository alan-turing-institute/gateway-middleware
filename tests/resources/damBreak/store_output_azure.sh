#!/bin/bash

# this script is called with the pbs tmp directory as an argument.
# Change to this dir first.

TMP_DIR=$1
cd $TMP_DIR

JOB_ID=$(cat job_id)
JOB_STORAGE_TOKEN=$(cat output_token.txt | jq -r '.data.token')
PBS_JOB_ID=$(cat pbs_job_id)

ACCOUNT=$(cat output_token.txt | jq -r '.data.account')
CONTAINER=$(cat output_token.txt | jq -r '.data.container')
BLOB=$(cat output_token.txt | jq -r '.data.blob')

lockdir='.lock_storage_sync'

mkdir $lockdir  || {
    echo "lock directory exists. exiting"
    exit 1
}

# remove lock directory
trap "rmdir $lockdir" EXIT INT KILL TERM

# zip files to /tmp/output_<job_id>.zip
zip -r /tmp/output_${JOB_ID}.zip ./*

# transfer files to cloud storage
CMD="az storage blob upload --container-name $CONTAINER --file /tmp/output_${JOB_ID}.zip --account-name $ACCOUNT --sas-token '$JOB_STORAGE_TOKEN' --name '$BLOB' "

# why does executing $CMD directly not work?  Don't know, but it doesn't!
echo $CMD > azure_cmd.sh
bash azure_cmd.sh | tee azure_output.txt


echo "Finished storage script"
