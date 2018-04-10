#!/usr/bin/env python

"""
create a Case corresponding to openfoam dambreak and store it in
the db.
"""

from connection import init_database
from connection.models import (db, Case, CaseField, Script,
                               JobParameterTemplate, JobParameter, Job)

from flask import Flask
from flask_restful import Api

def make_dambreak():
    """
    the openfoam dambreak case.
    """
    dambreak = Case(name="dambreak_test")

    allrun_script = Script(name="Allrun",
                         url="testopenfoamapi",
                         parent_case = dambreak)
    allclean_script = Script(name="Allclean",
                           url="testopenfoamapi",
                           parent_case = dambreak)
    return dambreak


def upload_dambreak_test():
    """
    upload test case and scripts to db
    """
    session = db.session
    dambreak = make_dambreak()
    session.add(dambreak)
    session.commit()
