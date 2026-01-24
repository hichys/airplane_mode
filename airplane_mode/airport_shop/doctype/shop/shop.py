# Copyright (c) 2026, awad mohamed and contributors
# For license information, please see license.txt

from airplane_mode import api
import frappe
from frappe.website.website_generator import WebsiteGenerator
from datetime import datetime

class Shop(WebsiteGenerator):
	def validate(self):
		self.validate_duplicate_shop_number()
		if not self.route :
			frappe.throw("Please Set Shop Route !")
	def on_submit(self):
		
		# send Email Every month on the 1st day of the month in background jobs
		isRemindersEnabled = frappe.db.get_single_value("Shop Setting", "rent_reminders")
		if isRemindersEnabled:
			# send Email Every month on the 1st day of the month in background jobs
			frappe.enqueue(
				"airplane_mode.api.send_rent_reminder_email",
				shop_name=self.name,
				queue="default"
			)
		else:
			frappe.msgprint("Info : Rent reminders are not enabled in the system settings");
		
	def before_insert(self):
		if not self.shop_number:
			self.shop_number = api.get_random_shop_number()
		if not self.route and self.shop_number :
			self.route = "Shop-" + str(self.shop_number)
	def validate_duplicate_shop_number(self):
		if not self.shop_number:
				return

		exists = frappe.db.exists(
				"Shop",
				{
					"shop_number": self.shop_number,
					"name": ["!=", self.name]
				}
			)

		if exists:
			frappe.throw("Shop Number already exists")

	def on_change(self):
		#TODO Send Notification to Tenant About Price Change
		amount_before_save = self.get_doc_before_save().rent_amount
		if(amount_before_save != self.rent_amount):
			increase_rent = amount_before_save < self.rent_amount
			frappe.msgprint(
				f"Will Notify Tenant that has Approved Contracts for this shop {abs(amount_before_save - self.rent_amount)}",
			"Notification Plane")