from app.main import main
from configuration import Configuration

from flask import render_template, url_for, flash, request
import requests
from math import ceil
import datetime
import json

@main.route("/ticket/<int:ticket_number>", methods=['GET'])
def ticket(ticket_number):
	try:
		# Fetch particular ticket details 
		ticket_url = "https://"+Configuration.subdomain+"/api/v2/tickets/"+str(ticket_number)+".json"
		
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		ticket_response = requests.get(ticket_url, headers=headers)
		ticket_response = ticket_response.json()

		# Fetch user details for the requested ticket.
		user_id = ticket_response['ticket']['requester_id']
		user_url = "https://"+Configuration.subdomain+"/api/v2/users/"+str(user_id)+".json"
		user_response = requests.get(user_url, headers=headers)

		try:
			# If user not present then display placeholder text.
			user_response = user_response.json()
			user_name = user_response['user']['name']
		except json.decoder.JSONDecodeError:
			user_name = "---"

		# Date time formating
		created_at = ticket_response['ticket']['created_at']
		created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
		created_at = created_at.strftime("%H:%I %p, %Y-%m-%d")

		page_number = ceil(ticket_number/Configuration.per_page_tickets)

		return render_template("ticket.html", 
							   ticket_information=ticket_response,
							   user_name=user_name,
							   created_at=created_at,
							   page_number=page_number), 200
	except requests.exceptions.ConnectionError:
		# Exception due to API not being available or network failure.
		return render_template("errors/503.html"), 503