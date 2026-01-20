# shop.py - Context provider for shop web templates
import frappe
from frappe import _

no_cache = 1

def get_context(context):
    # Get the shop document - it's automatically passed via context.doc for WebsiteGenerator
    if context.doc:
        doc = context.doc
        
        # Set page title
        context.title = f"{doc.shop_name} - Shop Details"
        
        # Format rent amount for display
        if doc.rent_amount:
            context.formatted_rent = frappe.format_value(doc.rent_amount, {'fieldtype': 'Currency'})
        
        # Format contract period for display
        if doc.contract_period:
            context.formatted_contract_period = frappe.utils.format_duration(doc.contract_period)
        
        # Get airport name if it's a linked field
        if doc.airport:
            context.airport_name = doc.airport
        
        # Set status class for styling
        status_classes = {
            'Available': 'status-available',
            'Rented': 'status-rented',
            'Under Maintenance': 'status-maintenance',
            'Reserved': 'status-reserved'
        }
        context.status_class = status_classes.get(doc.status, 'status-available')
