# Copyright (c) 2025, awad mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import formatdate, format_time
from frappe.model.document import Document

#on submit change the status of the airplane to "Completed"
class AirplaneFlight(WebsiteGenerator,Document):
	def on_submit(self):
		self.status = "Completed"
	def get_context(self, context):
		# Get airplane and airline details for individual flight pages
		if self.airplane:
			airplane = frappe.get_doc("Airplane", self.airplane)
			airline = frappe.get_doc("Airline", airplane.airline)
			context.airline_name = airline.name
		
		# Format date
		if self.date_of_departure:
			context.formatted_date = formatdate(self.date_of_departure, "d MMMM, YYYY")
		
		# Format time
		if self.time_of_departure:
			context.formatted_time = format_time(self.time_of_departure, "HH:mm:ss")
		
		# Format duration
		if self.duration:
			hours = self.duration // 3600
			minutes = (self.duration % 3600) // 60
			if hours > 0:
				context.formatted_duration = f"{hours}h {minutes}m"
			else:
				context.formatted_duration = f"{minutes}m"
		
		# Create route display
		if self.route:
			context.route_display = self.route
		else:
			context.route_display = f"{self.source_airport_code} → {self.destination_airport_code}"
		
		return context
