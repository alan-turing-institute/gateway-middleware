#!/usr/bin/env python

"""
functions containing all the steps to create a 'Tank Store' case and 
a 'Fluid Store' case.  These would be special cases (no pun intended) of Case
that a case-builder could pull things out of (e.g. here, tankA, fluidA) when
building a 'real-life' case. 
"""

from sqlalchemy_classes import Case, CaseField, ParameterSpec

def make_tank_store(session):
    tank_store = Case(name="tanks_R_us")
    
    tankA = CaseField(name="tankA", parent_case=tank_store)

    tankA_length = CaseField(name="length", parent_field=tankA)
    tankA_length_min = ParameterSpec(property_name="min", property_value="0.2", parent_casefield=tankA_length)
    tankA_length_max = ParameterSpec(property_name="max", property_value="40", parent_casefield=tankA_length)
    tankA_length_default = ParameterSpec(property_name="default", property_value="3", parent_casefield=tankA_length)
    tankA_length_units = ParameterSpec(property_name="units", property_value="m", parent_casefield=tankA_length)


    tankA_width = CaseField(name="width", parent_field=tankA)    
    tankA_width_min = ParameterSpec(property_name="min", property_value="0.1", parent_casefield=tankA_width)
    tankA_width_max = ParameterSpec(property_name="max", property_value="40", parent_casefield=tankA_width)
    tankA_width_default = ParameterSpec(property_name="default", property_value="3", parent_casefield=tankA_width)
    tankA_width_units = ParameterSpec(property_name="units", property_value="m", parent_casefield=tankA_width)


    session.add(tank_store)
    session.commit()


def make_fluid_store(session):
    fluid_store = Case(name="fluids_R_us")

    fluidA = CaseField(name="fluidA", parent_case=fluid_store)

    fluidA_density = CaseField(name="density", parent_field=fluidA)
    fluidA_density_min = ParameterSpec(property_name="min", 
                                       property_value="200",
                                       parent_casefield=fluidA_density)
    fluidA_density_max = ParameterSpec(property_name="max", 
                                       property_value="4000",
                                       parent_casefield=fluidA_density)
    fluidA_density_default = ParameterSpec(property_name="default", 
                                           property_value="1000",
                                           parent_casefield=fluidA_density)
    fluidA_density_units = ParameterSpec(property_name="units", 
                                         property_value="kg/m^3",
                                         parent_casefield=fluidA_density)


    fluidA_viscosity = CaseField(name="viscosity", parent_field=fluidA)
    fluidA_viscosity_min = ParameterSpec(property_name="min", 
                                         property_value="0.01",
                                         parent_casefield=fluidA_viscosity)
    fluidA_viscosity_max = ParameterSpec(property_name="max", 
                                         property_value="4.",
                                         parent_casefield=fluidA_viscosity)
    fluidA_viscosity_default = ParameterSpec(property_name="default", 
                                             property_value="1",
                                             parent_casefield=fluidA_viscosity)
    fluidA_viscosity_units = ParameterSpec(property_name="units", 
                                           property_value="Pa.s",
                                           parent_casefield=fluidA_viscosity)
    
    session.add(fluid_store)
    session.commit()

