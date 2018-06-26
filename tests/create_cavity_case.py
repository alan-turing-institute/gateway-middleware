"""
Create a test icoFoam cavity case,
using components from the "phase store".
"""

import os
import re
from posixpath import join

from connection.models import Case, CaseField, Script, ParameterSpec, db


def cavity_scripts(parent_case, local_base_dir):
    """
    Start by getting all the scripts in a local directory,
    and adding them to a dict (while modifiying source location with the
    prefix on Azure blob storage).   First apply default settings
    (destination same as location, no patching, no action), then override
    as necessary for individual scripts.
    """
    scripts = {}
    uri_base = ('https://simulate.blob.core.windows.net/'
                'openfoam-test-cases/')

    for root, _dirs, files in os.walk(local_base_dir):
        files = [f for f in files if not f[0] == '.']  # ignore hidden files
        for filename in files:
            full_filepath = os.path.join(root, filename)
            rel_filepath = re.search(r'cavity\/([\S]+)',
                                     full_filepath).groups()[0]

            # assume that relevant files aleady exist at source_filepath
            # (no files are transferred to cloud storage here)
            source_filepath = join(uri_base, 'cavity', rel_filepath)
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


def set_up_cavity_testdata():
    """
    Make a cavity case and commit it to the database
    """

    uri_base = 'https://simulate.blob.core.windows.net/'

    session = db.session
    # make damBreak case
    cavity = Case(name='cavity',
                  thumbnail=join(uri_base, 'openfoam-thumbnails/cavity.png'),
                  description='icoFoam cavity tutorial',
                  visible=True)

    fluid = CaseField(name='fluid', parent_case=cavity)
    kinematic_viscosity = CaseField(
        name='kinematic_viscosity', parent_field=fluid)
    ParameterSpec(name='min', value='0.000001',
                  parent_casefield=kinematic_viscosity)
    ParameterSpec(name='max', value='0.0001',
                  parent_casefield=kinematic_viscosity)
    ParameterSpec(name='step', value='0.000001',
                  parent_casefield=kinematic_viscosity)
    ParameterSpec(name='default', value='0.00001',
                  parent_casefield=kinematic_viscosity)
    ParameterSpec(name='units', value='m/s^2',
                  parent_casefield=kinematic_viscosity)

    lid = CaseField(name='lid', parent_case=cavity)
    wall_velocity = CaseField(name='wall_velocity', parent_field=lid)
    ParameterSpec(name='min', value='0.1',
                  parent_casefield=wall_velocity)
    ParameterSpec(name='max', value='2.0',
                  parent_casefield=wall_velocity)
    ParameterSpec(name='step', value='0.01',
                  parent_casefield=wall_velocity)
    ParameterSpec(name='default', value='0.5',
                  parent_casefield=wall_velocity)
    ParameterSpec(name='units', value='m/s',
                  parent_casefield=wall_velocity)

    # get the list of necessary scripts by scanning this local directory,
    # even though the actual scripts are on Azure blob storage
    # NOTE: this requires a manual sync between local scripts and azure scripts
    scripts = cavity_scripts(cavity, 'tests/resources/cavity')

    # add everything to the database
    for script in scripts.values():
        session.add(script)
    session.add(cavity)
    session.commit()
