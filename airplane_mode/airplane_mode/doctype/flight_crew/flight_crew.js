// Copyright (c) 2025, awad mohamed and contributors
// For license information, please see license.txt
frappe.ui.form.on("Flight Crew", {
    airline: function(frm) {
        // Clear flight when airline changes
        frm.set_value('flight', '');

        // Filter Flight field by selected airline via Airplane
        frm.set_query('flight', function() {
            if (frm.doc.airline) {
                return {
                    query: "frappe.desk.search.search_link",
                    filters: {
                        doctype: "Flight",
                        filters: [
                            ["airplane.airline", "=", frm.doc.airline]
                        ]
                    }
                };
            } else {
                return {};
            }
        });
    }
});
