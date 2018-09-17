#!/usr/bin/env python

import requests
import json

fname = "Simulate/state/job_id"
with open(fname, "r") as f:
    job_id = f.readline()

fname = "Simulate/state/job_token"
with open(fname, "r") as f:
    job_token = f.readline()


url = f"http://manager:5010/job/{job_id}/output"

payload = {
    "outputs": [
        {
            "destination": f"https://simulate.blob.core.windows.net/openfoam-test-output/{job_id}/metrics.json",
            "type": "metrics",
            "name": "metrics",
            "label": "Metrics (json)",
            "filename": "metrics.json",
        },
        {
            "destination": f"https://simulate.blob.core.windows.net/openfoam-test-output/{job_id}/output.zip",
            "type": "zip",
            "name": "output",
            "label": "Output (zip)",
            "filename": "output.zip",
        },
    ]
}

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {job_token}"}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)
