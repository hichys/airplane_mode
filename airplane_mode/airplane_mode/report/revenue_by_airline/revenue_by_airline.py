import frappe
from frappe import _
from frappe.query_builder import DocType, Case, functions as fn
from pypika.terms import ValueWrapper 

def execute(filters=None):
    columns = get_columns()
    data = get_data()

    # Calculate Total Revenue safely
    total_revenue = sum((row.get('total_revenue') or 0) for row in data)

    # Summary (Visual cards at top)
    report_summary = [
        {
            "value": total_revenue,
            "label": _("Total Revenue"),
            "datatype": "Currency",
            "currency": "USD", 
            "indicator": "Green" if total_revenue > 0 else "Red"
        }
    ]

    # Chart (Uses data before any manual modification)
    chart = {
        "data": {
            "labels": [row['airline'] for row in data],
            "datasets": [
                {
                    "name": _("Revenue"),
                    "values": [row['total_revenue'] for row in data]
                }
            ]
        },
        "type": "donut",
        "height": 300
    }

    # Removed: The block that appended the "Total" row to the 'data' list.
    
    # Return in the correct order: columns, data, message, chart, report_summary
    return columns, data, None, chart, report_summary


def get_columns():
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200
        },
        {
            "label": _("Revenue"),
            "fieldname": "total_revenue",
            "fieldtype": "Currency",
            "width": 150
        },
    ]


def get_data():
    Airline = DocType("Airline")
    Airplane = DocType("Airplane")
    Flight = DocType("Airplane Flight")
    Ticket = DocType("Airplane Ticket")

    query = (
        frappe.qb.from_(Airline)
        .left_join(Airplane).on(Airline.name == Airplane.airline)
        .left_join(Flight).on(Airplane.name == Flight.airplane)
        .left_join(Ticket).on(Flight.name == Ticket.flight)
        .select(
            Airline.name.as_("airline"),
            ValueWrapper("USD").as_("currency"), 
            fn.IfNull(
                fn.Sum(
                    Case()
                    .when(Ticket.docstatus == 1, Ticket.total_amount)
                    .else_(0)
                ), 
                0
            ).as_("total_revenue")
        )
        .groupby(Airline.name)
        .orderby(fn.Sum(Ticket.total_amount), order=frappe.qb.desc)
    )

    return query.run(as_dict=True)