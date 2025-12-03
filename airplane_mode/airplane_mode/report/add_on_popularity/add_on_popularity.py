import frappe
from frappe import _

def execute(filters=None):
    return get_columns(), get_data()

def get_columns():
    return [
        {
            "label": _("Add-on"),
            "fieldname": "item",
            "fieldtype": "Link",
            "options": "Airplane Ticket Add-on Type",
            "width": 200
        },
        {
            "label": _("Sold Count"),
            "fieldname": "sold_count",
            "fieldtype": "Int",
            "width": 120
        }
    ]

def get_data():
    return frappe.db.sql("""
        SELECT
            item AS item,
            COUNT(name) AS sold_count
        FROM `tabAirplane Ticket Add-on Item`
        WHERE item IS NOT NULL AND item != ''
        GROUP BY item
        ORDER BY sold_count DESC
    """, as_dict=True)
