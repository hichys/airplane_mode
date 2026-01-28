// Copyright (c) 2026, awad mohamed and contributors
// For license information, please see license.txt

//2- Ability to track how many shops a particular airport has
frappe.query_reports["Airport Shops"] = {
	"filters": [
		{
			fieldname: "airport",
			label: __("Airport"),
			fieldtype: "Link",
			options: "Airport",
			reqd: 0
		}
	]
};


