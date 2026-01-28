import frappe
from frappe.utils import add_days, nowdate
# from frappe import logger

def schedule_contract_reminders():
	frappe.enqueue(
		"airplane_mode.airport_shop.utils.reminders.contract_expire_soon",
		queue="long"
	)
def schedule_rent_reminders()  -> None:
	frappe.enqueue(
		"airplane_mode.airport_shop.utils.reminders.send_rent_reminders",
		queue="long"
	)
def schedule_contract_starting_soon_reminders():
	frappe.enqueue(
		"airplane_mode.airport_shop.utils.reminders.contract_starting_soon_reminders",
		days_before = 3,
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


# send reminders before 3 days 
def contract_starting_soon_reminders(before_days=3):
	"""
		send emails to tenant about contracts starting soon 

	"""
	target_date = add_days(nowdate(), before_days)
	contracts = frappe.get_all(
		"Shop Contract",
		filters={
			"start_date": target_date,
			"docstatus": 1,
			"workflow_state": "Approved",
		},
		fields=["name", "tenant", "shop"]
	)
	for c in contracts:
		tenant_email = frappe.db.get_value(
			"Tenant",
			c.tenant,
			"email"
		)
		if tenant_email:	
			frappe.sendmail(
				recipients=[tenant_email],
				subject=f"Shop Contract Starting in {before_days} days",
				message=f"""
				<p>Your shop contract <b>{c.name}</b> for shop <b>{c.shop}</b>
				will start in <b>{before_days} days</b>.</p>
				<p>Thanks for your Trust.</p>
				"""
			)
		else :
			#TODO log missing emails
			pass
def contract_expire_soon():
	logger = frappe.logger("contract_reminders")

	logger.info("=== Running contract reminder job ===")

	target_date = add_days(nowdate(), 3)
	logger.info(f"Target expiry date: {target_date}")
	contracts = frappe.get_all(
		"Shop Contract",
		filters={
			"end_date": target_date,
			"docstatus": 1,
			"workflow_state": "Active",
		},
		fields=["name", "tenant", "shop"]
	)

	logger.info(f"Contracts found: {len(contracts)}")
	print(f"Contracts found: {len(contracts)}")
	print(f"Contracts data: {contracts}")

	for c in contracts:
		tenant_email = frappe.db.get_value(
			"Tenant",
			c.tenant,
			"email"
		)

		if not tenant_email:
			logger.warning(
				f"Skipping contract {c.name} | Shop: {c.shop} | No tenant email"
			)
			continue

		logger.info(
			f"Sending reminder → "
			f"Contract: {c.name} | "
			f"Shop: {c.shop} | "
			f"Tenant: {c.tenant} | "
			f"Email: {tenant_email}"
		)

		frappe.sendmail(
			recipients=[tenant_email],
			subject="Shop Contract Expiry Reminder",
			message=f"""
			<p>Your shop contract <b>{c.name}</b> for shop <b>{c.shop}</b>
			will expire in <b>3 days</b>.</p>
			<p>Please contact management if you wish to renew.</p>
			"""
		)

	logger.info("=== Contract reminder job finished ===")
