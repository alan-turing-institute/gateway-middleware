"""
This module is to test the field validation
"""

from connection.field import Field


def test_update_specs():
    """
    Test that adding in specs after the constructor works
    """
    field = Field('test', {})
    assert(field.display_name == 'test')
    assert(field.process_name == 'test')
    assert(len(field.properties) == 0)

    field.set_properties(min=8)
    assert(field.display_name == 'test')
    assert(field.process_name == 'test')
    assert(len(field.properties) == 1)
    assert(not field.validate_value('test', 5))
    assert(field.validate_value('test', 8))
    assert(field.validate_value('test', 10))


def test_update_process_name():
    """
    Test that adding in name changes works
    """
    field = Field('test', {})
    assert(field.display_name == 'test')
    assert(field.process_name == 'test')
    assert(len(field.properties) == 0)

    field.set_properties(prefix='pre_')
    assert(field.display_name == 'test')
    assert(field.process_name == 'pre_test')

    field.set_properties(label='cool')
    assert(field.display_name == 'test')
    assert(field.process_name == 'pre_cool')

    field.set_properties(suffix='_suff')
    assert(field.display_name == 'test')
    assert(field.process_name == 'pre_cool_suff')


def test_constructor_process_name():
    """
    Make sure that setting the process name in the constructor works
    """
    field = Field('test', {'prefix': 'a_', 'label': 'b', 'suffix': '_c'})
    assert(field.display_name == 'test')
    assert(field.process_name == 'a_b_c')
    assert(len(field.properties) == 3)
