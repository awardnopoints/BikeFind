from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

#Change to local database after pull
db_connection_string ='mysql+cymysql://root:password@localhost:3306/test'
engine = create_engine(db_connection_string)

# way to define user models
Base = declarative_base()

class staticData(Base):
    __tablename__ = 'staticData'
    address = Column(String(70),  unique=True, nullable=False, primary_key=True)
    latitude = Column(Float, unique=False, nullable=True)
    longitude = Column(Float, unique=False, nullable=True)
    banking = Column(Boolean, unique=False, nullable=True)

class dynamicData(Base):
    __tablename__ ='dynamicData'
    index = Column(BigInteger, unique=True, primary_key=True)
    time = Column(BigInteger(), unique=False, nullable=False)
    address = Column(String(70), unique=False, nullable=False)
    totalBikeStands = Column(Integer, unique=False, nullable=True)
    availableBikeStands = Column(Integer, unique=False, nullable=True)
    availableBikes = Column(Integer, unique=False, nullable=True)
    status = Column(String(70), unique=False, nullable=True)

class weatherData(Base):
    __tablename__='weatherData'
    index = Column(BigInteger, unique=True, primary_key=True)
    time = Column(BigInteger(), unique=False, nullable=False)
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
