from base64 import b64encode

class Configuration():
	"""Configuration settings"""
	SECRET_KEY = "arunpottekat"

	# API configurations for the application

	encoded_string = b"pottekatarun1995@gmail.com:something123"
	encoded_string = b64encode(encoded_string)
	encoded_string = encoded_string.decode("utf-8")
	subdomain = "something1995.zendesk.com"

	# Number of tickets to be displayed on each page.
	per_page_tickets = 25

	def init_app(app):
		return

class dev_configuration(Configuration):
	"""configuration in development mode"""
	DEBUG = True

class prod_configuration(Configuration):
	"""configuration in production mode"""
	DEBUG = False

configuration = {
	'default': dev_configuration,
	'production': prod_configuration 
}