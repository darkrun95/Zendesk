from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(error):
	return render_template("errors/404.html"), 404

@main.app_errorhandler(503)
def service_unavailable(error):
	return render_template("errors/503.html"), 503