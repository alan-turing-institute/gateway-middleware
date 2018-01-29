"""
functions containing all the steps to create a 'MintStore'  that has 
preset sets of values for known things, e.g. "milk", "tankX"
"""

from sqlalchemy_classes import *

def make_mint_store(session):
    # create milk in the mintstore table
    milk = MintStore(name="Milk",version="1")
    milk_density = MintStoreValue(parameter_name="density",
                                   parameter_value="1003.3",
                                   parent_mintstore=milk)
    milk_viscosity = MintStoreValue(parameter_name="viscosity",
                                     parameter_value="2.3",
                                     parent_mintstore=milk)
    

    # create water in the mintstore table
    water = MintStore(name="Water",version="1")
    water_density = MintStoreValue(parameter_name="density",
                                    parameter_value="999.99",
                                    parent_mintstore=water)
    water_viscosity = MintStoreValue(parameter_name="viscosity",
                                      parameter_value="1.2",
                                      parent_mintstore=water)


    tankX = MintStore(name="TankX",version="1")
    tank_width = MintStoreValue(parameter_name="width",
                                 parameter_value="3.35",
                                 parent_mintstore=tankX)
    tank_length = MintStoreValue(parameter_name="length",
                                  parameter_value="2.56",
                                  parent_mintstore=tankX)

    session.add(milk)
    session.add(water)
    session.add(tankX)
    session.commit()
