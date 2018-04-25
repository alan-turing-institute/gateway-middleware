#!/usr/bin/env python

"""
Tools to help case-builders (and automated tests) build cases.
The functions in here should not be specific to any given case
or minted values, but can be called by specific case-building modules.
"""

from connection.models import (CaseField, Job,
                               JobParameter, JobParameterTemplate)


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
