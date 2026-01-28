// Copyright (c) 2026, awad mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Contract", {
        refresh(frm) {
            frm.set_query('shop', () => {
                return {
                    filters: {
                        "docstatus": 1
                    }
                }
            })
            if (!frm.is_new() && frm.doc.docstatus === 1) {
                frm.add_custom_button(
                    __("Create Payment"),
                    () => {
                        frm.events.create_payment(frm);
                    },
                    __("Create")
                );
                frm.add_custom_button(
                    __("Create Sales Invoice"),
                    () => {
                        frm.events.create_sales_invoice(frm);
                    },
                    __("Create")
                );
            }
            else
            {
                //hide renewed contract field , it will show when contracted ended and it has renewed
                frm.set_df_property('renewed_contract','hidden',1 );
            }
        
    },
    onload(frm){
        frappe.db.get_single_value(
            "Shop Setting",
            "default_grace_days"
        ).then(value => {
            if(frm.is_new())
            {
                frm.set_value('grace_period',value * 24 * 60 * 60)
            }
        });
    },
    start_date(frm) {
        calculate_contract_period(frm);
        
    },

    end_date(frm) {
        calculate_contract_period(frm);
    },

    contract_period(frm) {
        calculate_end_date(frm);
    },
    shop: function(frm){
        
        if (!frm.doc.shop) return;

        frappe.db.get_value(
            "Shop",
            frm.doc.shop,
            ["rent_amount", "contract_period"]
        ).then(r => {
            if (r && r.message) {
                if(!frm.doc.amount){
                    frm.set_value("amount", r.message.rent_amount || 0);
                }
                if(!frm.doc.contract_period){
                    frm.set_value("contract_period", r.message.contract_period || 0);
                }
            }
        });
    
    },
    create_sales_invoice(frm) {
        frappe.model.with_doctype("Sales Invoice", () => {
            //TODO Figure this auto
            uom = "Unit"
            income_account = "4120 - Service - A"
            let si = frappe.model.get_new_doc("Sales Invoice");
    
            // Required core fields
            si.customer = frm.doc.tenant;
            si.posting_date = frappe.datetime.get_today();
    
            // Custom link field (add this in Sales Invoice)
            si.remarks = frm.doc.name;
            // Subscription Peroid = Shop contract peroid
            si.from_date = frm.doc.start_date;
            si.to_date = frm.doc.end_date;
            si.due_date = frm.doc.end_date
           
            // Add item row (VERY IMPORTANT)
            let item = frappe.model.add_child(si, "items");
    
            item.item_code = "Airport Shop Rent"; // Must exist as Item
            item.item_name = "Airport Shop Rent";
            item.qty = 1;
            item.rate = frm.doc.amount;
            item.uom = uom
            item.income_account = income_account
    
    
            // Let ERPNext calculate totals
            si.set_posting_time = 1;
    
            frappe.set_route("Form", "Sales Invoice", si.name);
        });
    },
    
})
function calculate_contract_period(frm) {
    if (frm._updating_contract) return;

    if (!frm.doc.start_date || !frm.doc.end_date) return;

    let start = moment(frm.doc.start_date);
    let end = moment(frm.doc.end_date);

    if (end.isBefore(start)) {
        frm.set_df_property(
            "contract_period",
            "description",
            "<span style='color:red'>End date must be after start date</span>"
        );
        frm.set_value("contract_period", null);
        return;
    }

    frm._updating_contract = true;

    let days = end.diff(start, "days") + 1;
    let months = end.diff(start, "months", true).toFixed(1);

    // Duration field expects SECONDS
    let duration_seconds = days * 24 * 60 * 60;

    frm.set_value("contract_period", duration_seconds);

    frm.set_df_property(
        "contract_period",
        "description",
        `
        <span style="color:blue">
            Contract duration: <b>${days}</b> days
            (~ <b>${months}</b> months)
        </span>
        `
    );

    frm._updating_contract = false;
}
function calculate_end_date(frm) {
    if (frm._updating_contract) return;
    if (!frm.doc.contract_period) return;

    frm._updating_contract = true;

    // إذا لم يتم اختيار تاريخ بداية
    if (!frm.doc.start_date) {
        frm.set_value("start_date", frappe.datetime.get_today());
    }

    let start = moment(frm.doc.start_date);

    // Duration بالثواني
    let days = frm.doc.contract_period / (24 * 60 * 60);

    let end_date = start.add(days - 1, "days").format("YYYY-MM-DD");

    frm.set_value("end_date", end_date);

    frm._updating_contract = false;
}