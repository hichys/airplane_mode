# Copyright (c) 2025, awad mohamed and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import nowdate,date_diff,add_days
import random
@frappe.whitelist()
def is_airplane_full(flight):
	tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight})
	if(len(tickets) == 0 ):
		return False
	
	flight_name = frappe.get_doc('Airplane Ticket',tickets[0].name).flight
	flight_airplane = frappe.get_doc('Airplane Flight',flight_name).airplane
	capacity  = frappe.get_doc('Airplane',flight_airplane).capacity
	if len(tickets) >  capacity:
		return True
	return False

#scheduler_events , Hourly and monthly
@frappe.whitelist()
def send_rent_reminder_email(shop_name):
	print("scheduler_events:send_rent_reminder_email")
	# 1. Permission check
	if not frappe.has_permission("Shop", "read", shop_name):
		frappe.throw("Not permitted")

	# 2. Load document safely
	shop = frappe.get_doc("Shop", shop_name)

	# 3. Check system setting
	if not is_rent_reminders_enabled():
		return {
			"status": "disabled",
			"message": "Rent reminders are disabled in system settings"
		}

	# 4. Validate email
	if not shop.tenant_email:
		frappe.throw("Tenant email is missing")

	# 5. Send email
	frappe.sendmail(
		recipients=[shop.tenant_email],
		subject="Rent Reminder",
		message=f"""
			Dear Tenant,<br><br>
			Your rent amount <b>{shop.rent_amount}</b> is due on <b>{nowdate()}</b>.<br><br>
			Regards,<br>
			Management
		""",
	)

	return {
		"status": "success",
		"email": shop.tenant_email,
		"rent_amount": shop.rent_amount
	}

def is_contract_expire_today(contract_doc) :
	"""
	return : all contracts thats expiring today
	"""
	today = frappe.utils.nowdate()
	diff = date_diff(contract_doc.end_date,today) 
	# print(diff)
	return diff == 0

def get_contract_remining_days(contract_doc) -> int:
	"""
	Return how many days are left until the contract finishes.
	If the contract already ended, return 0.
	"""
	today = nowdate()
	end_date = contract_doc.end_date

	if not end_date:
		return 0

	remaining_days = date_diff(end_date, today)

	return max(remaining_days, 0)

@frappe.whitelist()
def is_rent_reminders_enabled():
	return frappe.db.get_single_value("Shop Setting", "rent_reminders")

@frappe.whitelist()
def send_monthly_rent_reminders():
	if not is_rent_reminders_enabled():
		return {
			"status": "disabled",
			"message": "No reminders sent , Rent reminders are disabled in system settings"
		}
	shops = frappe.get_all("Shop")
	for shop in shops:
		send_rent_reminder_email(shop.name)
	return {
		"status": "success",
		"message": "Rent reminders sent successfully for all shops"
	}


@frappe.whitelist()
def contracts_ends_in_3_days():
	target_date = frappe.utils.add_days(frappe.utils.nowdate(), 3)

	return frappe.get_all(
		"Shop Contract",
		filters={
			"end_date": target_date,
			"docstatus": 1
		},
		fields=["name", "tenant", "end_date"]
	)


@frappe.whitelist()
def send_reminders_before_3_days() :
	contracts = contracts_ends_in_3_days()
	emails = []
	for doc in contracts:
		tenant_email = frappe.db.get_value("Tenant",doc.tenant,'email')
		emails.append(tenant_email)

	

@frappe.whitelist()
def get_random_shop_number() -> int:
    existing_numbers = frappe.get_all(
        "Shop",
        pluck="shop_number"
    )
    for _ in range(100): 
        number = random.randint(1, 9999)
        if number not in existing_numbers:
            return number

    return -1

@frappe.whitelist()
def is_shop_number_exits(new_shop_number : int) -> int:
	exists = frappe.db.exists('Shop',{"shop_number":new_shop_number})
	return exists

@frappe.whitelist()
def check_contract_payment():
	shop_list = frappe.get_all(
		"Shop Contract",
		filters= {"docstatus" : 1}
		)
	print(shop_list)

@frappe.whitelist()
def sentry_test():
    frappe.log_error(
		"title",
		"Message - A"
	)
	