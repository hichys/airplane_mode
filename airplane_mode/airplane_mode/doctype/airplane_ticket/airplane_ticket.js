frappe.ui.form.on("Airplane Ticket", {
    async validate(frm) {

        // 1. Validate airplane capacity BEFORE saving
        let r = await frappe.call({
            method: "airplane_mode.api.is_airplane_full",
            args: { flight: frm.doc.flight }
        });

        if (r.message === true) {
            frappe.throw("Airplane flight capacity is exceeded");
        }

        // 2. Calculate total amount
        const addons_total = frm.doc.items?.reduce((acc, item) => acc + item.amount, 0) || 0;
        const flight_price = frm.doc.flight_price || 0;

        frm.doc.total_amount = addons_total + flight_price;

        // 3. Prevent duplicate items
        let items = frm.doc.items.map(i => i.item);
        if (items.length !== new Set(items).size) {
            frappe.throw("Add-ons items can't be duplicated");
        }
    },

    refresh(frm) {
        frm.add_custom_button("Set Seat", function () {
            let d = new frappe.ui.Dialog({
                title: 'Enter Seat Number',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1
                    },
                ],
                primary_action_label: "Submit",
                primary_action(values) {
                    frm.set_value("seat", values.seat_number);
                    d.hide();
                }
            });
            d.show();
        }, "Actions");
    },

    update_total_amount(frm) {
        let addons_total = frm.doc.items.reduce((acc, item) => acc + item.amount, 0);
        frm.set_value("total_amount", addons_total + frm.doc.flight_price);
    }
});

frappe.ui.form.on("Airplane Ticket Add-on Item", {

    item(frm, cdt, cdn) {
        let current = locals[cdt][cdn];
        let items = frm.doc.items.map(i => i.item);

        if (items.filter(i => i === current.item).length > 1) {
            frappe.model.clear_doc(cdt, cdn);
            frm.refresh_field("items");
            frappe.msgprint({
                title: "Duplicate Item",
                message: `"${current.item}" is already added.`,
                indicator: "red"
            });
        }
    },

    amount(frm) {
        frm.trigger("update_total_amount");
    },

    items_remove(frm) {
        frm.trigger("update_total_amount");
    }
});
