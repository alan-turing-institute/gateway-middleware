"""
Creates a test interFoam damBreak case.
Uses components from the "phase store".
"""

from connection.models import Case, db, Repository, Script
from .create_case_store import make_phases


def create_phase_store():
    """
    Populate the "store" of phases
    """
    # add some cases to the Phase Store
    session = db.session
    phases = make_phases()

    exists = session.query(Case).filter(Case.name == "phases").all()
    if len(exists) > 0:
        return "Case already exists: phases."
    session.add(phases)
    session.commit()
    return "Added case: phases."


def set_up_dambreak_testdata():
    """
    Make a real case, using phases from the 'phase store',
    and commit it to the database
    """
    phase_store_message = create_phase_store()

    session = db.session
    exists = session.query(Case).filter(Case.name == "damBreak").first()
    if exists:
        return f"{phase_store_message} Case already exists: damBreak."

    repository = Repository(
        url="https://github.com/alan-turing-institute/simulate-damBreak.git",
        branch=None,
        commit=None,
    )

    # make damBreak case
    damBreak = Case(
        name="damBreak",
        thumbnail="https://raw.githubusercontent.com/alan-turing-institute/simulate-damBreak/master/thumbnail.png",
        description="interFoam damBreak tutorial",
        repository=repository,
        visible=True,
    )
    # retrieve the phase store from the database
    new_phase_store = session.query(Case).filter(Case.name == "phases").first()

    # copy phases from the phase store, and name them Water and Air
    new_phaseA = new_phase_store.fields[0].deep_copy()
    new_phaseA.name = "Water"
    new_phaseA.prepend_prefix("Water_")

    new_phaseB = new_phase_store.fields[1].deep_copy()
    new_phaseB.name = "Air"
    new_phaseB.prepend_prefix("Air_")

    damBreak.fields.append(new_phaseA)
    damBreak.fields.append(new_phaseB)

    script = Script(
        parent_case=damBreak,
        source="constants.template.yml",
        destination="constants.yml",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=damBreak,
        source="simulate/state/job_id",
        destination="simulate/state/job_id",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=damBreak,
        source="simulate/state/job_token",
        destination="simulate/state/job_token",
        action=None,
        patch=True,
    )
    session.add(script)

    script = Script(
        parent_case=damBreak,
        source=None,
        destination="simulate/run.sh",
        action="RUN",
        patch=False,
    )
    session.add(script)

    Script(
        parent_case=damBreak,
        source=None,
        destination="simulate/stop.sh",
        action="STOP",
        patch=False,
    )
    session.add(script)

    session.add(damBreak)
    session.commit()
    return f"{phase_store_message} Added case: damBreak."
