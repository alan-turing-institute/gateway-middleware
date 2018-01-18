#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Case(Base):
    __tablename__ = 'case'

    case_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class CaseField(Base):
    __tablename__ = 'case_field'

    case_field_id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey('case.case_id'), nullable=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('case_field.case_field_id'), nullable=True)

    parent_case = relationship('Case', back_populates='fields')
    child_fields = relationship('CaseField')
    parent_field = relationship('CaseField', remote_side=[case_field_id])

    def deep_copy(self):
        new_case_field = CaseField(
            name = self.name)
        for child in self.child_fields:
            new_case_field.child_field.append(child.deep_copy())
        for spec in self.specs:
            new_case_field.specs.append(spec.deep_copy())
        return new_case_field

    def prepend_prefix(self, prefix):
        for child in self.child_field:
            child.prepend_prefix(prefix)
        prefix_spec = [spec for spec in self.specs if spec.property_name == "prefix"]
        if prefix_spec:
            prefix_spec[0].property_value = prefix + prefix_spec[0].property_value
        else:
            self.specs.append(ParameterSpec(property_name= "prefix", property_value=prefix))

Case.fields = relationship('CaseField', order_by=CaseField.case_field_id,
                           back_populates='parent_case', cascade='all, delete-orphan')


class ParameterSpec(Base):
    __tablename__ = 'parameterspec'

    parameterspec_id = Column(Integer, primary_key=True, autoincrement=True)
    casefield_id = Column(Integer, ForeignKey('case_field.case_field_id'), nullable=False)
    property_name = Column(String, nullable=False)
    property_value = Column(String, nullable=False)

    parent_casefield = relationship('CaseField', back_populates='specs')

    def deep_copy(self):
        new_param_spec = ParameterSpec(
            property_name = self.property_name,
            property_value = self.property_value
        )
        return new_param_spec

CaseField.specs = relationship('ParameterSpec', back_populates='parent_casefield', cascade='all, delete-orphan')


class MintedCase(Base):
    __tablename__ = 'mintedcase'

    mintedcase_id = Column(Integer,primary_key=True, autoincrement = True)
    mintedcase_name = Column(String, nullable = False)
    user = Column(String, nullable = False)


class MintedValue(Base):
    __tablename__ = "mintedvalues"

    mintedvalue_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mintedcase_id = Column(Integer, ForeignKey('mintedcase.mintedcase_id'), nullable=False)
    value = Column(String, nullable=False)
    mintstore_id = Column(Integer, ForeignKey('mintstore.mintstore_id'),nullable=True)

    parent_mintedcase = relationship('MintedCase', back_populates='values')
    parent_mintstore = relationship("MintStore")

MintedCase.values = relationship('MintedValue', back_populates='parent_mintedcase', cascade='all, delete-orphan')


class MintStore(Base):
    __tablename__ = "mintstore"

    mintstore_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    version = Column(Integer, nullable=False)

class MintStoreValues(Base):
    __tablename__ = "mintstorevalues"

    mintstorevalue_id = Column(Integer, primary_key=True,autoincrement=True)
    mintstore_id = Column(Integer,ForeignKey('mintstore.mintstore_id'),nullable=False)
    parameter_name = Column(String,nullable=False)
    parameter_value = Column(String,nullable=False)

    parent_mintstore = relationship("MintStore", back_populates='values')

MintStore.values = relationship("MintStoreValues", back_populates="parent_mintstore", cascade="all, delete-orphan")

Base.metadata.create_all(engine)
