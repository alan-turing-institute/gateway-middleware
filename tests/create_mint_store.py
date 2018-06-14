"""
functions containing all the steps to create a 'MintStore' that has
preset sets of values for known things, e.g. 'milk', 'tankX'"'
"""

from connection.models import JobParameterTemplate, JobParameterTemplateValue


def make_mint_store(session):
    """
    Create some example mint store values
    """
    # create milk in the mintstore table
    milk = JobParameterTemplate(name='Milk', version='1')
    JobParameterTemplateValue(name='density', value='1003.3',
                              parent_template=milk)
    JobParameterTemplateValue(name='viscosity', value='2.3',
                              parent_template=milk)

    # create water in the mintstore table
    water = JobParameterTemplate(name='Water', version='1')
    JobParameterTemplateValue(name='density', value='999.99',
                              parent_template=water)
    JobParameterTemplateValue(name='viscosity', value='1.2',
                              parent_template=water)

    # create air in the mintstore table
    air = JobParameterTemplate(name='Air', version='1')
    JobParameterTemplateValue(name='density', value='1.0',
                              parent_template=air)
    JobParameterTemplateValue(name='viscosity', value='1.48',
                              parent_template=air)

    # create tank_x in the mintstore table
    tankx = JobParameterTemplate(name='TankX', version='1')
    JobParameterTemplateValue(name='width', value='3.35',
                              parent_template=tankx)
    JobParameterTemplateValue(name='length', value='2.56',
                              parent_template=tankx)

    session.add(milk)
    session.add(water)
    session.add(tankx)
    session.add(air)
    session.commit()
