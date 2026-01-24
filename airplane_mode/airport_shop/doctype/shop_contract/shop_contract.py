# Copyright (c) 2026, awad mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days, today
from airplane_mode.airport_shop.notification import notification
class ShopContract(Document):
	def validate(self):
		self.validate_date_range()
		self.validate_no_overlap()
	def on_change(self):
		# Check if the state was changed to 'Active'
		# self.get_doc_before_save() allows comparing current vs previous values
		previous_doc = self.get_doc_before_save()
		if previous_doc and previous_doc.workflow_state != "Active" and self.workflow_state == "Active":
			notification.trigger_bell_notification(
				doctype="Shop Contract",
				docname=self.name,
				recipient="Administrator",
				message=f"Contract updated",
				subject= f'Contract : {self.name} is Activate Now'
			)

	def validate_date_range(self):
		if not self.start_date or not self.end_date:
			frappe.throw("Start Date and End Date are required")

		if getdate(self.end_date) < getdate(self.start_date):
			frappe.throw("End Date cannot be before Start Date")
	def validate_no_overlap(self):
		start = getdate(self.start_date)
		end = getdate(self.end_date)

		overlapping = frappe.db.sql(
			"""
			SELECT name, start_date, end_date
			FROM `tabShop Contract`
			WHERE shop = %s
			  AND docstatus = 1
			  AND name != %s
			  AND start_date <= %s
			  AND end_date >= %s
			LIMIT 1
			""",
			(self.shop, self.name or "", end, start),
			as_dict=True
		)

		if overlapping:
			c = overlapping[0]
			frappe.throw(
				f"""
				Contract overlaps with existing contract:
				<br><b>{c.name}</b>
				<br>From <b>{c.start_date}</b> to <b>{c.end_date}</b>
				""",
				title="Overlapping Contract"
			)



def update_contract_status() -> dict[str:str] :
	updated_contract = list()

	

	return updated_contract

def is_shop_rented_in_period(shop: str, start_date, end_date) -> bool:
	"""
	Check if a shop is rented in the given date range.
	"""

	# Validate inputs
	if not shop or not start_date or not end_date:
		return False

	# Normalize dates
	start_date = getdate(start_date)
	end_date = getdate(end_date)

	# Ensure correct order
	if end_date < start_date:
		frappe.throw("End date cannot be before start date")

	# overlap check
	result = frappe.db.sql(
		"""
		SELECT name
		FROM `tabShop Contract`
		WHERE shop = %s
		  AND docstatus = 1
		  AND start_date <= %s
		  AND end_date >= %s
		LIMIT 1
		""",
		(shop, end_date, start_date),
		as_dict=True
	)
	print(result)
	return bool(result)

def get_shop_availability(shop: str, from_date=None):

	from_date = getdate(from_date) if from_date else getdate(today())

	contracts = frappe.db.sql(
		"""
		SELECT start_date, end_date
		FROM `tabShop Contract`
		WHERE shop = %s
		  AND docstatus = 1
		  AND end_date >= %s
		ORDER BY start_date ASC
		""",
		(shop, from_date),
		as_dict=True
	)

	cursor = from_date

	for c in contracts:
		start = getdate(c.start_date)
		end = getdate(c.end_date)

		# GAP FOUND
		if start > cursor:
			return {
				"available_from": cursor,
				"available_to": add_days(start, -1)
			}

		# Move cursor forward
		cursor = max(cursor, add_days(end, 1))

	# No gaps → available after last contract
	return {
		"available_from": cursor,
		"available_to": "Open"
	}


