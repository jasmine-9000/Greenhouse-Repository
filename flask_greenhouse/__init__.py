# libraries necessary for deployment of our application.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_datepicker import datepicker
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


#initialize our "app" object of Flask type.
app = Flask(__name__)
#confirgure it with our secret key.
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



import time,json
# Template filters
@app.template_filter('ctime')
def timectime(s):
    return time.ctime(s) # datetime.datetime.fromtimestamp(s)

@app.template_filter('json_unpacker')
def json_unpacker(s):
	return json.load(s)

# initialize database
db = SQLAlchemy(app)

#initialize datepicker
datepicker(app)

# initialize Administration viewer.
admin = Admin(app) 

# initialize Login Manager
login_manager = LoginManager(app)

# initialize our Bcrypt encryption service.
bcrypt = Bcrypt(app)


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

