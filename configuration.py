from base64 import b64encode

class Configuration():
	"""Configuration settings"""
	SECRET_KEY = "arunpottekat"
	encoded_string = b64encode(b"pottekatarun1995@gmail.com:something123")
	encoded_string = encoded_string.decode("utf-8")
	per_page_tickets = 25
	subdomain = "something1995.zendesk.com"

	def init_app(app):
		pass		

class dev_configuration(Configuration):
	"""configuration in development mode"""
	DEBUG = True

configuration = {
	'default': dev_configuration
}