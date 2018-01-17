#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Case(Base):
    __tablename__ = 'case'

    case_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class CaseField(Base):
    __tablename__ = 'case_field'

    case_field_id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey('case.case_id'), nullable=False)
    name = Column(String, nullable=False)
    parent = Column(String, nullable=True)

    parent_case = relationship('Case', back_populates='fields')

Case.fields = relationship('CaseField', order_by=CaseField.case_field_id,
                           back_populates='parent_case', cascade='all, delete-orphan')


class ParameterSpec(Base):
    __tablename__ = 'parameterspec'

    parameterspec_id = Column(Integer, primary_key=True, autoincrement=True)
    casefield_id = Column(Integer, ForeignKey('case_field.case_field_id'), nullable=False)
    property_name = Column(String, nullable=False)
    property_value = Column(String, nullable=False)

    parent_casefield = relationship('CaseField', back_populates='specs')

CaseField.specs = relationship('ParameterSpec', back_populates='parent_casefield', cascade='all, delete-orphan')


class MintedCase(Base):
    __tablename__ = 'mintedcase'

    mintedcase_id = Column(Integer,primary_key=True, autoincrement = True)
    mintedcase_name = Column(String, nullable = False)
    user = Column(String, nullable = False)


class MintedValues(Base):
    __tablename__ = "mintedvalues"

    mintedvalue_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mintedcase_id = Column(Integer, ForeignKey('mintedcase.mintedcase_id'), nullable=False)
    value = Column(String, nullable=False)
    mintstore_id = Column(Integer, ForeignKey('mintstore.mintstore_id'),nullable=True)

    parent_mintedcase = relationship('MintedCase', back_populates='values')
    parent_mintstore = relationship("MintStore")

MintedCase.values = relationship('MintedValues', back_populates='parent_mintedcase', cascade='all, delete-orphan')


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

density = CaseField(name="Density", parent=None)

unit = ParameterSpec(property_name="Unit", property_value="Kg/s")
mins = ParameterSpec(property_name="Min", property_value="1")
maxs = ParameterSpec(property_name="Max", property_value="2")

density.specs.append(unit)
density.specs.append(mins)
density.specs.append(maxs)

mixer = Case(name="Mixer")
mixer.fields.append(density)
mixer.fields.append(CaseField(name="Rho",parent=None))
mixer.fields.append(CaseField(name="Tank",parent=None))
mixer.fields.append(CaseField(name="Num_Blades",parent="Tank"))
mixer.fields.append(CaseField(name="Blade_Angle",parent="Tank"))

session = sessionmaker(bind=engine)()

session.add(mixer)

num_cases = session.query(Case).count()
num_fields = session.query(CaseField).count()
num_specs = session.query(ParameterSpec).count()

print("Found", num_cases,"cases", "with", num_fields, "fields", 'and', num_specs, "specs")
