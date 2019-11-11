#libraries necessary for deployment of our application.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_datepicker import datepicker

#initialize our "app" object of Flask type.
app = Flask(__name__)
#confirgure it with our secret key.
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# initialize database
db = SQLAlchemy(app)
#initialize datepicker
datepicker(app)

#import our blueprints. These are our route handlers in package form.
# all our route handlers will be in "flask_greenhouse/<path>/routes.py"
# look there for details on how we handle our routes.
from flask_greenhouse.main.routes import main
from flask_greenhouse.bms.routes import bms
from flask_greenhouse.tristar.routes import tristar
from flask_greenhouse.sensors.routes import sensor_nodes
from flask_greenhouse.errors.handlers import errors

#register our blueprints.
app.register_blueprint(main)
app.register_blueprint(bms)
app.register_blueprint(tristar)
app.register_blueprint(sensor_nodes)
app.register_blueprint(errors)

