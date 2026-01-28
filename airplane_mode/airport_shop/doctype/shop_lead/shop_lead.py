# Copyright (c) 2026, awad mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopLead(Document):
	def validate(self):
		if self._is_locked and self.get_db_value("_is_locked") and self.docstatus != 1:
			frappe.throw("This document is locked, Unlock it First to modifiy it")

	def isLeadLocked(self):
		return self._is_locked
	
@frappe.whitelist()
def make_contract(source_name):
	def set_missing_values(source, target):
		target.start_date = frappe.utils.today()
		target.shop_lead = source.name
		# target.tenant = source.tenant
		# target.shop = source.shop

	doc = frappe.model.mapper.get_mapped_doc(
		"Shop Lead",
		source_name,
		{
			"Shop Lead": {
				"doctype": "Shop Contract",
				"field_map": {
					"shop": "shop",
					"full_name": "tenant",
					"email": "tenant_email",
				}
			}
		},
		postprocess=set_missing_values
	)

	return doc
