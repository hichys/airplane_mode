# Copyright (c) 2025, awad mohamed and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Count"),
            "fieldname": "count",
            "fieldtype": "Int",
            "width": 150,
        },
    ]


def get_data():
    result = frappe.db.sql("""
        SELECT 
            airline,
            COUNT(name) AS count
        FROM `tabAirplane`
        GROUP BY airline
        ORDER BY airline
    """, as_dict=True)

    data = []
    for row in result:
        data.append([row.airline, row.count])

    return data
