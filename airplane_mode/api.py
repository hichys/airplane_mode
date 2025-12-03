# Copyright (c) 2025, awad mohamed and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

@frappe.whitelist()
def is_airplane_full(flight):
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight})
    if(len(tickets) == 0 ):
        return True
    
    flight_name = frappe.get_doc('Airplane Ticket',tickets[0].name).flight
    flight_airplane = frappe.get_doc('Airplane Flight',flight_name).airplane
    capacity  = frappe.get_doc('Airplane',flight_airplane).capacity
    if len(tickets) >  capacity:
        return True
    return False