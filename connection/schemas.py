"""
Set up marshmallow classes for serialising data
"""
from flask_marshmallow import Marshmallow

from .models import (Case, CaseField,
                     Job, JobParameter,
                     ParameterSpec, Output)


ma = Marshmallow()


class ParamSpecSchema(ma.ModelSchema):
    """
    Serialise a Parameter spec
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = ParameterSpec
        fields = ('id', 'name', 'value')

    def make_param_spec(self, data):
        """
        Make an instance from a map
        """
        return ParameterSpec(
            id=data.get('id'),
            name=data.get('name'),
            value=data.get('value')
        )


class CaseFieldSchema(ma.ModelSchema):
    """
    Fully serialise a case field
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = CaseField
        fields = ('name', 'child_fields', 'specs')
    child_fields = ma.Nested('self', many=True)
    specs = ma.List(ma.Nested('ParamSpecSchema'))

    def make_case_field(self, data):
        """
        Make an instance from a map
        """
        casefield = CaseField(name=data.get('name'),
                              case_field_id=data.get('case_field_id')
                             )
        if data.get('specs'):
            ps_schema = ParamSpecSchema()
            for spec in data.get('specs'):
                param_spec = ps_schema.make_param_spec(spec)
                param_spec.parent_casefield = casefield.case_field_id
                casefield.specs.append(param_spec)
        if data.get('child_field'):
            for child in data.get('child_field'):
                child_cf = self.make_case_field(child)
                child_cf.parent_id = casefield.case_field_id
                casefield.child_field.append(child_cf)
        return casefield


class CaseSchema(ma.ModelSchema):
    """
    Fully serialise a Case
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = Case
        fields = ('id', 'name', 'fields', 'thumbnail', 'description')
    fields = ma.List(ma.Nested('CaseFieldSchema'))

    def make_case(self, data):
        """
        Make an instance from a map
        """
        case = Case(cid=data.get('id'),
                    name=data.get('name')
                   )
        if data.get('fields'):
            cfs = CaseFieldSchema()
            for child in data.get('fields'):
                case_field = cfs.make_case_field(child)
                case_field.case_id = case.id
                case.fields.append(case_field)
        return case


class CaseHeaderSchema(ma.ModelSchema):
    """
    Serilaise the key metadata about a Case for
    quick listing
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = Case
        fields = ('id', 'name', 'links', 'thumbnail', 'description')
    links = ma.Hyperlinks({
        'self': ma.URLFor('caseapi', case_id='<id>')
    })


class JobHeaderSchema(ma.ModelSchema):
    """
    Serialise the key metadata about a job schema for
    quick listing
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = Job
        fields = ('id', 'name', 'status', 'user', 'links', 'description',
                  'parent_case')
    links = ma.Hyperlinks({
        'self': ma.URLFor('jobapi', job_id='<id>'),
        'case': ma.URLFor('caseapi', case_id='<case_id>')
    })
    parent_case = ma.Nested('CaseHeaderSchema')


class JobSchema(ma.ModelSchema):
    """
    Serialise a job schema in full
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = Job
        fields = ('id', 'name', 'status', 'user', 'values', 'description',
                  'parent_case', 'outputs')
    values = ma.List(ma.Nested('JobValueSchema'))
    outputs = ma.List(ma.Nested('OutputSchema'))
    parent_case = ma.Nested('CaseSchema')
    

class JobValueSchema(ma.ModelSchema):
    """
    Serialise a key value pair from a job specification
    """

    class Meta:
        """
        Specification of what to use from the original class
        """

        model = JobParameter
        fields = ('id', 'name', 'value', 'parent_template')


class OutputSchema(ma.ModelSchema):
    """
    Serialize name and type of a job output
    """
    class Meta:
        """
        Specification of what to use from the original class
        """
        model = Output
        fields = ('destination_path', 'type')


def init_marshmallow(app):
    """
    Initialise marshmallow given a particular flask app
    """
    ma.init_app(app)
