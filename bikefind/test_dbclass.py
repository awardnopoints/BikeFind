''' from conor's classes'''
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

db_connection_string ='mysql+cymysql://root:password@localhost:3306/test_db'
engine = create_engine(db_connection_string)

# way to define user models
Base = declarative_base()

class staticData(Base):
    __tablename__ = 'staticData'
    address = Column(String(70),  unique=True, nullable=False, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    banking = Column(Boolean, unique=False, nullable=True)
   
class dynamicData(Base):
    __tablename__ ='dynamicData'
    time = Column(Integer, unique=False, nullable=False, primary_key=True)
    address = Column(String(70), unique=True, nullable=False, primary_key=True)
    totalBikeStands = Column(Integer)
    availableBikeStands = Column(Integer)
    availableBikes = Column(Integer)
    status = Column(String(70), unique=False, nullable=False)

Base.metadata.create_all(bind=engine) 

