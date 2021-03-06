import unittest
import requests
from flask import Flask
from flask_testing import TestCase
from configuration import Configuration

class TestCases(TestCase):
	"""
	Test Cases for Zendesk Ticket Viewer Application
	"""
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		return app

	# Check whether API's are up, by checking the response code.
	def test_check_api(self):
		page_value = "1"
		request_url = "https://" + \
					  Configuration.subdomain + \
					  "/api/v2/tickets.json?per_page=" + str(Configuration.per_page_tickets) + \
					  "&page=" + page_value + \
					  "&sort_by=id"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		response = requests.get(request_url, headers=headers)
		self.assertEqual(response.status_code, 200)

		ticket_number = 1
		ticket_url = "https://" + \
					 Configuration.subdomain + \
					 "/api/v2/tickets/" + \
					 str(ticket_number)+".json"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		ticket_response = requests.get(ticket_url, headers=headers)
		self.assertEqual(ticket_response.status_code, 200)
		return

	# Check if each page has less than or equal to "per_page" tickets
	def test_correct_ticket_count(self):
		request_url = "https://" + \
					  Configuration.subdomain + \
					  "/api/v2/tickets.json?per_page=" + str(Configuration.per_page_tickets) + \
					  "&sort_by=id"

		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		response = requests.get(request_url, headers=headers)
		response = response.json()
		next_page = response['next_page']

		while next_page:
			if len(response['tickets']) > 25:
				raise Exception("Invalid Page Tickets")

			response = requests.get(next_page, headers=headers)
			response = response.json()
			next_page = response['next_page']
		return

	# Checking the sample ticket, whether ticket fetched matches the id for the ticket.
	def test_valid_ticket(self):
		ticket_number = 1
		ticket_url = "https://" + \
					 Configuration.subdomain + \
					 "/api/v2/tickets/" + \
					 str(ticket_number)+".json"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		ticket_response = requests.get(ticket_url, headers=headers)
		ticket_response = ticket_response.json()
		self.assertEqual(ticket_response['ticket']['subject'], "Sample ticket: Meet the ticket")
		return

if __name__ == '__main__':
	unittest.main()

