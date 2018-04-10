#!/usr/bin/env python

"""
create a Case corresponding to openfoam dambreak and store it in
the db.
"""

from connection.models import Case, Script


def make_dambreak():
    """
    the openfoam dambreak case.
    """
    dambreak = Case(name='dambreak_test')

    Script(name='Allrun',
           url='testopenfoamapi',
           parent_case=dambreak)
    Script(name='Allclean',
           url='testopenfoamapi',
           parent_case=dambreak)
    return dambreak
