"""
Module to turn JSON cases into real cases
"""

from json import load

from connection.models import Case, CaseField, ParameterSpec, Script


def read_case_from_json(filename):
    """
    Given a json file, read in the case.

    This should parse the JSON file and return it as a case.
    If there are any errors it will throw a exception.
    """
    with open(filename, 'r') as json_file:
        json_data = load(json_file)
        case = parse_case(json_data)
    return case


def parse_case(case_map):
    """
    Take the root of the JSON case specification and turn it into a full case
    """
    case = Case(visible=True)
    for (key, value) in case_map.items():
        key = key.strip().lower()
        if key == 'name':
            case.name = ensure_string(value)
        elif key == 'image':
            case.thumbnail = ensure_string(value)
        elif key == 'description':
            case.description = ensure_string(value)
        elif key == 'script':
            case.scripts = parse_scripts(value, case)
        elif key == 'params':
            case.fields = parse_fields(value, case)
        else:
            raise AttributeError('Found unknown key in root: {}'.format(key))
    return case


def parse_fields(fields_list, parent_case):
    """
    Take the JSON list of fields, and return it
    as a list of CaseFields that can be added to the
    case
    """
    fields = []
    for field_map in fields_list:
        fields.append(parse_field(field_map, parent_case))
    return fields


def parse_field(field_map, parent_case):
    """
    Parse a JSON map into a CaseField
    """
    casefield = CaseField(parent_case=parent_case)
    for key, value in field_map.items():
        key = key.strip().lower()
        if key == 'name':
            casefield.name = ensure_string(value)
        elif key == 'params':
            casefield.child_fields = parse_fields(value, None)
        elif key == 'specs':
            casefield.specs = parse_specs(value, casefield)
    return casefield


def parse_specs(spec_map, parent_casefield):
    """
    Parse a set of specs from JSON to a list of objects
    """
    specs = []
    for spec, value in spec_map.items():
        spec = ensure_string(spec.strip().lower())
        value = ensure_string(value.strip().lower())
        specs.append(ParameterSpec(name=spec, value=value,
                                   parent_casefield=parent_casefield))
    return specs


def parse_scripts(scripts_list, parent_case):
    """
    Take the JSON structure of scripts and make it
    into a list of scripts
    """
    parsed_scripts = []
    for name, script in scripts_list.items():
        s = parse_script(script)
        s.action = name.strip().upper()
        s.parent_case = parent_case
        parsed_scripts.append(s)
    return parsed_scripts


def parse_script(script_map):
    """
    Parse a JSON script record into a Script object
    """
    script = Script(patch=False)
    for key, value in script_map.items():
        key = key.strip().lower()
        if key == 'source':
            script.source = ensure_string(value)
        elif key == 'destination':
            script.destination = ensure_string(value)
        elif key == 'patch':
            script.patch = ensure_boolean(value)
        else:
            raise AttributeError('Unexpected field {} in script'.format(key))
    return script


def ensure_string(value):
    """
    Ensure the current value is a string.

    If the current value is a string. Return it.
    Otherwise throw an exception
    """
    if isinstance(value, str):
        return value
    raise ValueError('{} must be of type string but is {}'.
                     format(value, type(value)))


def ensure_boolean(value):
    """
    Ensure the current value is a boolean

    If the current value is a boolean return it.
    Otherwise throw an exception
    """
    if isinstance(value, bool):
        return value
    raise ValueError('{} must be of type string but is {}'.
                     format(value, type(value)))
