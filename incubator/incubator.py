from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'incubator.db'),
    SECRET_KEY='alskdjlkfjakjupo32948u',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(app.config['DATABASE'])

api = Api(app)

db = SQLAlchemy(app)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return 'Temp: {}, Humidity: {}'.format(self.temperature, self.humidity)


class AddReading(Resource):
    def get(self):
        return {'hello': 'get'}

    def post(self):
        import pdb; pdb.set_trace()
        r = Reading(request.form['temperature'], request.form['humidity'])
        db.session.add(r)
        db.session.commit()
        return {'hello': 'post'}

api.add_resource(AddReading, '/add')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
