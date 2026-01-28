# Copyright (c) 2026, awad mohamed
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": "Airport",
			"fieldname": "airport",
			"fieldtype": "Link",
			"options": "Airport",
			"width": 200
		},
		{
			"label": "Available for Lease",
			"fieldname": "available",
			"fieldtype": "Int",
			"width": 160
		},
		{
			"label": "Occupied Shops",
			"fieldname": "occupied",
			"fieldtype": "Int",
			"width": 150
		},
		{
			"label": "Total Shops",
			"fieldname": "total",
			"fieldtype": "Int",
			"width": 120
		}
	]


def get_data(filters):
	conditions = "WHERE docstatus = 1"
	values = {}

	if filters and filters.get("airport"):
		conditions += " AND airport = %(airport)s"
		values["airport"] = filters.get("airport")

	return frappe.db.sql(f"""
		SELECT
			airport,

			SUM(
				CASE
					WHEN status = 'Available' THEN 1
					ELSE 0
				END
			) AS available,

			SUM(
				CASE
					WHEN status IN ('Rented', 'Reserved', 'Under Maintenance') THEN 1
					ELSE 0
				END
			) AS occupied,

			COUNT(name) AS total

		FROM `tabShop`
		{conditions}
		GROUP BY airport
	""", values, as_dict=1)


