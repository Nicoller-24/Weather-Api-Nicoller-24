from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    temp_min = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    is_hottest_day = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f'<Weather {self.city_name}'

    def serialize(self):
        return {
            "id": self.id,
            "city_name": self.city_name,
            "date": self.date,
            "temp_max": self.temp_max,
            "temp_min": self.temp_min,
            "lat": self.lat,
            "lon": self.lon,
            "is_hottest_day": self.is_hottest_day  
        }
    
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Lead {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "budget": self.budget
        }