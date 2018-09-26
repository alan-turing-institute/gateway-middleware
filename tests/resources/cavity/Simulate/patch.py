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
parameter_set["nu"] = config["kinematic_viscosity"]
parameter_set.writeFile()

wall_velocity = config["wall_velocity"]
velocity_set = ParsedParameterFile("0/U")

velocity_vector = f"uniform ({wall_velocity:.10f} 0 0)"
velocity_set["boundaryField"]["movingWall"]["value"] = velocity_vector
velocity_set.writeFile()
