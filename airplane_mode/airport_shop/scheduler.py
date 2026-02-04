import frappe
from sentry_sdk.crons import capture_checkin
from sentry_sdk.crons.consts import MonitorStatus
from frappe.utils import getdate, add_days, today,date_diff, nowdate
def automated_autorenew_shop_contracts() -> list:
	checkin_id = capture_checkin(
		monitor_slug="automated_autorenew_shop_contracts",
		status=MonitorStatus.IN_PROGRESS,
	)

	try:
		target_date = frappe.utils.nowdate()

		contracts = frappe.db.get_list(
			"Shop Contract",
			filters={
				"end_date": target_date,
				"auto_renew": 1,
				"workflow_state": "Active",
			},
			fields=["name"],
		)

		# Check if its already renewed
		contracts = [c for c in contracts if not frappe.db.exists(
			"Shop Contract",
			{
				"renewed_from": c.name,
			}
		)]

		for c in contracts:
			old_contract = frappe.get_doc("Shop Contract",c.name)
			new_contract = frappe.copy_doc(old_contract)
			new_contract.name = None
			new_contract.modified = None
			new_contract.modified_by = None
			new_contract.renewed_from = old_contract.name
			new_contract.start_date = frappe.utils.add_days(today(), 1)
			old_contract_period_in_days = frappe.utils.date_diff(old_contract.end_date,old_contract.start_date) + 1
			new_contract.end_date = frappe.utils.add_days( new_contract.start_date , old_contract_period_in_days)
			new_contract.workflow_state = None
			new_contract.insert()
			#TODO make shop field in new contract read only after insert


		frappe.db.commit()

		capture_checkin(
			monitor_slug="automated_autorenew_shop_contracts",
			check_in_id=checkin_id,
			status=MonitorStatus.OK,
		)

		return contracts

	except Exception:
		capture_checkin(
			monitor_slug="automated_autorenew_shop_contracts",
			check_in_id=checkin_id,
			status=MonitorStatus.ERROR,
		)
		raise

def activate_contracts_starting_today() -> list:
	checkin_id = capture_checkin(
		monitor_slug="activate_contracts_starting_today",
		status=MonitorStatus.IN_PROGRESS,
	)

	try:
		target_date = frappe.utils.nowdate()

		contracts = frappe.db.get_list(
			"Shop Contract",
			filters={
				"start_date": target_date,
				"workflow_state": "Approved",
			},
			fields=["name"],
		)

		for c in contracts:
			frappe.db.set_value(
				"Shop Contract",
				c.name,
				"workflow_state",
				"Active",
			)

		frappe.db.commit()

		capture_checkin(
			monitor_slug="activate_contracts_starting_today",
			check_in_id=checkin_id,
			status=MonitorStatus.OK,
		)

		return contracts

	except Exception:
		capture_checkin(
			monitor_slug="activate_contracts_starting_today",
			check_in_id=checkin_id,
			status=MonitorStatus.ERROR,
		)
		raise


def expire_contracts_ended_yesterday():
	checkin_id = capture_checkin(
		monitor_slug="expire_contracts_ended_yesterday",
		status=MonitorStatus.IN_PROGRESS,
	)

	try:
		today = frappe.utils.nowdate()

		frappe.db.sql(
			"""
			UPDATE `tabShop Contract`
			SET status = 'Expired'
			WHERE end_date < %s
			  AND status = 'Active'
			  AND docstatus = 1
			""",
			today,
		)
		frappe.db.commit()

		capture_checkin(
			monitor_slug="expire_contracts_ended_yesterday",
			check_in_id=checkin_id,
			status=MonitorStatus.OK,
		)

	except Exception:
		capture_checkin(
			monitor_slug="expire_contracts_ended_yesterday",
			check_in_id=checkin_id,
			status=MonitorStatus.ERROR,
		)
		raise
