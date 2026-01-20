// Copyright (c) 2026, awad mohamed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Contract", {
    start_date(frm) {
        calculate_contract_period(frm);
    },

    end_date(frm) {
        calculate_contract_period(frm);
    },

    contract_period(frm) {
        calculate_end_date(frm);
    }
});

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
