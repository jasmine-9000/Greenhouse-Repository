from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(400)
def error_400(error):
	return render_template('errors/400.html'), 400
	
@errors.app_errorhandler(401)
def error_401(error):
	return render_template('errors/401.html'), 401

@errors.app_errorhandler(405)
def error_405(error):
	return render_template('errors/405.html'), 405

@errors.app_errorhandler(408)
def error_408(error):
	return render_template('errors/408.html'), 408
	
@errors.app_errorhandler(410)
def error_410(error):
	return render_template('errors/410.html'), 410
	
	
@errors.app_errorhandler(413)
def error_413(error):
	return render_template('errors/413.html'), 413	
	
@errors.app_errorhandler(414)
def error_414(error):
	return render_template('errors/414.html'), 414	
	
@errors.app_errorhandler(415)
def error_415(error):
	return render_template('errors/415.html'), 415	
	

	
@errors.app_errorhandler(429)
def error_429(error):
	return render_template('errors/429.html'), 429	
	
@errors.app_errorhandler(451)
def error_451(error):
	return render_template('errors/451.html'), 451	
	
	
@errors.app_errorhandler(502)
def error_502(error):
	return render_template('errors/502.html'), 502	
	
@errors.app_errorhandler(503)
def error_503(error):
	return render_template('errors/503.html'), 503	
	
@errors.app_errorhandler(504)
def error_504(error):
	return render_template('errors/504.html'), 504	
	