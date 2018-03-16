from app import db
from app.models import User, StaticData, DynamicData, WeatherData
import time
DynamicData.query.delete()
db.session.commit()
count = 0
while(True):
    data = DynamicData(time=count, address="Clontarf", totalBikeStands = 10, availableBikeStands = 1, availableBikes = 9, status = "OK")
    db.session.add(data)
    db.session.commit()
    count += 1

    total_data = DynamicData.query.all()
    print(total_data)
    time.sleep(10)
