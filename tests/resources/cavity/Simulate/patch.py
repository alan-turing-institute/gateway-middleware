#!/usr/bin/env python

# flake8: noqa

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

# read existing parameter file
parameter_set = ParsedParameterFile('constant/transportProperties')
parameter_set['nu'] = ${parameters['kinematic_viscosity']}

# overwrite existing parameter file
parameter_set.writeFile()

wall_velocity = ${parameters['wall_velocity']}
velocity_set = ParsedParameterFile('0/U')
velocity_set['boundaryField']['movingWall']['value'] = 'uniform ({:.10f} 0 0)'.format(wall_velocity)
velocity_set.writeFile()
