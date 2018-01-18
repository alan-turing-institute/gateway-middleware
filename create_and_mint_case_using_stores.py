#!/usr/bin/env python

"""
main function, doing the following:
* create Cases in the DB that are stores of Tank and Fluid casefields.
(calling functions in create_case_store.py)
* create a MintStore in the DB containing preset sets of values called 'milk' and 'tankA'
(calling functions in create_mintstore.py)

Then...

* Make a 'real' case, with a tank and two fluids, by retrieving casefields from the Tank and Fluid 
stores.
"""

from sqlalchemy_classes import *

from create_case_store import *

from create_mint_store import *


def apply_mintstore_value_to_case_field(minted_value, case_field):
    ## output will be a minted value.  name will come from the case_field

    
    for spec in case_field.specs:
## check mintstore value against min, max 
        pass
    
    
    output_val = MintedValue(name = case_field.name)

    

def mint_case(name, case, user, mintstores = []):

    new_minted_case = MintedCase(mintedcase_name=name, user=user)

    ## get a list of case_fields in the input case that correspond to parameters

    


if __name__ == "__main__":
    
## start a DB session

    session = sessionmaker(bind=engine)()

    ########### preamble - pretend this bit is being done beforehand #######
    
## add some cases to the Tank Store and the Fluid Store
    make_tank_store(session)
    make_fluid_store(session)
## add milk and tankX (fixed values for MintedCases) to the MintStore
    make_mint_store(session)

    ########### end of preamble #################
    
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

### test the prefix has been added
##    print("prefix to fluid2 viscosity ",mycase.fields[2].child_field[1].specs[-1].property_value)

###################################################################
#########################try minting a case ########################


## first retrieve milk, water and tankX from the MintStore
    milk = session.query(MintStore).filter(MintStore.name=="Milk").first()
    water = session.query(MintStore).filter(MintStore.name=="Water").first()
    tank = session.query(MintStore).filter(MintStore.name == "TankX").first()


    
    
