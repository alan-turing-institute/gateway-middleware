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


def apply_mintstore_to_case_field(mintstore, case_field):
    ### output will be a list of minted values.

    minted_value_list = []
    
    print("applying %s to %s" % (mintstore.name, case_field.name) )
    case_fields_with_specs = recursively_get_case_fields_with_specs(case_field)
    mintstore_vals = mintstore.values
    if len(mintstore_vals) != len(case_fields_with_specs):
        raise Exception("number of mintstore values doesn't match number of case_fields %i %i"%
                        (len(mintstore_vals), len(case_fields_with_specs)))

    ### double loop.... is there not a better way?
    for mv in mintstore_vals:
        for cf in case_fields_with_specs:
            if mv.parameter_name == cf.name:
                print("  Setting values for %s" % cf.name)
                minted_value_list.append(apply_mintstore_value_to_case_field(mv,cf))
                break
            pass
        pass
    return minted_value_list
                                         

          

def apply_mintstore_value_to_case_field(mintstore_value, case_field):
    ## output will be a minted value.  name will come from the case_field
    try:
        mint_param_val = float(mintstore_value.parameter_value)
        
    except(TypeError):
        print("Value of %s doesn't seem to be a number" % mintstore_value.parameter_name)
        return None
    min_val = None
    max_val = None
    prefix = ""
    for spec in case_field.specs:
## check mintstore value against min, max
        if spec.property_name == "min":
            try:
                min_val = float(spec.property_value)
            except(TypeError):
                print("Min value of %s not a number?" % case_field.name)
                pass
        elif spec.property_name == "max":
            try:
                max_val = float(spec.property_value)
            except(TypeError):
                print("Max value of %s not a number?" % case_field.name)
                pass
            pass
## get prefix - will be prepended to MintedValue name
        elif spec.property_name == "prefix":
            prefix = spec.property_value
            pass
        pass
    if min_val and max_val:
        if mint_param_val < min_val or mint_param_val > max_val:
            raise ValueError("Out of range!")
        else:
            mv = MintedValue(name = prefix + case_field.name,
                             value = str(mint_param_val))
            return mv
### something went wrong - maybe something wasn't a number etc.
### (though we should support non-number parameters!)
    return None



def recursively_get_case_fields_with_specs(case_field):
    output_list = []
    if len(case_field.specs) > 0:
        if not (len(case_field.specs) == 1 and case_field.specs[0].property_name == "prefix"):
#### ^ what a horrible hack!! we only want to apply MintedStoreValues to those CaseFields
### that have specs, but even 'top-level' things like "tank" or "fluid" can have a prefix...
            output_list += [case_field]
            pass
        pass
    for child in case_field.child_fields:
        output_list += recursively_get_case_fields_with_specs(child)
    return output_list
    

def mint_case(name, case, user, mintstoremap = {} ):

    new_minted_case = MintedCase(mintedcase_name=name, user=user)

    for k,v in mintstoremap.items():
        case_field = session.query(CaseField).filter(CaseField.name==k).first().deep_copy()
        if not case_field:
            raise KeyError("CaseField %s not found in DB" % k)
        mintstore = session.query(MintStore).filter(MintStore.name==v).first().deep_copy()
        if not mintstore:
            raise KeyError("Mintstore %s not found in DB" % v)
        new_minted_case.values += apply_mintstore_to_case_field(mintstore,case_field)
        pass

    return new_minted_case



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
### save this to the DB
    session.add(mycase)
    
### test the prefix has been added
##    print("prefix to fluid2 viscosity ",mycase.fields[2].child_field[1].specs[-1].property_value)

###################################################################
#########################try minting a case ########################


### create a dictionary with the mapping between the case names and the mintstore names
###  ===> i guess the UI will have a better way of doing this in real life!

    mintstoremap = {
        "tankA" : "TankX",
        "fluid 1" : "Milk",
        "fluid 2" : "Water"
    }
    
    minted_case = mint_case("TESTMINT",mycase, "nbarlow",mintstoremap)  
    print("\n ==== Created a MintedCase ====== \n")
    
    for v in minted_case.values:
        print("Minted case has %s = %s" % (v.name, v.value))
        
