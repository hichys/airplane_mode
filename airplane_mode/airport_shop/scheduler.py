import frappe


#TODO Activate Contract when its start day is = Today
def activate_contracts_starting_today() -> list():
	target_date = frappe.utils.nowdate()
	contracts = frappe.db.get_list("Shop Contract",
	filters={
		"start_date" : target_date,
		"workflow_state" : "Approved"
	},
	fields=["name"]
	)
	if contracts :
		for c in contracts:
			frappe.db.set_value(
            "Shop Contract",
            c.name,
            "workflow_state",
            "Active"
        )
		frappe.db.commit()
		
	return contracts
#TODO make contracted Expired if its end_day < today , and auto renew is off
def expire_contracts_ended_yesterday():
    today = frappe.utils.nowdate()

    frappe.db.sql(
	"""
        UPDATE `tabShop Contract`
        SET status = 'Expired'
        WHERE end_date < %s
        AND status = 'Active'
        AND docstatus = 1
    """, today)

    frappe.db.commit()
	