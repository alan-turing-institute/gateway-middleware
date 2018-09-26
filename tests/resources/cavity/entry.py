import os
from pathlib import Path
from distutils.dir_util import copy_tree
import subprocess

import requests
import json


from simulate.status import update_status
from simulate.config import CONFIG, ENDPOINTS
from simulate.storage import upload, zip_dir


TMPDIR = f"/tmp/pbs.{CONFIG['PBS_JOB_ID']}"
JOB_ID = CONFIG["JOB_ID"]

print(TMPDIR)

print("INFO: Copying required job files")
copy_tree(".", TMPDIR)
os.chdir(TMPDIR)

update_status("RUNNING")
subprocess.run("python simulate/patch.py", shell=True)
subprocess.run("bash ./Allrun", shell=True)

sas_token = update_status("FINALIZING")

subprocess.run("python simulate/metrics.py", shell=True)
subprocess.run("python simulate/outputs.py", shell=True)


upload("metrics.json", sas_token=sas_token)

zip_dir("cavity.zip", ".")
upload("cavity.zip", sas_token=sas_token)

update_status("COMPLETED")
