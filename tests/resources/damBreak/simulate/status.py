import requests
import json

from .config import CONFIG, ENDPOINTS

STATUS_URL = f"{ENDPOINTS['MANAGER_URL']}/job/{CONFIG['JOB_ID']}/status"


def update_status(status: str):
    res = requests.patch(STATUS_URL, json={"status": status})
    if res.status_code == 200:
        print(f"INFO: Updated job status to {status}.")

    if status == "FINALIZING":
        data = res.json().get("data")
        with open("simulate/state/store.json", "w") as f:
            json.dump(data, f)

        sas_token = data.get("token")
        return sas_token
    else:
        return None
