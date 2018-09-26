#!/usr/bin/env python

import requests
import json

from config import CONFIG, ENDPOINTS


JOB_ID = CONFIG["JOB_ID"]
OUTPUTS_URL = f"{ENDPOINTS['MANAGER_URL']}/job/{JOB_ID}/output"

payload = {
    "outputs": [
        {
            "destination": f"https://simulate.blob.core.windows.net/openfoam-test-output/{JOB_ID}/metrics.json",
            "type": "metrics",
            "name": "metrics",
            "label": "Metrics (json)",
            "filename": "metrics.json",
        },
        {
            "destination": f"https://simulate.blob.core.windows.net/openfoam-test-output/{JOB_ID}/damBreak.zip",
            "type": "zip",
            "name": "damBreak",
            "label": "damBreak (zip)",
            "filename": "damBreak.zip",
        },
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CONFIG['JOB_TOKEN']}",
}

res = requests.request("POST", OUTPUTS_URL, json=payload, headers=headers)

print("INFO: Posting new output files.")
print(res.text)
