from flask import Flask, request, g, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

import os, requests, time

sensor_url = ""
app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'incubator.db'),
    SECRET_KEY='alskdjlkfjakjupo32948u',))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(app.config['DATABASE'])

api = Api(app)

db = SQLAlchemy(app)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __init__(self, temperature, humidity, date=None):
        self.temperature = temperature
        self.humidity = humidity
        if date is None:
            date = datetime.now()
        self.date = date

    def __repr__(self):
        # This is nasty, but it beats writing a full JSON encoder.
        date = '"' + str(self.date.strftime("%H:%M:%S")) + '"'
        ret = '{' + '"date": ' + date + ',' + '"temperature": ' + str(self.temperature) + ',' + '"humidity": ' + str(self.humidity) + '}'
        return ret


@app.route("/")
def show_readings():
    readings = Reading.query.order_by('id desc').limit(20).all()
    return render_template('show_readings.html', readings=readings)

class Register(Resource):
    def post(self):
        if 'url' in request.form:
            global sensor_url
            sensor_url = request.form['url']
            return "registered"
        return "error"

class ReadSensor(Resource):
    def post(self):
        if sensor_url is "":
            return "{}: no URL".format(datetime.now())
        return sensor_read(sensor_url)

api.add_resource(ReadSensor, '/readsensor')
api.add_resource(Register, '/register')

def sensor_read(url):
    print ("{}: reading from {}".format(datetime.now(), url))
    try:
        req = requests.get(url, timeout=5)
    except:
        print("Error Reading from Sensor, requests")
        return "failed"
    if req.status_code == 200:
        print(req.text)
        try:
            obj = req.json()
            temp = obj['temperature']
            hum = obj['humidity']
        except:
            return "Error reading from sensor"
        r = Reading(temp, hum)
        db.session.add(r)
        db.session.commit()
        return obj
    return "Timed Out"


def main():
    app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
    main()

'''
def sensor_read_worker():
    print ("starting thread {}".format(threading.get_ident()))
    while True:
        print ("{}: sleeping".format(datetime.now()))
        time.sleep(DELAY)
        if sensor_url is "":
            print ("{}: no URL will retry in 10".format(datetime.now()))
            continue;
        sensor_read(sensor_url)

class Sensor(db.Model):
    url = db.Column(db.String, primary_key=True)

class AddReading(Resource):
    def get(self):
        return {'hello': 'get'}

    def post(self):
        r = Reading(request.form['temperature'], request.form['humidity'])
        db.session.add(r)
        db.session.commit()
        return {'return': 'thanks'}

api.add_resource(AddReading, '/add')
'''
