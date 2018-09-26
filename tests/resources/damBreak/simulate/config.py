CONFIG_FILES = {
    "JOB_ID": "simulate/state/job_id",
    "JOB_TOKEN": "simulate/state/job_token",
    "PBS_JOB_ID": "simulate/state/pbs_job_id",
}


def read_config(files: dict):
    config = {}
    for name, fpath in files.items():
        with open(fpath, "r") as f:
            content = f.readline()
            config[name] = content.rstrip()
    return config


CONFIG = read_config(CONFIG_FILES)
ENDPOINTS = {"MANAGER_URL": "http://manager:5010"}
