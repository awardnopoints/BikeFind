from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+cymysql://conor:team0db1@team0db.cojxdhcdsq2b.us-west-2.rds.amazonaws.com/team0"
db = SQLAlchemy(app)

class staticData(db.Model):
    address = db.Column(db.String(70),  unique=True, nullable=False, primary_key=True)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    banking = db.Column(db.Boolean, unique=False, nullable=True)

class dynamicData(db.Model):
    time = db.Column(db.Integer, unique=False, nullable=False, primary_key=True)
    address = db.Column(db.String(70),  unique=True, nullable=False, primary_key=True)
    totalBikeStands = db.Column(db.Integer)
    availableBikeStands = db.Column(db.Integer)
    availableBikes = db.Column(db.Integer)
    status = db.Column(db.String(70), unique=False, nullable=False)

db.create_all()
#newEntry = staticData(address="North Side Hovel", latitude=2, longitude=5, banking=True)
entry2 = dynamicData(time=123, address="UCD", totalBikeStands=5, availableBikeStands=2, availableBikes=1, status="OK")
entry1 = dynamicData(time=123, address="Howth", totalBikeStands=5, availableBikeStands=2, availableBikes=1, status="OK")
#db.session.add(newEntry)
db.session.add(entry1)
db.session.commit()
