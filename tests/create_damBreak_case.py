"""
Create a test OpenFOAM damBreak case,
using components from the "phase store".
"""

import os
import re
from posixpath import join

from connection.models import Case, db, Script
from .create_case_store import make_phases


def create_phase_store():
    """
    Populate the "store" of phases
    """
    # add some cases to the Phase Store
    session = db.session
    phases = make_phases()

    exists = session.query(Case).filter(Case.name == 'phases').all()
    if len(exists) > 0:
        print('PhaseStore already there!')
        exit()
    session.add(phases)
    session.commit()


def add_damBreak_scripts(parent_case, local_base_dir):
    """
    Start by getting all the scripts in a local directory,
    and adding them to a dict (while modifiying source location with the
    prefix on Azure blob storage).   First apply default settings
    (destination same as location, no patching, no action), then override
    as necessary for individual scripts.
    """
    scripts = {}
    uri_base = ('https://sgmiddleware.blob.core.windows.net/'
                'openfoam-test-cases/')

    for root, _dirs, files in os.walk(local_base_dir):
        files = [f for f in files if not f[0] == '.']  # ignore hidden files
        for filename in files:
            full_filepath = os.path.join(root, filename)
            rel_filepath = re.search(r'damBreak\/([\S]+)',
                                     full_filepath).groups()[0]

            # assume that relevant files aleady exist at source_filepath
            # (no files are transferred to cloud storage here)
            source_filepath = join(uri_base, 'damBreakRefactor', rel_filepath)
            destination_filepath = rel_filepath

            # assume unique filenames for test case
            scripts[filename] = Script(parent_case=parent_case,
                                       source=source_filepath,
                                       destination=destination_filepath,
                                       action='',
                                       patch=False)

    # now override the scripts that we do want to patch
    scripts['patch.py'].patch = True
    scripts['job_id'].patch = True
    scripts['run.sh'].action = 'RUN'

    return scripts


def setup_dambreak_testdata():
    """
    Make a real case, using phases from the 'phase store',
    and commit it to the database
    """
    create_phase_store()

    uri_base = 'https://sgmiddleware.blob.core.windows.net/'

    session = db.session
    # make damBreak case
    damBreak = Case(name='damBreak',
                    thumbnail=uri_base + 'openfoam/thumbnails/damBreak.png',
                    description='OpenFOAM simulation of breaking dam',
                    visible=True)
    # retrieve the phase store from the database
    new_phase_store = session.query(Case). \
        filter(Case.name == 'phases').first()

    # copy phases from the phase store, and name them Water and Air
    new_phaseA = new_phase_store.fields[0].deep_copy()
    new_phaseA.name = 'Water'
    new_phaseA.prepend_prefix('Water_')

    new_phaseB = new_phase_store.fields[1].deep_copy()
    new_phaseB.name = 'Air'
    new_phaseB.prepend_prefix('Air_')

    damBreak.fields.append(new_phaseA)
    damBreak.fields.append(new_phaseB)
    # get the list of necessary scripts by listing this local directory,
    # even though the actual scripts are on Azure blob storage
    scripts = add_damBreak_scripts(damBreak, 'tests/resources/damBreak')

    # add everything to the database
    for script in scripts.values():
        session.add(script)
    session.add(damBreak)
    session.commit()
