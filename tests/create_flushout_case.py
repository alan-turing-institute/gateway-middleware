"""
Create a test icoFoam flushout case.
"""

from connection.models import Case, CaseField, db, ParameterSpec, Repository, Script


def set_up_flushout_testdata():
    """
    Make a flushout case and commit it to the database
    """

    session = db.session

    exists = session.query(Case).filter(Case.name == "flushout").first()

    if exists:
        return f"Case already exists: flushout."

    repository = Repository(
        url="https://github.com/ImperialCollegeLondon/mfg-MachineLearning-Flushout.git",
        branch="webapp",
        commit=None,
    )
    # make flushout case
    flushout = Case(
        name="flushout",
        thumbnail="https://raw.githubusercontent.com/alan-turing-institute/"
        "simulate-flushout/master/thumbnail.png",
        description="Machine learning flushout demonstration.",
        repository=repository,
        visible=True,
    )

    config = CaseField(name="config", parent_case=flushout)
    run_count = CaseField(name="run_count", parent_field=config, component="slider")
    ParameterSpec(name="min", value="10", parent_casefield=run_count)
    ParameterSpec(name="max", value="30", parent_casefield=run_count)
    ParameterSpec(name="step", value="1", parent_casefield=run_count)
    ParameterSpec(name="default", value="15", parent_casefield=run_count)
    ParameterSpec(name="units", value="", parent_casefield=run_count)

    script = Script(
        parent_case=flushout,
        source="constants.template.yml",
        destination="constants.yml",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=flushout,
        source="simulate/state/job_id",
        destination="simulate/state/job_id",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=flushout,
        source="simulate/state/job_token",
        destination="simulate/state/job_token",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=flushout,
        source="simulate/state/manager_url",
        destination="simulate/state/manager_url",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=flushout,
        source=None,
        destination="simulate/run.sh",
        action="RUN",
        patch=False,
    )
    session.add(script)

    Script(
        parent_case=flushout,
        source=None,
        destination="simulate/stop.sh",
        action="STOP",
        patch=False,
    )
    session.add(script)

    session.add(flushout)
    session.commit()
    return "Added case: flushout."
