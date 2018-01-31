"""
This module is reponsible for the SQL connection
to store Cases and Jobs
"""

from flask_sqlalchemy import SQLAlchemy


# pylint: disable=W0601,C0103,W0602
def init_database(app):
    """
    Initialise the database and required classes in the context
    of the relevant flask app
    """
    global db
    global Case
    global CaseField
    global ParameterSpec
    global MintedCase
    global MintedValue
    global MintStore
    global MintStoreValue

    db = SQLAlchemy(app)

    Base = db.Model

    class Case(Base):
        """
        This represents the metadata for a Case in the system
        """
        __tablename__ = 'case'

        case_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String, nullable=False)

    class CaseField(Base):
        """
        A casefield is a particular accordion or field within a given case
        """
        __tablename__ = 'case_field'

        case_field_id = db.Column(db.Integer, primary_key=True,
                                  autoincrement=True)
        case_id = db.Column(db.Integer, db.ForeignKey('case.case_id'),
                            nullable=True)
        name = db.Column(db.String, nullable=False)
        parent_id = db.Column(db.Integer,
                              db.ForeignKey('case_field.case_field_id'),
                              nullable=True)

        parent_case = db.relationship('Case', back_populates='fields')
        child_fields = db.relationship('CaseField',
                                       backref=db.
                                       backref('parent_field',
                                               remote_side=[case_field_id]))

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
                           spec.property_name == 'prefix']
            if prefix_spec:
                prefix_spec[0].property_value = prefix + \
                                                prefix_spec[0].property_value
            else:
                self.specs.append(ParameterSpec(property_name='prefix',
                                                property_value=prefix))

    Case.fields = db.relationship('CaseField',
                                  order_by=CaseField.case_field_id,
                                  back_populates='parent_case',
                                  cascade='all, delete-orphan')

    class ParameterSpec(Base):
        """
        Each parameterspec is a single metadata entry for a single field.
        There may be many ParameterSpecs per field
        """
        __tablename__ = 'parameterspec'

        parameterspec_id = db.Column(db.Integer, primary_key=True,
                                     autoincrement=True)
        casefield_id = db.Column(db.Integer,
                                 db.ForeignKey('case_field.case_field_id'),
                                 nullable=False)
        property_name = db.Column(db.String, nullable=False)
        property_value = db.Column(db.String, nullable=False)

        parent_casefield = db.relationship('CaseField', back_populates='specs')

        def deep_copy(self):
            new_param_spec = ParameterSpec(
                property_name=self.property_name,
                property_value=self.property_value
            )
            return new_param_spec

    CaseField.specs = db.relationship('ParameterSpec',
                                      back_populates='parent_casefield',
                                      cascade='all, delete-orphan')

    class MintedCase(Base):
        """
        A minted case is a job, or an instance of a case for a
        specific user with chosen values
        """
        __tablename__ = 'mintedcase'
        __table_args__ = (db.UniqueConstraint('user', 'mintedcase_name',
                          name='unique_user_and_name'),)

        mintedcase_id = db.Column(db.Integer, primary_key=True,
                                  autoincrement=True)
        case_id = db.Column(db.Integer, db.ForeignKey('case.case_id'),
                            nullable=False)
        mintedcase_name = db.Column(db.String, nullable=False)
        user = db.Column(db.String, nullable=False)

        parent_case = db.relationship('Case')

    class MintedValue(Base):
        """
        A Minted Value is a specific value for a field in a case.
        """
        __tablename__ = 'mintedvalues'

        mintedvalue_id = db.Column(db.Integer, primary_key=True,
                                   autoincrement=True)
        name = db.Column(db.String, nullable=False)
        mintedcase_id = db.Column(db.Integer,
                                  db.ForeignKey('mintedcase.mintedcase_id'),
                                  nullable=False)
        value = db.Column(db.String, nullable=False)
        mintstore_id = db.Column(db.Integer,
                                 db.ForeignKey('mintstore.mintstore_id'),
                                 nullable=True)

        parent_mintedcase = db.relationship('MintedCase',
                                            back_populates='values')
        parent_mintstore = db.relationship('MintStore')

    MintedCase.values = db.relationship('MintedValue',
                                        back_populates='parent_mintedcase',
                                        cascade='all, delete-orphan')

    class MintStore(Base):
        """
        A mint store is a collection of saved name value pairs
        bound to a given name. The idea is that they can be used
        as prefilled templates for values for cases
        """
        __tablename__ = 'mintstore'

        mintstore_id = db.Column(db.Integer, primary_key=True,
                                 autoincrement=True)
        name = db.Column(db.String, nullable=False)
        version = db.Column(db.Integer, nullable=False)

        def deep_copy(self):
            new_mintstore = MintStore(
                name=self.name,
                version=self.version
            )
            for val in self.values:
                new_mintstore.values.append(val.deep_copy())
            return new_mintstore

    class MintStoreValue(Base):
        """
        A Mint Store Value is a specific key value pair in a
        given mint store
        """
        __tablename__ = 'mintstorevalue'

        mintstorevalue_id = db.Column(db.Integer, primary_key=True,
                                      autoincrement=True)
        mintstore_id = db.Column(db.Integer,
                                 db.ForeignKey('mintstore.mintstore_id'),
                                 nullable=False)
        parameter_name = db.Column(db.String, nullable=False)
        parameter_value = db.Column(db.String, nullable=False)

        parent_mintstore = db.relationship('MintStore',
                                           back_populates='values')

        def deep_copy(self):
            new_mint_store_val = MintStoreValue(
                mintstore_id=self.mintstore_id,
                parameter_name=self.parameter_name,
                parameter_value=self.parameter_value
            )
            return new_mint_store_val

    MintStore.values = db.relationship('MintStoreValue',
                                       back_populates='parent_mintstore',
                                       cascade='all, delete-orphan')

    db.create_all()
