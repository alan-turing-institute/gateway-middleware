#!/bin/bash

JOB_ID=$(cat job_id)
JOB_STORAGE_TOKEN=$(cat /tmp/output_token.txt | jq -r '.data.token')
PBS_JOB_ID=$(cat pbs_job_id)

ACCOUNT=$(cat /tmp/output_token.txt | jq -r '.data.account')
CONTAINER=$(cat /tmp/output_token.txt | jq -r '.data.container')


lockdir='.lock_storage_sync'

mkdir $lockdir  || {
    echo "lock directory exists. exiting"
    exit 1
}

# remove lock directory
trap "rmdir $lockdir" EXIT INT KILL TERM

# transfer files to cloud storage
az storage blob upload --container-name $CONTAINER --file ./output.zip --account-name $ACCOUNT --sas-token $JOB_STORAGE_TOKEN --name $JOB_ID/output.txt

#/home/vm-admin/miniconda/bin/blobxfer upload \
#    --sas "$JOB_STORAGE_TOKEN" \
#    --storage-account $ACCOUNT \
#    --remote-path $CONTAINER/$JOB_ID \
#    --local-path . \
#    --no-overwrite \
#    --recursive

# fine-grained control over overwrite decision
#--skip-on-filesize-match
#--skip-on-lmt-ge  (most approriate?)
#--skip-on-md5-match
