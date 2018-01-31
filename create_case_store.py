"""
functions containing all the steps to create a 'Tank Store' case and
a 'Fluid Store' case.  These would be special cases (no pun intended) of Case
that a case-builder could pull things out of (e.g. here, tanka, fluida) when
building a 'real-life' case.
"""

from sqlalchemy_classes import Case, CaseField, ParameterSpec


def make_tank_store(session):
    """
    Make an example tank case containing a sample tank
    """
    tank_store = Case(name='tanks_R_us')

    tanka = CaseField(name='tankA', parent_case=tank_store)

    tanka_length = CaseField(name='length', parent_field=tanka)
    ParameterSpec(property_name='min', property_value='0.2',
                  parent_casefield=tanka_length)
    ParameterSpec(property_name='max', property_value='40',
                  parent_casefield=tanka_length)
    ParameterSpec(property_name='default', property_value='3',
                  parent_casefield=tanka_length)
    ParameterSpec(property_name='units', property_value='m',
                  parent_casefield=tanka_length)

    tanka_width = CaseField(name='width', parent_field=tanka)
    ParameterSpec(property_name='min', property_value='0.1',
                  parent_casefield=tanka_width)
    ParameterSpec(property_name='max', property_value='40',
                  parent_casefield=tanka_width)
    ParameterSpec(property_name='default', property_value='3',
                  parent_casefield=tanka_width)
    ParameterSpec(property_name='units', property_value='m',
                  parent_casefield=tanka_width)

    session.add(tank_store)
    session.commit()


def make_fluid_store(session):
    """
    Make an example fluid case for reusing later
    """
    fluid_store = Case(name='fluids_R_us')

    fluida = CaseField(name='fluidA', parent_case=fluid_store)

    fluida_density = CaseField(name='density', parent_field=fluida)
    ParameterSpec(property_name='min', property_value='200',
                  parent_casefield=fluida_density)
    ParameterSpec(property_name='max', property_value='4000',
                  parent_casefield=fluida_density)
    ParameterSpec(property_name='default', property_value='1000',
                  parent_casefield=fluida_density)
    ParameterSpec(property_name='units', property_value='kg/m^3',
                  parent_casefield=fluida_density)

    fluida_viscosity = CaseField(name='viscosity', parent_field=fluida)
    ParameterSpec(property_name='min', property_value='0.01',
                  parent_casefield=fluida_viscosity)
    ParameterSpec(property_name='max', property_value='4.',
                  parent_casefield=fluida_viscosity)
    ParameterSpec(property_name='default', property_value='1',
                  parent_casefield=fluida_viscosity)
    ParameterSpec(property_name='units', property_value='Pa.s',
                  parent_casefield=fluida_viscosity)

    session.add(fluid_store)
    session.commit()
