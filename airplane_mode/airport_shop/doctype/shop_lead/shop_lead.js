// Copyright (c) 2026, awad mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Lead", {
	refresh(frm) {
        frm.clear_custom_buttons();
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
        if(frm.doc.docstatus === 1 && frm.doc.status === "Converted"){
            //TODO Server Validation !!
            if(!frm.doc._is_locked  )
            {
                frm.add_custom_button(
                    __("Lock"),
                    () => {
                        frm.set_df_property("status","read_only",1);
                        frm.set_df_property("note","read_only",1)
                        frm.set_value("_is_locked",1);
                        frm.save()
                    }
                )
            }
            else
            {
                frm.add_custom_button(
                    __("unLock"),
                    () => {
                        frm.set_df_property("status","read_only",0);
                        frm.set_df_property("note","read_only",0)
                        frm.set_value("_is_locked",0);
                        frm.save()
                    }
                )
            }
        }
	},
});
