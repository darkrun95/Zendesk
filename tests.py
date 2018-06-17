import unittest
import urllib
import requests
from flask import Flask
from flask_testing import TestCase
from configuration import Configuration

class TestCases(TestCase):
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		return app

	def test_check_api(self):
		page_value = "1"
		request_url = "https://"+Configuration.subdomain+"/api/v2/tickets.json?per_page=" + str(Configuration.per_page_tickets) + "&page=" + page_value + "&sort_by=id"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		response = requests.get(request_url, headers=headers)
		self.assertEqual(response.status_code, 200)

		ticket_number = 1
		ticket_url = "https://"+Configuration.subdomain+"/api/v2/tickets/"+str(ticket_number)+".json"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		ticket_response = requests.get(ticket_url, headers=headers)
		self.assertEqual(ticket_response.status_code, 200)
		return

	def test_flask_application_is_up_and_running(self):
		response = urllib.request.urlopen("http://localhost:5000")
		self.assertEqual(response.code, 200)
		return

	def test_valid_ticket(self):
		ticket_number = 1
		ticket_url = "https://"+Configuration.subdomain+"/api/v2/tickets/"+str(ticket_number)+".json"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		ticket_response = requests.get(ticket_url, headers=headers)
		ticket_response = ticket_response.json()
		self.assertEqual(ticket_response['ticket']['subject'], "Sample ticket: Meet the ticket")
		return

if __name__ == '__main__':
	unittest.main()

