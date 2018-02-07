#!/usr/bin/env python

"""
main function, doing the following:
* create Cases in the DB that are stores of Tank and Fluid casefields.
(calling functions in create_case_store.py)
* create a JobParameterTemplate in the DB containing preset sets of values
called 'milk' and 'tankA' (calling functions in create_mintstore.py)

Then...

* Make a 'real' case, with a tank and two fluids,
by retrieving casefields from the Tank and Fluid stores.
"""

from connection import init_database
from connection.models import (db, Case, CaseField,
                               JobParameterTemplate, JobParameter, Job)

from .create_case_store import make_tank_store, make_fluid_store
from .create_mint_store import make_mint_store

from flask import Flask
from flask_restful import Api


def apply_mintstore_to_case_field(mintstore, case_field):
    """
    Populate the values of a case field with defaults form a mintstore
    """
    # output will be a list of minted values.

    minted_value_list = []

    print('applying %s to %s' % (mintstore.name, case_field.name))
    case_fields_with_specs = recursively_get_case_fields_with_specs(case_field)
    mintstore_vals = mintstore.values
    if len(mintstore_vals) != len(case_fields_with_specs):
        raise Exception("number of mintstore values doesn't"
                        'match number of case_fields %i %i' %
                        (len(mintstore_vals), len(case_fields_with_specs)))

    # double loop.... is there not a better way?
    for mv in mintstore_vals:
        for cf in case_fields_with_specs:
            if mv.name == cf.name:
                print('  Setting values for %s' % cf.name)
                minted_value_list.append(
                    apply_mintstore_value_to_case_field(mv, cf))
                break
    return minted_value_list


def apply_mintstore_value_to_case_field(mintstore_value, case_field):
    """
    Apply a specific mint store value to a case field
    """
    # output will be a minted value.  name will come from the case_field
    try:
        mint_param_val = float(mintstore_value.value)
    except(TypeError):
        print("Value of %s doesn't seem to be a number" %
              mintstore_value.name)
        return None
    min_val = None
    max_val = None
    prefix = ""
    for spec in case_field.specs:
        # check mintstore value against min, max
        if spec.name == 'min':
            try:
                min_val = float(spec.value)
            except(TypeError):
                print('Min value of %s not a number?' % case_field.name)
        elif spec.name == 'max':
            try:
                max_val = float(spec.value)
            except(TypeError):
                print('Max value of %s not a number?' % case_field.name)
        elif spec.name == 'prefix':
            # get prefix - will be prepended to JobParameter name
            prefix = spec.value
    if min_val and max_val:
        if mint_param_val < min_val or mint_param_val > max_val:
            raise ValueError('Out of range!')
        else:
            mv = JobParameter(name=prefix + case_field.name,
                              value=str(mint_param_val))
            return mv
    # something went wrong - maybe something wasn't a number etc.
    # (though we should support non-number parameters!)
    return None


def recursively_get_case_fields_with_specs(case_field):
    """
    Get the casefiels with specs
    """
    output_list = []
    if len(case_field.specs) > 0:
        if not (len(case_field.specs) == 1 and
                case_field.specs[0].name == 'prefix'):
            # ^ what a horrible hack!! we only want to apply
            # MintedStoreValues to those CaseFields
            # that have specs, but even 'top-level' things like
            # 'tank' or 'fluid' can have a prefix...
            output_list += [case_field]
    for child in case_field.child_fields:
        output_list += recursively_get_case_fields_with_specs(child)
    return output_list


def mint_case(session, name, case, user, mintstoremap={}):
    """
    Turn a case into a job by minting it
    """
    new_minted_case = Job(name=name, user=user,
                          parent_case=case)

    for (k, v) in mintstoremap.items():
        print(k, ",", v)
        case_field = session.query(CaseField). \
            filter(CaseField.name == k).first().deep_copy()
        if not case_field:
            raise KeyError('CaseField %s not found in DB' % k)
        mintstore = session.query(JobParameterTemplate). \
            filter(JobParameterTemplate.name == v).first().deep_copy()
        if not mintstore:
            raise KeyError('Mintstore %s not found in DB' % v)
        new_minted_case.values += apply_mintstore_to_case_field(mintstore,
                                                                case_field)

    return new_minted_case


def set_up_test_database():
    """
    Set up a database with some stuff in it
    """
    # preamble - pretend this bit is being done before hand #################

    # add some cases to the Tank Store and the Fluid Store
    session = db.session
    tank = make_tank_store()
    fluid = make_fluid_store()

    done = False
    for case in Case.query.all():
        done = True
    if done:
        print("Data already there!")
        exit()
    session.add(tank)
    session.add(fluid)
    session.commit()
    # add milk and tankX (fixed values for Jobs) to the JobParameterTemplate
    make_mint_store(session)

    # end of preamble #################

    # create a real case, using the tank from the tank store
    #  and the fluid from the fluid store

    mycase = Case(name='MyCase')

    new_tank_store = session.query(Case). \
        filter(Case.name == 'tanks_R_us').first()

    new_tankA = new_tank_store.fields[0].deep_copy()
    new_fluid_store = session.query(Case). \
        filter(Case.name == 'fluids_R_us').first()

    new_fluid1 = new_fluid_store.fields[0].deep_copy()
    new_fluid1.name = 'fluid 1'
    new_fluid1.prepend_prefix('Fluid1_')
    new_fluid2 = new_fluid_store.fields[0].deep_copy()
    new_fluid2.name = 'fluid 2'
    new_fluid2.prepend_prefix('Fluid2_')

    mycase.fields.append(new_tankA)
    mycase.fields.append(new_fluid1)
    mycase.fields.append(new_fluid2)
    # save this to the DB
    session.add(mycase)
    session.commit()

    # test the prefix has been added
    # print('prefix to fluid2 viscosity ',
    #       mycase.fields[2].child_field[1].specs[-1].property_value)

    ###################################################################
    # ########################try minting a case ########################

    # create a dictionary with the mapping between
    # the case names and the mintstore names
    # => i guess the UI will have a better way of doing this in real life!

    mintstoremap = {
        'tankA': 'TankX',
        'fluid 1': 'Milk',
        'fluid 2': 'Water'
    }

    minted_case = mint_case(session, 'TESTMINT',
                            mycase, 'nbarlow', mintstoremap)
    print('\n ==== Created a Job ====== \n')

    for v in minted_case.values:
        print('Minted case has %s = %s' % (v.name, v.value))

    session.add(minted_case)
    session.commit()


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ('postgres://'
                                             'sg:sg@localhost:8082/sg')

    init_database(app)

    api = Api(app)
    with app.app_context():
        set_up_test_database()
