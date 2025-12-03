# Copyright (c) 2025, awad mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random

class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_addons()

	def remove_duplicate_addons(self):
		seen = set()
		unique_items = []

		# child table = self.items
		for row in self.items:
			if row.item not in seen:
				unique_items.append(row)
				seen.add(row.item)

		# replace child table with cleaned rows
		self.items = unique_items

	def before_submit(self):
		if self.status != "Boarded":
			raise frappe.ValidationError("Only tickets with status Boarded can be submitted.")

	def before_insert(self):
		# seat = <random-integer><random-capital-alphabet-from-A-to-E
		self.seat = f"{random.randint(1, 10)}{random.choice(['A', 'B', 'C', 'D', 'E'])}"
		
	
	def on_submit(self):
		self.db_set("status", "Completed")