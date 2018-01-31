"""
functions containing all the steps to create a 'MintStore' that has
preset sets of values for known things, e.g. 'milk', 'tankX'"'
"""

from sqlalchemy_classes import MintStore, MintStoreValue


def make_mint_store(session):
    """
    Create some example mint store values
    """
    # create milk in the mintstore table
    milk = MintStore(name='Milk', version='1')
    MintStoreValue(parameter_name='density', parameter_value='1003.3',
                   parent_mintstore=milk)
    MintStoreValue(parameter_name='viscosity', parameter_value='2.3',
                   parent_mintstore=milk)

    # create water in the mintstore table
    water = MintStore(name='Water', version='1')
    MintStoreValue(parameter_name='density', parameter_value='999.99',
                   parent_mintstore=water)
    MintStoreValue(parameter_name='viscosity', parameter_value='1.2',
                   parent_mintstore=water)

    tankx = MintStore(name='TankX', version='1')
    MintStoreValue(parameter_name='width', parameter_value='3.35',
                   parent_mintstore=tankx)
    MintStoreValue(parameter_name='length', parameter_value='2.56',
                   parent_mintstore=tankx)

    session.add(milk)
    session.add(water)
    session.add(tankx)
    session.commit()
