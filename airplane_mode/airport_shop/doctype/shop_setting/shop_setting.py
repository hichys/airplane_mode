# Copyright (c) 2026, awad mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopSetting(Document):
	def on_change(self):
		if self.rent_reminders:
			frappe.msgprint("Info : Reminders are enabled");
		else:
			frappe.msgprint("Info : Reminders are disabled");


