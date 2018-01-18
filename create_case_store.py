#!/usr/bin/env python

"""
functions containing all the steps to create a 'Tank Store' case and 
a 'Fluid Store' case.  These would be special cases (no pun intended) of Case
that a case-builder could pull things out of (e.g. here, tankA, fluidA) when
building a 'real-life' case. 
"""

from sqlalchemy_classes import *

def make_tank_store(session):
    tank_store = Case(name="tanks_R_us")
    
    tankA = CaseField(name="tankA")

    tankA_length = CaseField(name="length")
    tankA_width = CaseField(name="width")    
    tankA_length_min = ParameterSpec(property_name="min", property_value="0.2")
    tankA_length_max = ParameterSpec(property_name="max", property_value="40")
    tankA_length_default = ParameterSpec(property_name="default", property_value="3")
    tankA_length_units = ParameterSpec(property_name="units", property_value="m")
    tankA_length.specs.append(tankA_length_min)
    tankA_length.specs.append(tankA_length_max)
    tankA_length.specs.append(tankA_length_default)
    tankA_length.specs.append(tankA_length_units)

    tankA_width_min = ParameterSpec(property_name="min", property_value="0.1")
    tankA_width_max = ParameterSpec(property_name="max", property_value="40")
    tankA_width_default = ParameterSpec(property_name="default", property_value="3")
    tankA_width_units = ParameterSpec(property_name="units", property_value="m")
    tankA_width.specs.append(tankA_width_min)
    tankA_width.specs.append(tankA_width_max)
    tankA_width.specs.append(tankA_width_default)
    tankA_width.specs.append(tankA_width_units)
    tank_store.fields.append(tankA)
    tankA.child_fields.append(tankA_length)
    tankA.child_fields.append(tankA_width)
    session.add(tank_store)


def make_fluid_store(session):
    fluid_store = Case(name="fluids_R_us")
    fluidA = CaseField(name="fluidA")
    fluidA_density = CaseField(name="density")
    fluidA_viscosity = CaseField(name="viscosity")
    fluidA_density_min = ParameterSpec(property_name="min", 
                                       property_value="200")
    fluidA_density_max = ParameterSpec(property_name="max", 
                                       property_value="4000")
    fluidA_density_default = ParameterSpec(property_name="default", 
                                           property_value="1000")
    fluidA_density_units = ParameterSpec(property_name="units", 
                                         property_value="kg/m^3")
    fluidA_density.specs.append(fluidA_density_min)
    fluidA_density.specs.append(fluidA_density_max)
    fluidA_density.specs.append(fluidA_density_default)
    fluidA_density.specs.append(fluidA_density_units)

    fluidA_viscosity_min = ParameterSpec(property_name="min", 
                                         property_value="0.01")
    fluidA_viscosity_max = ParameterSpec(property_name="max", 
                                         property_value="4.")
    fluidA_viscosity_default = ParameterSpec(property_name="default", 
                                             property_value="1")
    fluidA_viscosity_units = ParameterSpec(property_name="units", 
                                           property_value="Pa.s")
    fluidA_viscosity.specs.append(fluidA_viscosity_min)
    fluidA_viscosity.specs.append(fluidA_viscosity_max)
    fluidA_viscosity.specs.append(fluidA_viscosity_default)
    fluidA_viscosity.specs.append(fluidA_viscosity_units)
    fluidA.child_fields.append(fluidA_density)
    fluidA.child_fields.append(fluidA_viscosity)
    fluid_store.fields.append(fluidA)
    session.add(fluid_store)

