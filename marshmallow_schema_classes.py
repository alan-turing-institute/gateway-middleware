
import marshmallow as ma

from sqlalchemy_classes import *

class ParamSpecSchema(ma.Schema):
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


class CaseFieldSchema(ma.Schema):
    class Meta:
        model = CaseField
        fields = ("case_field_id","case_id","name","child_field","specs")
    child_field = ma.fields.Nested("self",many=True)
    specs = ma.fields.List(ma.fields.Nested("ParamSpecSchema"))
        
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

    
     
class CaseSchema(ma.Schema):
    class Meta:
        model = Case
        fields = ("case_id","name","fields")
    fields = ma.fields.List(ma.fields.Nested("CaseFieldSchema"))

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
            
