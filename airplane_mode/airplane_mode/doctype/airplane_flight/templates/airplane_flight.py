# flight.py
import frappe
from frappe import _

def get_context(context):
    # Assume we get a flight doc
    flight_name = frappe.form_dict.get("flight")
    doc = frappe.get_doc("Airplane Ticket", flight_name)

    context.doc = doc
    context.route_display = f"{doc.source_airport_code} → {doc.destination_airport_code}" if doc.source_airport_code and doc.destination_airport_code else None
    context.airline_name = doc.airline_name

    # Format date and time
    context.formatted_date = frappe.utils.formatdate(doc.date_of_departure, "MMMM d, YYYY") if doc.date_of_departure else None
    context.formatted_time = frappe.utils.format_time(doc.time_of_departure) if doc.time_of_departure else None

    # Format duration into clean "2h 5m" format
    context.formatted_duration = format_duration(doc.duration) if doc.duration else None


def format_duration(duration):
    """
    Convert a Frappe duration string like '2.0h 5.0m' into '2h 5m'.
    Removes .0 decimals and handles 0 values.
    """
    if not duration:
        return None

    try:
        hours, minutes = duration.split(" ")
        hours = hours.replace(".0", "").replace("h", "")
        minutes = minutes.replace(".0", "").replace("m", "")

        result = ""
        if hours != "0":
            result += f"{hours}h"
        if minutes != "0":
            if result:
                result += " "
            result += f"{minutes}m"

        return result
    except Exception as e:
        frappe.log_error(f"Error formatting duration: {duration} - {str(e)}")
        return duration
