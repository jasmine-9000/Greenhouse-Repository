from flask import render_template, request, Blueprint
from flask_greenhouse.forms import Date_Form

tristar = Blueprint("tristar", __name__)



@tristar.route("/Tristar", methods=["POST", "GET"])
def Tristar():
	form = Date_Form()
	return render_template('Tristar.html', title="Tristar Data", form=form)




#post BMS JSON data to this address.
@tristar.route("/Tristar/post-json", methods=["POST"]) #get requests will be blocked.
def Tristar_Post():
	req_data = request.get_json()
	new_Tristar_entry = TristarDataentry(JSON_data=req_data)
	db.session.add(new_Tristar_entry)
	db.session.commit()
	return "your data has been received."