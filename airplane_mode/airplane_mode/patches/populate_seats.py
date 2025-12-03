# update seat field in airplane ticket doctype with random seat
import frappe
import random

def execute():
    # get only names, not full docs
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ["is", "not set"]}, fields=["name"])

    for t in tickets:
        seat = f"{random.randint(1, 10)}{random.choice(['A', 'B', 'C', 'D', 'E'])}"

        frappe.db.set_value("Airplane Ticket", t["name"], "seat", seat)

    frappe.db.commit()
