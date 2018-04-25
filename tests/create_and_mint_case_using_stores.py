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
import os
import re
from flask import Flask
from flask_restful import Api

from connection import init_database
from connection.models import (Case, CaseField, db, Job,
                               JobParameter, JobParameterTemplate, Script)
from .create_case_store import make_fluid_store, make_tank_store, make_phases
from .create_mint_store import make_mint_store


def apply_mintstore_to_case_field(mintstore, case_field):
    """
    Populate the values of a case field with defaults form a mintstore
    """
    # output will be a list of minted values.

    minted_value_list = []

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
    except TypeError:
        print("Value of %s doesn't seem to be a number" %
              mintstore_value.name)
        return None
    min_val = None
    max_val = None
    prefix = ''
    for spec in case_field.specs:
        # check mintstore value against min, max
        if spec.name == 'min':
            try:
                min_val = float(spec.value)
            except TypeError:
                print('Min value of %s not a number?' % case_field.name)
        elif spec.name == 'max':
            try:
                max_val = float(spec.value)
            except TypeError:
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
    Get the casefields with specs
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


def mint_case(session, name, case, user, mintstoremap):
    """
    Turn a case into a job by minting it
    """
    new_minted_case = Job(name=name, user=user,
                          parent_case=case)

    for (k, v) in mintstoremap.items():
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


def create_stores():
    """
    Populate the "stores" of case building-blocks, and the mint-store
    """
    # preamble - pretend this bit is being done before hand #################

    # add some cases to the Tank Store and the Fluid Store
    session = db.session
    phases = make_phases()

    done = False
    for _ in Case.query.all():
        done = True
    if done:
        print('Data already there!')
        exit()
    session.add(phases)
    session.commit()
    # add milk, water, air and tankX (fixed values for Jobs) to the JobParameterTemplate
    make_mint_store(session)

    # end of preamble #################


def add_damBreak_scripts(parent_case, local_base_dir):
    """
    Start by getting all the scripts in a local directory,
    and adding them to a dict with default settings (destination same as location,
    no patching, no action.
    """
    scripts = {}
    uri_base = 'https://sgmiddleware.blob.core.windows.net/testopenfoam2/'

    for root, dirs, files in os.walk(local_base_dir):
        for filename in files:
            full_filepath = os.path.join(root,filename)
            rel_filepath = re.search("(damBreak\/[\S]+)",full_filepath).groups()[0]
            scripts[filename] = Script(parent_case = parent_case,
                                       source=uri_base+rel_filepath,
                                       destination=rel_filepath,
                                       action='',
                                       patch=False)
            pass
        pass
    # now override the scripts that we do want to patch
    scripts['transportProperties'].patch=True
    scripts['Allrun'].action='RUN'

    return scripts


def set_up_test_database():
    """
    Make a real case.
    """
    uri_base = 'https://sgmiddleware.blob.core.windows.net/'
    create_stores()
    session = db.session
    # make damBreak case
    damBreak = Case(name='damBreak',
                    thumbnail = uri_base + 'openfoam/thumbnails/damBreak.png',
                    description = 'OpenFOAM simulation of breaking dam')
    new_phase_store = session.query(Case). \
        filter(Case.name == 'phases').first()

    new_phaseA = new_phase_store.fields[0].deep_copy()
    new_phaseA.name = 'Water'
    new_phaseA.prepend_prefix('Water_')
    
    new_phaseB = new_phase_store.fields[1].deep_copy()
    new_phaseB.name = "Air"
    new_phaseB.prepend_prefix('Air_')

    damBreak.fields.append(new_phaseA)
    damBreak.fields.append(new_phaseB)

    scripts = add_damBreak_scripts(damBreak,'tests/resources/damBreak')

    for script in scripts.values():
        session.add(script)
    session.add(damBreak)
    session.commit()
