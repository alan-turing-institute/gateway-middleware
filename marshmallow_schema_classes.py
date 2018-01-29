
from flask_marshmallow import Marshmallow

from sqlalchemy_classes import app, Case, CaseField, ParameterSpec, MintedCase, MintedValue

ma = Marshmallow(app)

class ParamSpecSchema(ma.ModelSchema):
    class Meta:
        model = ParameterSpec
        fields = ("parameterspec_id","property_name","property_value")

    def make_param_spec(self,data):
        p = ParameterSpec(
            parameterspec_id = data.get("parameterspec_id"),
            property_name = data.get("property_name"),
            property_value = data.get("property_value")
            )
        return p


class CaseFieldSchema(ma.ModelSchema):
    class Meta:
        model = CaseField
        fields = ("name","child_fields","specs")
    child_fields = ma.Nested("self", many=True)
    specs = ma.List(ma.Nested("ParamSpecSchema"))
        
    def make_case_field(self,data):
        cf = CaseField(
            name = data.get("name"),
            case_field_id = data.get("case_field_id")
        )
        if data.get("specs"):
            ps_schema = ParamSpecSchema()
            for spec in data.get("specs"):
                param_spec = ps_schema.make_param_spec(spec)
                param_spec.parent_casefield = cf.case_field_id
                cf.specs.append(param_spec)
        if data.get("child_field"):
            for child in data.get("child_field"):
                child_cf = self.make_case_field(child)
                child_cf.parent_id = cf.case_field_id
                cf.child_field.append(child_cf)
        return cf

    
     
class CaseSchema(ma.ModelSchema):
    class Meta:
        model = Case
        fields = ("case_id","name","fields")
    fields = ma.List(ma.Nested("CaseFieldSchema"))

    def make_case(self,data):
        c = Case(
            case_id = data.get("case_id"),
            name = data.get("name")
        )
        if data.get("fields"):
            cfs = CaseFieldSchema()
            for child in data.get("fields"):
                case_field = cfs.make_case_field(child)
                case_field.case_id = c.case_id
                c.fields.append(case_field)
        return c
            
class CaseHeaderSchema(ma.ModelSchema):
    class Meta:
        model = Case
        fields = ("case_id", "name", 'links')
    links = ma.Hyperlinks({
        'self': ma.URLFor('caseapi', case_id='<case_id>')
    })

    def make_case(self, data):
        c = Case(
            case_id = data.get("case_id"),
            name = data.get("name")
        )
        if data.get("fields"):
            cfs = CaseFieldSchema()
            for child in data.get("fields"):
                case_field = cfs.make_case_field(child)
                case_field.case_id = c.case_id
                c.fields.append(case_field)
        return c

class JobHeaderSchema(ma.ModelSchema):
    class Meta:
        model = MintedCase
        fields = ("mintedcase_id", 'mintedcase_name', 'user', 'links')
    links = ma.Hyperlinks({
        'self': ma.URLFor('jobapi', job_id='<mintedcase_id>'),
        'case': ma.URLFor('caseapi', case_id='<case_id>')
    })

class JobSchema(ma.ModelSchema):
    class Meta:
        model = MintedCase
        fields = ("mintedcase_id", 'mintedcase_name', 'user', 'values')
    values = ma.List(ma.Nested("JobValueSchema"))

class JobValueSchema(ma.ModelSchema):
    class Meta:
        model = MintedValue
