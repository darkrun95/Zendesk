from . import main
from configuration import Configuration

from flask import render_template, url_for, flash, request
import requests
from math import ceil
import datetime
import json

@main.route("/", methods=['GET'])
def index():
	page_value = request.args.get("page_value")
	flash_value = request.args.get("flash")
	if not page_value:
		page_value = "1"

	flag = True

	request_url = "https://"+Configuration.subdomain+"/api/v2/tickets.json?per_page=" + str(Configuration.per_page_tickets) + "&page=" + page_value + "&sort_by=id"
	headers = {
		"Authorization": "Basic {0}".format(Configuration.encoded_string)
	}

	try:
		response = requests.get(request_url, headers=headers)
	
		if not response.ok:
			flash("Credentials Incorrect. Access denied.","error")
			flag = False
		else:
			if not flash_value or flash_value == 'True':
				flash("Tickets fetched successfully", "success")
			response = response.json()
			count_tickets = response['count']

			if count_tickets != 0:
				total_pages = ceil(count_tickets/Configuration.per_page_tickets)
			else:
				total_pages = 0
			page_tickets = len(response['tickets'])
	
		return render_template("index.html", 
								valid_response=True,
								response=response, 
								flag=flag, 
								total_tickets=count_tickets, 
								page_tickets=page_tickets,
								total_pages=range(1, total_pages+1)), 200
	except json.decoder.JSONDecodeError:
		return render_template("index.html", 
							   valid_response=False), 200
	except requests.exceptions.ConnectionError:
		return render_template("errors/503.html"), 503

@main.route("/ticket/<int:ticket_number>", methods=['GET'])
def ticket(ticket_number):
	try:
		ticket_url = "https://"+Configuration.subdomain+"/api/v2/tickets/"+str(ticket_number)+".json"
		
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		ticket_response = requests.get(ticket_url, headers=headers)
		ticket_response = ticket_response.json()

		user_id = ticket_response['ticket']['requester_id']
		user_url = "https://"+Configuration.subdomain+"/api/v2/users/"+str(user_id)+".json"
		user_response = requests.get(user_url, headers=headers)

		try:
			user_response = user_response.json()
			user_name = user_response['user']['name']
		except json.decoder.JSONDecodeError:
			user_name = "---"

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
		return render_template("errors/503.html"), 503