from app import db

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class StaticData(db.Model):
    address = db.Column(db.String(70),  unique=True, nullable=False, primary_key=True)
    latitude = db.Column(db.String(10))
    longitude = db.Column(db.String(10))
    banking = db.Column(db.Boolean, unique=False, nullable=True)

    def __repr__(self):
        return '<address: {}>'.format(self.address)

class DynamicData(db.Model):
    time = db.Column(db.BigInteger, unique=False, nullable=False, primary_key=True)
    address = db.Column(db.String(70),  unique=False, nullable=False, primary_key=True)
    totalBikeStands = db.Column(db.Integer)
    availableBikeStands = db.Column(db.Integer)
    availableBikes = db.Column(db.Integer)
    status = db.Column(db.String(70), unique=False, nullable=False)

    def __repr__(self):
        return '<time: {}, address: {}>'.format(self.time, self.address)

class WeatherData(db.Model):
    time = db.Column(db.BigInteger(), unique=True, nullable=False, primary_key=True)
    mainDescription = db.Column(db.String(70), unique=False, nullable=True)
    detailedDescription = db.Column(db.String(70), unique=False, nullable=True)
    icon = db.Column(db.String(20), unique=False, nullable=True)

    currentTemp = db.Column(db.Float, unique=False, nullable=True)
    maxTemp = db.Column(db.Float, unique=False, nullable=True)
    minTemp = db.Column(db.Float, unique=False, nullable=True)
    pressure = db.Column(db.Integer, unique=False, nullable=True)
    humidity = db.Column(db.Integer, unique=False, nullable=True)

    windSpeed = db.Column(db.Float, unique=False, nullable=True)
    windAngle = db.Column(db.Integer, unique=False, nullable=True)
    cloudDensity = db.Column(db.Integer, unique=False, nullable=True)
    visibility = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<time: {}>'.format(self.time)
