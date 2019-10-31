from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_datepicker import datepicker

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)
datepicker(app)

#import our blueprints.
from flask_greenhouse.main.routes import main
from flask_greenhouse.bms.routes import bms
from flask_greenhouse.tristar.routes import tristar
from flask_greenhouse.sensors.routes import sensor_nodes

app.register_blueprint(main)
app.register_blueprint(bms)
app.register_blueprint(tristar)
app.register_blueprint(sensor_nodes)


