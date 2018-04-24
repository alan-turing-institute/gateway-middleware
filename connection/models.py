"""
This module is reponsible for the SQL connection
to store Cases and Jobs
"""

from flask_sqlalchemy import SQLAlchemy

from .constants import JobStatus
from .field import Field

db = SQLAlchemy()

Base = db.Model


class Case(Base):
    """
    This represents the metadata for a Case in the system
    """

    __tablename__ = 'case'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    flat_fields = None

    def _get_possible_fields(self):
        """
        Flatten the fields in a map for easy checking of whether they are
        allowed and what their bounds are
        """
        stack = []
        stack.extend(self.fields)
        flat_fields = {}
        while len(stack) > 0:
            child = stack.pop()
            # Recusively add children
            stack.extend(child.child_fields)

            # Get all the flattened spec
            specs_map = {}
            for spec in child.specs:
                existing = specs_map.get(spec.name)
                if existing is None:
                    specs_map[spec.name] = spec.value
                elif isinstance(existing, list):
                    existing.append(spec.value)
                else:
                    specs_map[spec.name] = [existing, spec.value]

            # If you have children you're not a field!
            if len(child.child_fields) == 0:
                field = Field(child.name, specs_map)
                flat_fields[field.process_name] = field
        self.flat_fields = flat_fields

    def validate_value(self, fullname, value):
        """
        Check if a value is allowed to be set for a particular
        parameter.
        This uses the full name of the parameter, not the display name
        """
        if self.flat_fields is None:
            self._get_possible_fields()
        field = self.flat_fields.get(fullname)
        if field is None:
            return False
        return field.validate_value(fullname, value)

    def required_values(self):
        """
        Return a set of all the fiels that need to be set
        """
        if self.flat_fields is None:
            self._get_possible_fields()
        return set(self.flat_fields.keys())


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
        """
        Create a deep clone
        """
        new_case_field = CaseField(
            name=self.name)
        for child in self.child_fields:
            new_case_field.child_fields.append(child.deep_copy())
        for spec in self.specs:
            new_case_field.specs.append(spec.deep_copy())
        return new_case_field

    def prepend_prefix(self, prefix):
        """
        Add a prefix to all child fields
        """
        for child in self.child_fields:
            child.prepend_prefix(prefix)
        prefix_spec = [spec for spec in self.specs if
                       spec.name == 'prefix']
        if prefix_spec:
            prefix_spec[0].value = prefix + prefix_spec[0].value
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
        """
        Deep clone
        """
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
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False,
                       default=JobStatus.NOT_STARTED.value)

    parent_case = db.relationship('Case')

    def set_name(self, new_name, log):
        """
        Replace the job name if it is sensible.

        Return True if the job name was changed. If it was
        not there will be a string in the log explaining
        why it was rejected.
        """
        if new_name is None:
            log.append('Name must be provided')
            return False
        new_name = new_name.strip()
        if len(new_name) == 0:
            log.append('Name cannot be the empty string')
            return False
        self.name = new_name
        return True

    def set_description(self, new_description, log):
        """
        Replace the job description if it is sensible.

        Return True if the job description was changed. If it was
        not there will be a string in the log explaining
        why it was rejected.
        """
        if new_description is None:
            log.append('Description must be provided')
            return False
        new_description = new_description.strip()
        if len(new_description) == 0:
            log.append('Description cannot be the empty string')
            return False
        self.description = new_description
        return True

    def set_value_list(self, new_values, log):
        """
        Replace the list of jobs with a list of new jobs

        Return True if the list was replaced successfully.
        Note that data may partially have been changed, so the
        session should still be rollbacked.
        If it returns false log will have appended messages
        explaining why it was rejected.
        """
        success = True
        for value in self.values:
            db.session.delete(value)
        for value in new_values:
            if self.validate_value(value['name'], value['value']):
                new_minted_value = JobParameter(name=value['name'],
                                                value=value['value'],
                                                parent_job=self)
                self.values.append(new_minted_value)
            else:
                success = False
                log.append('Rejected parameter "{}" with value "{}"'.
                           format(value['name'], value['value']))
        return success

    def validate_value(self, fullname, value):
        """
        Check if a value is allowed to be set for a particular
        parameter.
        This uses the full name of the parameter, not the display name
        """
        return self.parent_case.validate_value(fullname, value)

    def fully_configured(self):
        """
        Check to make sure the job has all of it's required values set
        """
        set_values = set([v.name for v in self.values])
        required_values = self.parent_case.required_values()
        return len(required_values - set_values) == 0

    def field_list(self):
        """
        Get the field values as a dictionary
        """
        fields = []
        for param in self.values:
            fields.append({
                'name': param.name,
                'value': param.value
            })
        return fields

    def script_list(self):
        """
        Get the list of scripts as a dictionary
        """
        scripts = []
        for script in self.parent_case.scripts:
            scripts.append({
                'source': script.source,
                'destination': script.destination,
                'action': script.action,
                'patch': script.patch
            })
        return scripts


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

    def __repr__(self):
        """
        Create a user friendly string representation
        """
        return '<JP {}: {}>'.format(self.name, self.value)


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
        """
        Create a deep clone
        """
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
        """
        Create a deep clone
        """
        new_mint_store_val = JobParameterTemplateValue(
            id=self.id,
            name=self.name,
            value=self.value
        )
        return new_mint_store_val


JobParameterTemplate.values = db.relationship('JobParameterTemplateValue',
                                              back_populates='parent_template',
                                              cascade='all, delete-orphan')


class Script(Base):
    """
    A table of scripts for a case
    """

    __tablename = 'script'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer,
                        db.ForeignKey('case.id'),
                        nullable=False)
    source = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=False)
    patch = db.Column(db.Boolean, nullable=False)        

    parent_case = db.relationship('Case', back_populates='scripts')


Case.scripts = db.relationship('Script',
                               back_populates='parent_case',
                               cascade='all, delete-orphan')


def init_database(app):
    """
    Initialise the database and required classes in the context
    of the relevant flask app
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
