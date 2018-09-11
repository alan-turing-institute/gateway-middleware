#!/usr/bin/env python

# Example output
# output = {
#     "labels": ["Time"],
#     "names": ["time"],
#     "units": ["s"],
#     "metrics": {
#         "time": [0.00119048, 0.00258503, 0.00422003, 0.00612753, 0.00832115, 0.0109261]
#     },
# }

import subprocess

import json
import numpy as np

subprocess.call("foamLog -n -quiet log.icoFoam", shell=True)

selection_list = [
    {"fpath": "logs/Time_0", "label": "Time", "name": "time", "units": "s"},
    {
        "fpath": "logs/CourantMax_0",
        "label": "Courant Max",
        "name": "courantMax_0",
        "units": "",
    },
]

output = {"labels": [], "names": [], "units": [], "metrics": {}}
for selection in selection_list:
    fpath = selection["fpath"]
    label = selection["label"]
    name = selection["name"]
    units = selection["units"]

    data = np.loadtxt(fpath).tolist()
    output["metrics"][name] = data
    output["labels"].append(label)
    output["names"].append(name)
    output["units"].append(units)


with open("metrics.json", "w") as f:
    json.dump(output, f)
