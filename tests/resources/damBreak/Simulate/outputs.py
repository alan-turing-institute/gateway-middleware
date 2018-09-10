#!/usr/bin/env python

import requests
import json

fname = "Simulate/state/job_id"
with open(fname, "r") as f:
    job_id = f.readline()

url = f"http://manager:5001/job/{job_id}/output"

payload = {
    "outputs": [
        {
            "destination": f"https://simulate.blob.core.windows.net/openfoam-test-output/{job_id}/metrics.json",
            "type": "metrics",
            "name": "metrics",
            "label": "Metrics (json)",
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    # 'Authorization': "Bearer fooToken",
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)
