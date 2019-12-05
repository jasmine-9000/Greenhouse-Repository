from flask import render_template, request, Blueprint, send_from_directory, flash
import os 
import json

from flask_greenhouse.utils.warnings import flash_ts_warnings, flash_bms_warnings
main = Blueprint("main", __name__, static_folder="flask_greenhouse/static")


# a route is where we are going.
# we handle routes by having decorators.
# we don't need to know any of the backend stuff. The Flask API will handle this.

@main.route("/")# this is our main route decorator.
@main.route("/home")
def home():	
	ts_filepath = "flask_greenhouse/Tristar_instantaneous_file.json"
	bms_filepath = "flask_greenhouse/BMS_file.json"
	flash_ts_warnings(ts_filepath)
	flash_bms_warnings(bms_filepath)
	return render_template('home.html', title="Home")

@main.route("/about")
def about():
	return render_template('about.html', title="About")

@main.route("/test")
def test():
	return render_template("test.html")
	
@main.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(main.root_path, 'static'),
									'favicon.ico', mimetype='image/vnd.microsoft.icon')