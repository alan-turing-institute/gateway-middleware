#!/usr/bin/env python

# flake8: noqa

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

# read existing parameter file
parameter_set = ParsedParameterFile('constant/transportProperties')

parameter_set['water']['nu'] = ${parameters['Water_viscosity']}
parameter_set['water']['rho'] = ${parameters['Water_density']}

parameter_set['air']['nu'] = ${parameters['Air_viscosity']}
parameter_set['air']['rho'] = ${parameters['Air_density']}

parameter_set['sigma'] = ${parameters['Water_surface_tension']}

# overwrite existing parameter file
parameter_set.writeFile()
