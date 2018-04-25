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

from flask import Flask
from flask_restful import Api

from connection import init_database
from connection.models import Case, db, Script
from .case_creation_utils import mint_case
from .create_case_store import make_fluid_store, make_tank_store
from .create_mint_store import make_mint_store


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
    for _ in Case.query.all():
        done = True
    if done:
        print('Data already there!')
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

    start = Script(parent_case=mycase, action='start',
                   source='http://the.internet/start',
                   destination='start', patch=False)
    run = Script(parent_case=mycase, action='run',
                 source='http://the.internet/run',
                 destination='run', patch=False)
    gofish = Script(parent_case=mycase, action='gofish',
                    source='http://the.internet/gofish',
                    destination='gofish', patch=False)

    # save this to the DB
    session.add(mycase)
    session.add(start)
    session.add(run)
    session.add(gofish)
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
                            mycase, 'testuser', mintstoremap)

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
