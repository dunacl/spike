# Imports
import os
import time
import math
import requests
import json
import jsonschema
from jsonschema import validate
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
# SQLite bc time is not enough ¯\_(ツ)_/¯
import sqlite3

# Setup
DBNAME = './rose.db'

if os.getenv('MODE') == "PROD":
  load_dotenv('.env_prod')
else:
  load_dotenv('.env_dev', verbose=True)

def xprint(*args):
  if os.getenv('MODE') == "DEV":
    print(*args)


xprint("Running as", os.getenv('MODE'))

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)

users = {
  "rose": generate_password_hash("averycomplexpassword")
}

address_schema = {
    "type": "object",
    "properties": {
        "fromStreet": {"type": "string"},
        "fromNumber": {"type": "string"},
        "fromCity": {"type": "string"},
        "fromCountry": {"type": "string"},
    },
}

# Simple access check
@auth.verify_password
def verify_password(username, password):
  if username in users and check_password_hash(users.get(username), password):
    return username

# check json structure and keys are valid
def validate_structure(json_data):
  try:
    validate(instance=json_data, schema=address_schema)
  except jsonschema.exceptions.ValidationError as err:
    xprint("Error", err)
    return False

  valid_keys = ['fromStreet', 'fromNumber', 'fromCity', 'fromCountry']
  for key in json_data.keys():
    if key not in valid_keys:
      return False
  return True

def get_coordinates(address):
  url_base = "https://nominatim.openstreetmap.org/search?q="
  url_querystring = address["fromNumber"]+"+"+address["fromStreet"]+"+"+address["fromCity"]+"+"+address["fromCountry"]+"&format=geojson"
  url = url_base+url_querystring
  headers     = {'Accept': 'application/json'} 
  s = requests.get(url,headers = headers)
  return json.loads(s.text)

# as some user in forum said
# using https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
def distance_points(lat1, lon1, lat2, lon2):
  R = 6373.0
  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = R * c
  return distance

def set_records(data):
  insert_id = None
  try:
    today = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    # pretty ugly query
    strquery = "INSERT INTO address_queries(datequery, fromStreet, fromNumber, fromCity, fromCountry, toStreet, toNumber, toCity, toCountry) VALUES('"+str(today)+"','"+data["address1"]["fromStreet"]+"','" +data["address1"]["fromNumber"]+"','"+data["address1"]["fromCity"]+"','"+data["address1"]["fromCountry"]+"','" +data["address2"]["fromStreet"]+"','"+data["address2"]["fromNumber"]+"','"+data["address2"]["fromCity"]+"','" +data["address2"]["fromCountry"]+"')"
    cursor.execute(strquery)
    insert_id = cursor.lastrowid
    conn.commit()
    conn.close()
  except Exception as e:
    print("Some error in db at insert", e)
  return insert_id

def update_records(insert_id, lat1, lon1, lat2, lon2, distance):
  try:
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    # pretty ugly query
    strquery = "UPDATE address_queries SET distance='"+distance+"', fromLatitude='"+lat1+"', fromLongitude='"+lon1+"', toLatitude='"+lat2+"', toLongitude='"+lon2+"' WHERE queryid='"+insert_id+"'"
    cursor.execute(strquery)
    conn.commit()
    conn.close()
  except Exception as e:
    print("Some error in db at update", e)

def get_db_records():
  result = None
  try:
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    # pretty ugly query
    strquery = "SELECT * FROM address_queries"
    cursor.execute(strquery)
    conn.commit()
    result = cursor.fetchall()
    columns = [d[0] for d in cursor.description]
    ret_data = [dict(zip(columns, row)) for row in result]
    conn.close()
  except Exception as e:
    print("Some error in db", e)

  return json.dumps(ret_data)

def calculate_distance(data):
  # dumb way to validate json structure
  valid_json = validate_structure(data["address1"])
  if not valid_json:
    return '{"result":"invalid", "detail": "json address 1 structure not compliant"}', 400
  valid_json = validate_structure(data["address2"])
  if not valid_json:
    return '{"result":"invalid", "detail": "json address 2 structure not compliant"}', 400

  # after validation, we insert in db
  insert_id = set_records(data)

  coordinates1 = get_coordinates(data["address1"])
  coordinates2 = get_coordinates(data["address2"])

  if not coordinates1["features"][0]["geometry"]["coordinates"] or not coordinates2["features"][0]["geometry"]["coordinates"]:
    return '{"result":"failed", "detail": "address not found"}', 401

  # each is a list: 0 longitude, 1 latitude
  set1 = coordinates1["features"][0]["geometry"]["coordinates"]
  set2 = coordinates2["features"][0]["geometry"]["coordinates"]

  distance = distance_points(set1[1], set1[0], set2[1], set2[0])

  # Update db
  if insert_id is not None:
    update_records(str(insert_id), str(set1[1]), str(set1[0]), str(set2[1]), str(set2[0]), str(distance))

  result = {"result":"OK", "detail": distance, "unit": "kms"}
  return result, 200

@app.route('/calculate-distance', methods=['POST'])
@auth.login_required
def get_dist():
  if len(request.data) > 0:
    data = json.loads(request.data.decode('utf-8'))
    return calculate_distance(data)
  else:
    return '{"result":"invalid", "detail": "no data in request"}', 400

@app.route('/records', methods=['GET'])
@auth.login_required
def records():
  return get_db_records()

@app.route('/ping')
def index():
  return '{"result":"pong"}'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3001)