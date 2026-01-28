import frappe
from sentry_sdk.crons import capture_checkin
from sentry_sdk.crons.consts import MonitorStatus


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
