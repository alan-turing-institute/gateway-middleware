"""
Create a test icoFoam cavity case,
using components from the "phase store".
"""

from dataloading.case_json_loader import read_case_from_json

from connection.models import Case, db, Job


def set_up_osrc_testdata():
    """
    Make a osrc case and commit it to the database
    """
    session = db.session
    # make osrc case
    osrc = read_case_from_json('resources/osrc.json')

    session.add(osrc)
    session.commit()


def clear_db():
    """
    Clear the database from all the junk
    """
    session = db.session

    jobs = Job.query.all()
    for job in jobs:
        session.delete(job)
    cases = Case.query.all()
    for case in cases:
        session.delete(case)
    session.commit()
