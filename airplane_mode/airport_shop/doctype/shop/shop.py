# Copyright (c) 2026, awad mohamed and contributors
# For license information, please see license.txt

# Shop is considered an Assest
# Each shop will have corssponding Item created automaticly when the shop doc is submited
# the new item will be in form off > itemcode = shopcode item_name = shop_name
# if code conflic with other item mix between item name and item code will be used for item_code and item name is shop name



from sys import exception
from airplane_mode import api
import frappe
from frappe.website.website_generator import WebsiteGenerator
from datetime import datetime

class Shop(WebsiteGenerator):
	is_asset_ : bool | None
	def validate(self):
		self.validate_duplicate_shop_number()
		if not self.route :
			frappe.throw("Please Set Shop Route !")
		if self.is_asset_:
			if not self.shop_asset :
				frappe.throw("Please provide asset for this shop or uncheck Is Asset!")
			
			
	def on_submit(self):
		#TODO create item for sales invoice 
		#TODO 
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
		if self.docstatus == 1:
			amount_before_save = self.get_doc_before_save().rent_amount
			if(amount_before_save != self.rent_amount):
				increase_rent = amount_before_save < self.rent_amount
				frappe.msgprint(
					f"Will Notify Tenant that has Approved Contracts for this shop {abs(amount_before_save - self.rent_amount)}",
				"Notification Plane")

	# def create_item_for_shop(name,code) :
	# 	try:
	# 		item = frappe.new_doc("Item");
	# 		item.item_code = str(code)
	# 		item.item_name = str(name)
	# 		item.item_group = "Rental"
	# 		item.stock_uom = "Unit"
	# 		item.asset_category = "Airport Shop"
	# 		item.is_fixed_asset = 1
	# 		item.is_stock_item = 0
	# 		item.is_purchase_item = 0
	# 		new_item_code = item.save()
	# 		frappe.db.commit()
	# 		return new_item_code
	# 	except exception as e:
	# 		return False;
		
