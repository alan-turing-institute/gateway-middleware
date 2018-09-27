"""
Create a test icoFoam cavity case.
"""

from connection.models import Case, CaseField, db, ParameterSpec, Repository, Script


def set_up_cavity_testdata():
    """
    Make a cavity case and commit it to the database
    """

    session = db.session

    exists = session.query(Case).filter(Case.name == "cavity").first()

    if exists:
        return f"Case already exists: cavity."

    repository = Repository(
        url="https://github.com/alan-turing-institute/simulate-cavity.git",
        branch=None,
        commit=None,
    )
    # make cavity case
    cavity = Case(
        name="cavity",
        thumbnail="https://raw.githubusercontent.com/alan-turing-institute/"
        "simulate-cavity/master/thumbnail.png",
        description="icoFoam cavity tutorial",
        repository=repository,
        visible=True,
    )

    fluid = CaseField(name="fluid", parent_case=cavity)
    kinematic_viscosity = CaseField(
        name="kinematic_viscosity", parent_field=fluid, component="slider"
    )
    ParameterSpec(name="min", value="0.001", parent_casefield=kinematic_viscosity)
    ParameterSpec(name="max", value="1.0", parent_casefield=kinematic_viscosity)
    ParameterSpec(name="step", value="0.001", parent_casefield=kinematic_viscosity)
    ParameterSpec(name="default", value="0.01", parent_casefield=kinematic_viscosity)
    ParameterSpec(name="units", value="m²/s", parent_casefield=kinematic_viscosity)

    lid = CaseField(name="lid", parent_case=cavity)
    wall_velocity = CaseField(
        name="wall_velocity", parent_field=lid, component="slider"
    )
    ParameterSpec(name="min", value="0.1", parent_casefield=wall_velocity)
    ParameterSpec(name="max", value="2.0", parent_casefield=wall_velocity)
    ParameterSpec(name="step", value="0.01", parent_casefield=wall_velocity)
    ParameterSpec(name="default", value="0.5", parent_casefield=wall_velocity)
    ParameterSpec(name="units", value="m/s", parent_casefield=wall_velocity)

    script = Script(
        parent_case=cavity,
        source="constants.template.yml",
        destination="constants.yml",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=cavity,
        source="simulate/state/job_id",
        destination="simulate/state/job_id",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=cavity,
        source="simulate/state/job_token",
        destination="simulate/state/job_token",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=cavity,
        source="simulate/state/manager_url",
        destination="simulate/state/manager_url",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=cavity,
        source=None,
        destination="simulate/run.sh",
        action="RUN",
        patch=False,
    )
    session.add(script)

    Script(
        parent_case=cavity,
        source=None,
        destination="simulate/stop.sh",
        action="STOP",
        patch=False,
    )
    session.add(script)

    session.add(cavity)
    session.commit()
    return "Added case: cavity."
