// Copyright (c) 2026, awad mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Lead", {
	refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(
                __("Shop Contract"),
                () => {
                    frappe.model.open_mapped_doc({
                        method: "airplane_mode.airport_shop.doctype.shop_lead.shop_lead.make_contract",
                        frm: frm
                    });
                }
            ,"Create");
        }
	},
});
