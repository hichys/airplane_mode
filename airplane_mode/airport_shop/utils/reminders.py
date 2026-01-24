import frappe
from frappe.utils import add_days, nowdate

def schedule_contract_reminders():
	frappe.enqueue(
		"airplane_mode.airport_shop.utils.reminders.send_contract_reminders",
		queue="long"
	)
def schedule_rent_reminders()  -> None:
	frappe.enqueue(
		"airplane_mode.airport_shop.utils.reminders.send_rent_reminders",
		queue="long"
	)

def send_rent_reminders() -> None :
	"""
		send rent reminders for contract that ending today
		and tell them if the contract will be auto renewed or not
	"""
	frappe.logger().info("Sending Rent Reminders bg jobs")
	target_date = frappe.utils.nowdate()

	contracts = frappe.get_all(
		"Shop Contract",
		filters = {
			"end_date" : target_date,
			"workflow_status": "Active",
		},
		fields= ["name","tenant","auto_renew"]
	)
	for c in contracts:
		tenant_email = frappe.db.get_value(
			"Tenant",
			c.tenant,
			"email"
		)

		if tenant_email:
			if not c.auto_renew :
				frappe.sendmail(
					recipients=[tenant_email],
					subject="Shop Contract Rent Reminder",
					message=f"""
					Your shop contract <b>{c.name}</b> will expire in Today.
					Please Pay in time .
					Please contact management if you want to renew.
					"""
				)
			else :
				frappe.sendmail(
					recipients=[tenant_email],
					subject="Shop Contract Rent Reminder",
					message=f"""
					Your shop contract <b>{c.name}</b> will expire in Today.
					Please Pay in time, your contract will be auto renewed as requested before
					Please contact management if you want to cancel or have any question .
					thanks , 
					Sales Team.
					"""
				)


def send_contract_reminders():
	frappe.logger().info("Running contract reminder job")
	target_date = add_days(nowdate(), 3)

	contracts = frappe.get_all(
		"Shop Contract",
		filters={
			"end_date": target_date,
			"docstatus": 1
		},
		fields=["name", "tenant"]
	)

	for c in contracts:
		tenant_email = frappe.db.get_value(
			"Tenant",
			c.tenant,
			"email"
		)

		if tenant_email:
			frappe.logger().info("Running contract reminder job email :",tenant_email)
			frappe.sendmail(
				recipients=[tenant_email],
				subject="Shop Contract Expiry Reminder",
				message=f"""
				Your shop contract <b>{c.name}</b> will expire in 3 days.
				Please contact management if you want to renew.
				"""
			)

