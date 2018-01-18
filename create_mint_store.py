"""
functions containing all the steps to create a 'MintStore'  that has 
preset sets of values for known things, e.g. "milk", "tankX"
"""

from sqlalchemy_classes import *

def make_mint_store(session):
        # create milk in the mintstore table
    milk = MintStore(name="Milk",version="1")
    milk_density = MintStoreValues(parameter_name="density",
                                   parameter_value="1003.3",
                                   parent_mintstore=milk)
    milk_viscosity = MintStoreValues(parameter_name="viscosity",
                                     parameter_value="28.3",
                                     parent_mintstore=milk)
    milk.values.append(milk_density)
    milk.values.append(milk_viscosity)

    # create water in the mintstore table
    water = MintStore(name="Water",version="1")
    water_density = MintStoreValues(parameter_name="density",
                                    parameter_value="999.99",
                                    parent_mintstore=water)
    water_viscosity = MintStoreValues(parameter_name="viscosity",
                                      parameter_value="1.2",
                                      parent_mintstore=water)
    water.values.append(water_density)
    water.values.append(water_viscosity)

    tankX = MintStore(name="TankX",version="1")
    tank_width = MintStoreValues(parameter_name="width",
                                 parameter_value="3425.",
                                 parent_mintstore=tankX)
    tank_length = MintStoreValues(parameter_name="length",
                                  parameter_value="2425.",
                                  parent_mintstore=tankX)
    
    tankX.values.append(tank_width)
    tankX.values.append(tank_length)

    session.add(milk)
    session.add(water)
    session.add(tankX)
