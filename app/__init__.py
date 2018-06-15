from flask import Flask
from configuration import configuration

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(configuration[config_name])
	configuration[config_name].init_app(app)

	from .main import main
	app.register_blueprint(main)

	return app