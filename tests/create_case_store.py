"""
functions containing all the steps to create a 'Tank Store' case and
a 'Fluid Store' case.  These would be special cases (no pun intended) of Case
that a case-builder could pull things out of (e.g. here, tanka, fluida) when
building a 'real-life' case.
"""

from connection.models import Case, CaseField, ParameterSpec


def make_tank_store():
    """
    Make an example tank case containing a sample tank
    """
    tank_store = Case(name='tanks_R_us', visible=False)

    tanka = CaseField(name='tankA', parent_case=tank_store)

    tanka_length = CaseField(name='length', parent_field=tanka)
    ParameterSpec(name='min', value='0.2',
                  parent_casefield=tanka_length)
    ParameterSpec(name='max', value='40',
                  parent_casefield=tanka_length)
    ParameterSpec(name='default', value='3',
                  parent_casefield=tanka_length)
    ParameterSpec(name='units', value='m',
                  parent_casefield=tanka_length)

    tanka_width = CaseField(name='width', parent_field=tanka)
    ParameterSpec(name='min', value='0.1',
                  parent_casefield=tanka_width)
    ParameterSpec(name='max', value='40',
                  parent_casefield=tanka_width)
    ParameterSpec(name='default', value='3',
                  parent_casefield=tanka_width)
    ParameterSpec(name='units', value='m',
                  parent_casefield=tanka_width)

    return tank_store


def make_fluid_store():
    """
    Make an example fluid case for reusing later
    """
    fluid_store = Case(name='fluids_R_us', visible=False)

    fluida = CaseField(name='fluidA', parent_case=fluid_store)

    fluida_density = CaseField(name='density', parent_field=fluida)
    ParameterSpec(name='min', value='200',
                  parent_casefield=fluida_density)
    ParameterSpec(name='max', value='4000',
                  parent_casefield=fluida_density)
    ParameterSpec(name='default', value='1000',
                  parent_casefield=fluida_density)
    ParameterSpec(name='units', value='kg/m^3',
                  parent_casefield=fluida_density)

    fluida_viscosity = CaseField(name='viscosity', parent_field=fluida)
    ParameterSpec(name='min', value='0.01',
                  parent_casefield=fluida_viscosity)
    ParameterSpec(name='max', value='4.',
                  parent_casefield=fluida_viscosity)
    ParameterSpec(name='default', value='1',
                  parent_casefield=fluida_viscosity)
    ParameterSpec(name='units', value='Pa.s',
                  parent_casefield=fluida_viscosity)

    return fluid_store


def make_phases():
    """
    Make an example fluid case for reusing later
    """
    phase_store = Case(name='phases', visible=False)
    # phase_A (e.g. water)
    phase_A = CaseField(name='phase_A',
                        parent_case=phase_store,
                        component='heading')

    phase_A_density = CaseField(name='density',
                                parent_field=phase_A,
                                component='slider')
    ParameterSpec(name='min', value='1',
                  parent_casefield=phase_A_density)
    ParameterSpec(name='max', value='2000',
                  parent_casefield=phase_A_density)
    ParameterSpec(name='default', value='1000',
                  parent_casefield=phase_A_density)
    ParameterSpec(name='units', value='kg/m^3',
                  parent_casefield=phase_A_density)

    phase_A_viscosity = CaseField(name='viscosity',
                                  parent_field=phase_A,
                                  component='slider')
    ParameterSpec(name='min', value='0.000001',
                  parent_casefield=phase_A_viscosity)
    ParameterSpec(name='max', value='0.0001',
                  parent_casefield=phase_A_viscosity)
    ParameterSpec(name='step', value='0.000001',
                  parent_casefield=phase_A_viscosity)
    ParameterSpec(name='default', value='0.00001',
                  parent_casefield=phase_A_viscosity)
    ParameterSpec(name='units', value='m/s^2',
                  parent_casefield=phase_A_viscosity)

    phase_A_surface_tension = CaseField(name='surface_tension',
                                        parent_field=phase_A,
                                        component='slider')
    ParameterSpec(name='min', value='0.01',
                  parent_casefield=phase_A_surface_tension)
    ParameterSpec(name='max', value='0.1',
                  parent_casefield=phase_A_surface_tension)
    ParameterSpec(name='step', value='0.01',
                  parent_casefield=phase_A_surface_tension)
    ParameterSpec(name='default', value='0.07',
                  parent_casefield=phase_A_surface_tension)
    ParameterSpec(name='units', value='N/m',
                  parent_casefield=phase_A_surface_tension)

    # phase_B (e.g. air)
    phase_B = CaseField(name='phase_B',
                        parent_case=phase_store,
                        component='heading')

    phase_B_density = CaseField(name='density',
                                parent_field=phase_B,
                                component='slider')
    ParameterSpec(name='min', value='1',
                  parent_casefield=phase_B_density)
    ParameterSpec(name='max', value='2000',
                  parent_casefield=phase_B_density)
    ParameterSpec(name='default', value='1000',
                  parent_casefield=phase_B_density)
    ParameterSpec(name='units', value='kg/m^3',
                  parent_casefield=phase_B_density)

    phase_B_viscosity = CaseField(name='viscosity',
                                  parent_field=phase_B,
                                  component='slider')
    ParameterSpec(name='min', value='0.000001',
                  parent_casefield=phase_B_viscosity)
    ParameterSpec(name='max', value='0.0001',
                  parent_casefield=phase_B_viscosity)
    ParameterSpec(name='step', value='0.000001',
                  parent_casefield=phase_B_viscosity)
    ParameterSpec(name='default', value='0.00001',
                  parent_casefield=phase_B_viscosity)
    ParameterSpec(name='units', value='m/s^2',
                  parent_casefield=phase_B_viscosity)

    return phase_store
