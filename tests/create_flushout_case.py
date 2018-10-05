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
        thumbnail="https://simulate.blob.core.windows.net/"
        "openfoam-thumbnails/flushout.png",
        description="Machine learning flushout demonstration.",
        repository=repository,
        visible=True,
    )

    config = CaseField(name="config", parent_case=flushout)

    run_count = CaseField(name="run_count", parent_field=config, component="slider")
    ParameterSpec(name="min", value="2", parent_casefield=run_count)
    ParameterSpec(name="max", value="30", parent_casefield=run_count)
    ParameterSpec(name="step", value="1", parent_casefield=run_count)
    ParameterSpec(name="default", value="10", parent_casefield=run_count)
    ParameterSpec(name="units", value="", parent_casefield=run_count)
    ParameterSpec(name="title", value="Run count", parent_casefield=run_count)

    Re_lower = CaseField(name="Re_lower", parent_field=config, component="slider")
    ParameterSpec(name="min", value="20000", parent_casefield=Re_lower)
    ParameterSpec(name="max", value="40000", parent_casefield=Re_lower)
    ParameterSpec(name="step", value="1000", parent_casefield=Re_lower)
    ParameterSpec(name="default", value="20000", parent_casefield=Re_lower)
    ParameterSpec(name="units", value="", parent_casefield=Re_lower)
    ParameterSpec(
        name="title", value="Reynolds number (lower)", parent_casefield=Re_lower
    )

    Re_upper = CaseField(name="Re_upper", parent_field=config, component="slider")
    ParameterSpec(name="min", value="100000", parent_casefield=Re_upper)
    ParameterSpec(name="max", value="200000", parent_casefield=Re_upper)
    ParameterSpec(name="step", value="1000", parent_casefield=Re_upper)
    ParameterSpec(name="default", value="200000", parent_casefield=Re_upper)
    ParameterSpec(name="units", value="", parent_casefield=Re_upper)
    ParameterSpec(
        name="title", value="Reynolds number (upper)", parent_casefield=Re_upper
    )

    mu_ratio_lower = CaseField(
        name="mu_ratio_lower", parent_field=config, component="slider"
    )
    ParameterSpec(name="min", value="150", parent_casefield=mu_ratio_lower)
    ParameterSpec(name="max", value="200", parent_casefield=mu_ratio_lower)
    ParameterSpec(name="step", value="1", parent_casefield=mu_ratio_lower)
    ParameterSpec(name="default", value="150", parent_casefield=mu_ratio_lower)
    ParameterSpec(name="units", value="", parent_casefield=mu_ratio_lower)
    ParameterSpec(
        name="title", value="Viscosity ratio (lower)", parent_casefield=mu_ratio_lower
    )

    mu_ratio_upper = CaseField(
        name="mu_ratio_upper", parent_field=config, component="slider"
    )
    ParameterSpec(name="min", value="300", parent_casefield=mu_ratio_upper)
    ParameterSpec(name="max", value="400", parent_casefield=mu_ratio_upper)
    ParameterSpec(name="step", value="1", parent_casefield=mu_ratio_upper)
    ParameterSpec(name="default", value="400", parent_casefield=mu_ratio_upper)
    ParameterSpec(name="units", value="", parent_casefield=mu_ratio_upper)
    ParameterSpec(
        name="title", value="Viscosity ratio (upper)", parent_casefield=mu_ratio_upper
    )

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
