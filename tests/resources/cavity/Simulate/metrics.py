#!/usr/bin/env python

"""
Example output:
{
  "metadata": { "time": { "label": "Time", "units": "s" }, "courantMax_0": { "label": "Courant Max", "units": "" } },
  "data": [
    { "time": 0.005, "courantMax_0": 0.0 },
    { "time": 0.01, "courantMax_0": 0.595866 },
    { "time": 0.015, "courantMax_0": 0.768778 },
    { "time": 0.02, "courantMax_0": 0.806096 },
    { "time": 0.49, "courantMax_0": 0.85218 },
    { "time": 0.495, "courantMax_0": 0.85218 },
    { "time": 0.5, "courantMax_0": 0.85218 }
  ]
}
"""

import subprocess

import json
import pandas as pd
import numpy as np

# update latest simulation metrics
subprocess.call("foamLog -n -quiet log.icoFoam", shell=True)

selection_list = [
    {"fpath": "logs/Time_0", "label": "Time", "name": "time", "units": "s"},
    {
        "fpath": "logs/CourantMax_0",
        "label": "Courant Max",
        "name": "courantMax_0",
        "units": "",
    },
    {
        "fpath": "logs/clockTime_0",
        "label": "Clock Time",
        "name": "clockTime_0",
        "units": "s",
    },
]


data_raw = {}
metadata = {}
names = []
for selection in selection_list:
    fpath = selection["fpath"]

    label = selection["label"]
    name = selection["name"]
    units = selection["units"]
    data = np.loadtxt(fpath).tolist()

    data_raw[name] = data
    metadata[name] = {"label": label, "units": units}
    names.append(name)


# Use pandas to convert to "record" format
# 'records' : list like [{column -> value}, … , {column -> value}]
# records format is suitable for g2 frontend chart rendering
data_records = pd.DataFrame.from_dict(data_raw).to_dict(orient="records")

# write structure to metrics file
output = {"names": names, "metadata": metadata, "data": data_records}
with open("metrics.json", "w") as f:
    json.dump(output, f)

