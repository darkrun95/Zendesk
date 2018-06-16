from app.main import main
from configuration import Configuration

from flask import render_template, url_for, flash, request
import requests
from math import ceil
import json

@main.route("/", methods=['GET'])
def index():
	# Flash message display flag
	flag = True

	# Pagination range values
	upper_limit = None
	lower_limit = None
	upper_limit_val = None
	lower_limit_val = None

	# Maximum page value options to be displayed to the user at each page.
	pagination_length = 3

	page_value = request.args.get("page_value")
	flash_value = request.args.get("flash")
	if not page_value:
		page_value = "1"

	try:
		request_url = "https://"+Configuration.subdomain+"/api/v2/tickets.json?per_page=" + str(Configuration.per_page_tickets) + "&page=" + page_value + "&sort_by=id"
		headers = {
			"Authorization": "Basic {0}".format(Configuration.encoded_string)
		}

		# REST GET call for fetching tickets for the current user.
		response = requests.get(request_url, headers=headers)
		page_value = int(page_value)

		if not response.ok:
			flash("Credentials Incorrect. Access denied.","error")
			flag = False
		else:
			if not flash_value or flash_value == 'True':
				flash("Tickets fetched successfully", "success")
			response = response.json()

			# Total tickets for the given user.
			count_tickets = response['count']

			# Pagination:
			# Finding the lower and upper limits at each page value
			# with an interval of "pagination_length" value
			# and keeping lower_limit_val as the current page value.
			if count_tickets != 0:
				total_pages = ceil(count_tickets / Configuration.per_page_tickets)
				lower_limit_val = page_value
				upper_limit_val = page_value + pagination_length - 1

				if lower_limit_val != 1:
					lower_limit = True

				if upper_limit_val > total_pages:
					upper_limit_val = total_pages
				else:
					upper_limit = True
				page_range = range(lower_limit_val, upper_limit_val + 1)
			else:
				total_pages = 0

			# Total tickets displayed on the current page.
			page_tickets = len(response['tickets'])
	
		return render_template("index.html", 
								valid_response=True,
								response=response, 
								flag=flag, 
								total_tickets=count_tickets, 
								page_tickets=page_tickets,
								upper_limit=upper_limit,
								lower_limit=lower_limit,
								upper_limit_val=upper_limit_val,
								lower_limit_val=lower_limit_val,
								page_range=page_range), 200

	except json.decoder.JSONDecodeError:
		# JSON error in case of invalid format of data being fetched
		# during REST call.
		return render_template("index.html", 
							   valid_response=False), 200
	except requests.exceptions.ConnectionError:
		# Exception due to API not being available or network failure.
		return render_template("errors/503.html"), 503