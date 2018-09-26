#!/usr/bin/env python

# flake8: noqa
import yaml
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def read_yaml(fname):
    with open(fname, "r") as stream:
        content = yaml.load(stream)
        return content


config = read_yaml("constants.yml")

# read existing parameter file
parameter_set = ParsedParameterFile("constant/transportProperties")

parameter_set["water"]["nu"] = config["Water_viscosity"]
parameter_set["water"]["rho"] = config["Water_density"]

parameter_set["air"]["nu"] = config["Air_viscosity"]
parameter_set["air"]["rho"] = config["Air_density"]
parameter_set["sigma"] = config["Water_surface_tension"]

# overwrite existing parameter file
parameter_set.writeFile()
