"""
This module is reponsible for the SQL connection
to store Cases and Jobs
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = db.Model


class Case(Base):
    """
    This represents the metadata for a Case in the system
    """
    __tablename__ = 'case'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class CaseField(Base):
    """
    A casefield is a particular accordion or field within a given case
    """
    __tablename__ = 'case_field'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'),
                        nullable=True)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer,
                          db.ForeignKey('case_field.id'),
                          nullable=True)

    parent_case = db.relationship('Case', back_populates='fields')
    child_fields = db.relationship('CaseField',
                                   backref=db.
                                   backref('parent_field',
                                           remote_side=[id]))

    def deep_copy(self):
        new_case_field = CaseField(
            name=self.name)
        for child in self.child_fields:
            new_case_field.child_fields.append(child.deep_copy())
        for spec in self.specs:
            new_case_field.specs.append(spec.deep_copy())
        return new_case_field

    def prepend_prefix(self, prefix):
        for child in self.child_fields:
            child.prepend_prefix(prefix)
        prefix_spec = [spec for spec in self.specs if
                       spec.name == 'prefix']
        if prefix_spec:
            prefix_spec[0].value = prefix + \
                                            prefix_spec[0].value
        else:
            self.specs.append(ParameterSpec(name='prefix',
                                            value=prefix))


Case.fields = db.relationship('CaseField',
                              order_by=CaseField.id,
                              back_populates='parent_case',
                              cascade='all, delete-orphan')


class ParameterSpec(Base):
    """
    Each parameterspec is a single metadata entry for a single field.
    There may be many ParameterSpecs per field
    """
    __tablename__ = 'parameterspec'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    casefield_id = db.Column(db.Integer,
                             db.ForeignKey('case_field.id'),
                             nullable=False)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    parent_casefield = db.relationship('CaseField', back_populates='specs')

    def deep_copy(self):
        new_param_spec = ParameterSpec(
            name=self.name,
            value=self.value
        )
        return new_param_spec


CaseField.specs = db.relationship('ParameterSpec',
                                  back_populates='parent_casefield',
                                  cascade='all, delete-orphan')


class Job(Base):
    """
    A job is an instance of a case for a
    specific user with chosen values
    """
    __tablename__ = 'job'
    __table_args__ = (db.UniqueConstraint('user', 'name',
                      name='unique_user_and_name'),)

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'),
                        nullable=False)
    name = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)

    parent_case = db.relationship('Case')


class JobParameter(Base):
    """
    A Minted Value is a specific value for a field in a case.
    """
    __tablename__ = 'job_parameter'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String, nullable=False)
    job_id = db.Column(db.Integer,
                       db.ForeignKey('job.id'),
                       nullable=False)
    value = db.Column(db.String, nullable=False)
    template_id = db.Column(db.Integer,
                            db.ForeignKey('job_parameter_template.id'),
                            nullable=True)

    parent_job = db.relationship('Job',
                                 back_populates='values')
    parent_template = db.relationship('JobParameterTemplate')


Job.values = db.relationship('JobParameter',
                             back_populates='parent_job',
                             cascade='all, delete-orphan')


class JobParameterTemplate(Base):
    """
    A mint store is a collection of saved name value pairs
    bound to a given name. The idea is that they can be used
    as prefilled templates for values for cases
    """
    __tablename__ = 'job_parameter_template'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String, nullable=False)
    version = db.Column(db.Integer, nullable=False)

    def deep_copy(self):
        new_mintstore = JobParameterTemplate(
            name=self.name,
            version=self.version
        )
        for val in self.values:
            new_mintstore.values.append(val.deep_copy())
        return new_mintstore


class JobParameterTemplateValue(Base):
    """
    A Mint Store Value is a specific key value pair in a
    given mint store
    """
    __tablename__ = 'job_parameter_template_value'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    template_id = db.Column(db.Integer,
                            db.ForeignKey('job_parameter_template.id'),
                            nullable=False)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    parent_template = db.relationship('JobParameterTemplate',
                                      back_populates='values')

    def deep_copy(self):
        new_mint_store_val = JobParameterTemplateValue(
            id=self.id,
            name=self.name,
            value=self.value
        )
        return new_mint_store_val


JobParameterTemplate.values = db.relationship('JobParameterTemplateValue',
                                              back_populates='parent_template',
                                              cascade='all, delete-orphan')


def init_database(app):
    """
    Initialise the database and required classes in the context
    of the relevant flask app
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
