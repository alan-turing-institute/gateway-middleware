#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

Base = db.Model

class Case(Base):
    __tablename__ = 'case'

    case_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class CaseField(Base):
    __tablename__ = 'case_field'

    case_field_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.case_id'), nullable=True)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('case_field.case_field_id'), nullable=True)

    parent_case = db.relationship('Case', back_populates='fields')
    child_fields = db.relationship('CaseField')
    parent_field = db.relationship('CaseField', remote_side=[case_field_id])

    def deep_copy(self):
        new_case_field = CaseField(
            name = self.name)
        for child in self.child_fields:
            new_case_field.child_fields.append(child.deep_copy())
        for spec in self.specs:
            new_case_field.specs.append(spec.deep_copy())
        return new_case_field

    def prepend_prefix(self, prefix):
        for child in self.child_fields:
            child.prepend_prefix(prefix)
        prefix_spec = [spec for spec in self.specs if spec.property_name == "prefix"]
        if prefix_spec:
            prefix_spec[0].property_value = prefix + prefix_spec[0].property_value
        else:
            self.specs.append(ParameterSpec(property_name= "prefix", property_value=prefix))

Case.fields = db.relationship('CaseField', order_by=CaseField.case_field_id,
                        back_populates='parent_case', cascade='all, delete-orphan')


class ParameterSpec(Base):
    __tablename__ = 'parameterspec'

    parameterspec_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    casefield_id = db.Column(db.Integer, db.ForeignKey('case_field.case_field_id'), nullable=False)
    property_name = db.Column(db.String, nullable=False)
    property_value = db.Column(db.String, nullable=False)

    parent_casefield = db.relationship('CaseField', back_populates='specs')

    def deep_copy(self):
        new_param_spec = ParameterSpec(
            property_name = self.property_name,
            property_value = self.property_value
        )
        return new_param_spec

CaseField.specs = db.relationship('ParameterSpec', back_populates='parent_casefield', cascade='all, delete-orphan')


class MintedCase(Base):
    __tablename__ = 'mintedcase'

    mintedcase_id = db.Column(db.Integer,primary_key=True, autoincrement = True)
    mintedcase_name = db.Column(db.String, nullable = False)
    user = db.Column(db.String, nullable = False)


class MintedValue(Base):
    __tablename__ = "mintedvalues"

    mintedvalue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    mintedcase_id = db.Column(db.Integer, db.ForeignKey('mintedcase.mintedcase_id'), nullable=False)
    value = db.Column(db.String, nullable=False)
    mintstore_id = db.Column(db.Integer, db.ForeignKey('mintstore.mintstore_id'),nullable=True)

    parent_mintedcase = db.relationship('MintedCase', back_populates='values')
    parent_mintstore = db.relationship("MintStore")

MintedCase.values = db.relationship('MintedValue', back_populates='parent_mintedcase', cascade='all, delete-orphan')


class MintStore(Base):
    __tablename__ = "mintstore"

    mintstore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String,nullable=False)
    version = db.Column(db.Integer, nullable=False)
    
    def deep_copy(self):
        new_mintstore = MintStore(
            name = self.name,
            version= self.version
        )
        for val in self.values:
            new_mintstore.values.append(val.deep_copy())
        return new_mintstore

class MintStoreValue(Base):
    __tablename__ = "mintstorevalue"

    mintstorevalue_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    mintstore_id = db.Column(db.Integer,db.ForeignKey('mintstore.mintstore_id'),nullable=False)
    parameter_name = db.Column(db.String,nullable=False)
    parameter_value = db.Column(db.String,nullable=False)

    parent_mintstore = db.relationship("MintStore", back_populates='values')

    def deep_copy(self):
        new_mint_store_val = MintStoreValue(
            mintstore_id = self.mintstore_id,
            parameter_name = self.parameter_name,
            parameter_value = self.parameter_value
        )
        return new_mint_store_val

    

MintStore.values = db.relationship("MintStoreValue", back_populates="parent_mintstore", cascade="all, delete-orphan")

db.create_all()

