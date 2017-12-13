import sqlalchemy

# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///:memory:', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float


class ParameterSpec(Base):
    __tablename__ = 'parameter_spec'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(Float)


class Case(Base):
    __tablename__ = 'case'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)

    def __repr__(self):
       return "name = {}".format(self.name)



case = Case(name='Test')
case
