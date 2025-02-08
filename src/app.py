"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Weather, Lead
import requests


#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/weather/<float:lat>/<float:lon>/<int:cnt>', methods=['GET'])
def get_weather(lat, lon, cnt):
    API_KEY = "ee8d20f96a2af7c6c1cea357e9b6112b"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={cnt}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    print(url)
    if response.status_code != 200:
        return jsonify({"error": "No se pudo obtener el clima"}), response.status_code

    data = response.json()

    return jsonify(data), 200


@app.route('/save_weather/<float:lat>/<float:lon>/<int:cnt>', methods=['POST'])
def save_weather(lat, lon, cnt):
    API_KEY = "ee8d20f96a2af7c6c1cea357e9b6112b"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={cnt}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "No se pudo obtener el clima"}), response.status_code

    data = response.json()
    city_name = data["city"]["name"]

    hottest_entry = max(data["list"], key=lambda x: x["main"]["temp_max"])

    hottest_day = Weather(
        city_name=city_name,
        date=hottest_entry["dt_txt"],
        temp_max=hottest_entry["main"]["temp_max"],
        temp_min=hottest_entry["main"]["temp_min"],
        lat=lat,
        lon=lon,
        is_hottest_day=True  
    )

    db.session.add(hottest_day)
    db.session.commit()

    return jsonify({
        "message": "Día más caluroso guardado correctamente",
        "hottest_day": hottest_day.serialize()
    }), 201

@app.route("/lead/create", methods=["POST"])
def create_lead():
    body = request.get_json()

    if "name" not in body or "location" not in body or "budget" not in body:
        return jsonify({"msg": "Faltan datos requeridos"}), 400
 
    existing_customer = Lead.query.filter_by(name=body["name"]).first()
    if existing_customer:
        return jsonify({"msg": "El cliente ya existe"}), 409

    
    customer = Lead(
        name=body["name"],
        location=body["location"].upper(),
        budget=body["budget"]
    )

    db.session.add(customer)
    db.session.commit()

    response_body = {
        "msg": "Lead creado",
        "result": customer.serialize()
    }
    return jsonify(response_body), 201

@app.route('/lead/<string:city>', methods=['GET'])
def get_lead_by_city(city):
    leads = Lead.query.filter_by(location=city.upper()).order_by(Lead.budget.desc()).all()

    if not leads:
        return jsonify({"msg": "No hay registros con la ubicación solicitada"}), 404

    total_budget = sum(lead.budget for lead in leads)

    return jsonify({
        "total_budget": total_budget,
        "city": city,
        "filtered_leads": [lead.serialize() for lead in leads]
    }), 200




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
