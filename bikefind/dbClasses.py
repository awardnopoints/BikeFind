from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

#Change to local database after pull
db_connection_string = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/test3"
#db_connection_string = "mysql+cymysql://root:password@localhost/test"
engine = create_engine(db_connection_string)

# way to define user models
Base = declarative_base()

class staticData(Base):
    __tablename__ = 'staticData'
    address = Column(String(70),  unique=True, nullable=False, primary_key=True)
    latitude = Column(String(70), unique=False, nullable=True)
    longitude = Column(String(70), unique=False, nullable=True)
    banking = Column(Boolean, unique=False, nullable=True)

class dynamicData(Base):
    __tablename__ ='dynamicData'
    time = Column(BigInteger(), unique=False, nullable=False, primary_key=True)
    address = Column(String(70), unique=False, nullable=False, primary_key=True)
    totalBikeStands = Column(Integer, unique=False, nullable=True)
    availableBikeStands = Column(Integer, unique=False, nullable=True)
    availableBikes = Column(Integer, unique=False, nullable=True)
    status = Column(String(70), unique=False, nullable=True)
    
class currentData(Base):
    __tablename__ = 'currentData'
    address = Column(String(70), unique=True, nullable=False, primary_key=True)
    last_update = Column(BigInteger(), unique=False, nullable=True)
    totalBikeStands = Column(Integer, unique=False, nullable=True)
    availableBikeStands = Column(Integer, unique=False, nullable=True)
    availableBikes = Column(Integer, unique=False, nullable=True)
    status = Column(String(70), unique=False, nullable=True)

class weatherData(Base):
    __tablename__='weatherData'
    time = Column(BigInteger(), unique=False, nullable=False, primary_key=True)
    mainDescription = Column(String(70), unique=False, nullable=True)
    detailedDescription = Column(String(70), unique=False, nullable=True)
    icon = Column(String(20), unique=False, nullable=True)

    currentTemp = Column(Float, unique=False, nullable=True)
    maxTemp = Column(Float, unique=False, nullable=True)
    minTemp = Column(Float, unique=False, nullable=True)
    pressure = Column(Integer, unique=False, nullable=True)
    humidity = Column(Integer, unique=False, nullable=True)

    windSpeed = Column(Float, unique=False, nullable=True)
    windAngle = Column(Integer, unique=False, nullable=True)
    cloudDensity = Column(Integer, unique=False, nullable=True)
    visibility = Column(Integer, unique=False, nullable=True)

Base.metadata.create_all(bind=engine)
