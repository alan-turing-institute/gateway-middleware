#!/usr/bin/env python

from app import *


if __name__ == "__main__":
    
    # create milk in the mintstore table
    milk = MintStore(name="Milk",version="1")
    milk_density = MintStoreValues(parameter_name="density",parameter_value="1003.3", parent_mintstore=milk)
    milk_viscosity = MintStoreValues(parameter_name="viscosity",parameter_value="28.3", parent_mintstore=milk)
    milk.values.append(milk_density)
    milk.values.append(milk_viscosity)

    # create water in the mintstore table
    water = MintStore(name="Water",version="1")
    water_density = MintStoreValues(parameter_name="density",parameter_value="999.99", parent_mintstore=water)
    water_viscosity = MintStoreValues(parameter_name="viscosity",parameter_value="1.2", parent_mintstore=water)
    water.values.append(milk_density)
    water.values.append(milk_viscosity)

    tankX = MintStore(name="TankX",version="1")
    tank_width = MintStoreValues(parameter_name="width",parameter_value="3425.", parent_mintstore=tankX)
    tank_length = MintStoreValues(parameter_name="length",parameter_value="2425.", parent_mintstore=tankX)
    
    tankX.values.append(tank_width)
    tankX.values.append(tank_length)

    session = sessionmaker(bind=engine)()
    session.add(milk)
    session.add(water)
    session.add(tankX)

### create a case that contains a tank and two fluids

    tank_store = Case(name="tanks_R_us")
    
    tankA = CaseField(name="tankA")#,parent=tank_store)

    tankA_length = CaseField(name="length")
 #                            parent_case=tank_store,
                           #  parent=tankA)
    tankA_width = CaseField(name="width")#,
#                            parent_case=tank_store,
                            #parent=tankA)
    
    tankA_length_min = ParameterSpec(property_name="min", property_value="2")
    tankA_length_max = ParameterSpec(property_name="max", property_value="4")
    tankA_length_default = ParameterSpec(property_name="default", property_value="3")
    tankA_length_units = ParameterSpec(property_name="units", property_value="m")
    tankA_length.specs.append(tankA_length_min)
    tankA_length.specs.append(tankA_length_max)
    tankA_length.specs.append(tankA_length_default)
    tankA_length.specs.append(tankA_length_units)

    tankA_width_min = ParameterSpec(property_name="min", property_value="2")
    tankA_width_max = ParameterSpec(property_name="max", property_value="4")
    tankA_width_default = ParameterSpec(property_name="default", property_value="3")
    tankA_width_units = ParameterSpec(property_name="units", property_value="m")
    tankA_width.specs.append(tankA_width_min)
    tankA_width.specs.append(tankA_width_max)
    tankA_width.specs.append(tankA_width_default)
    tankA_width.specs.append(tankA_width_units)
 #   tankA.child_field = [tankA_length, tankA_width]

 #   tank_store.fields.append(tankA_length)
 #   tank_store.fields.append(tankA_width)
    tank_store.fields.append(tankA)
    tankA.child_field.append(tankA_length)
    tankA.child_field.append(tankA_width)
    session.add(tank_store)

    fluid_store = Case(name="fluids_R_us")
    
    fluidA = CaseField(name="fluidA")#,parent_case=fluid_store)

    fluidA_density = CaseField(name="density")#,
#                               parent=fluidA)
    fluidA_viscosity = CaseField(name="viscosity")#,
#                                 parent=fluidA)
    
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
                                         property_value="0.2")
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
    


    fluidA.child_field.append(fluidA_density)
    fluidA.child_field.append(fluidA_viscosity)
    fluid_store.fields.append(fluidA)
    session.add(fluid_store)

# create a real case, using the tank from the tank store 
#  and the fluid from the fluid store

    mycase = Case(name="MyCase")
    
    new_tank_store = session.query(Case).filter(Case.name=="tanks_R_us").first()
    
    new_tankA = new_tank_store.fields[0].deep_copy()

    new_fluid_store = session.query(Case).filter(Case.name=="fluids_R_us").first()
    
    new_fluid1 = new_fluid_store.fields[0].deep_copy()
    new_fluid1.name = "fluid 1"
    new_fluid1.prepend_prefix("Fluid1_")
    new_fluid2 = new_fluid_store.fields[0].deep_copy()
    new_fluid2.name = "fluid 2"
    new_fluid2.prepend_prefix("Fluid2_")
    
    mycase.fields.append(new_tankA)
    mycase.fields.append(new_fluid1)
    mycase.fields.append(new_fluid2)

# test the prefix has been added
    print("prefix to fluid2 viscosity ",mycase.fields[2].child_field[1].specs[-1].property_value)

# try minting a case

    
