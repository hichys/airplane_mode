frappe.ui.form.on("Rent Payment", {
	onload(frm) {
		update_child_allocations(frm);
	},
	amount(frm) {
		update_child_allocations(frm);
		// frm.set_df_property("payment", "read_only", 1);
	},
	shop_contract(frm) {
		if (!frm.doc.shop_contract) return;

		frappe.db.get_value("Shop Contract", frm.doc.shop_contract, "amount").then((r) => {
			if (!r.message?.amount) {
				frappe.msgprint("Shop Contract has no amount.");
				return;
			}

			let amount = flt(r.message.amount);

			// If only one row exists
			let row = frm.doc.payment?.[0];

			if (row) {
				frappe.model.set_value(row.doctype, row.name, "total_amount", amount);
			}

			frm.refresh_field("payment");
		});
	},
});

function update_child_allocations(frm) {
	let paid = flt(frm.doc.amount);

	if (!frm.doc.payment || frm.doc.payment.length === 0) return;

	frm.doc.payment.forEach((row) => {
		let total = flt(row.total_amount); // make sure fieldname is correct

		let allocated = paid;
		let outstanding = total - allocated;

		if (outstanding < 0) outstanding = 0;

		frappe.model.set_value(row.doctype, row.name, "allocated_amount", allocated);
		frappe.model.set_value(row.doctype, row.name, "outstanding_amount", outstanding);
	});

	frm.refresh_field("payment");
}
// function init_date_picker(frm)
// {
//     if (!frm.is_new()) return;

//         const wrapper = frm.fields_dict['payment_for_month'].wrapper;

//         // التاريخ الحالي
//         const today = new Date();
//         const currentYear = today.getFullYear();
//         const currentMonth = String(today.getMonth() + 1).padStart(2, '0');

//         // القيمة الافتراضية (لو الحقول متعبية)
//         const value = frm.doc.payment_for_month && frm.doc.payment_for_month
//             ? `${frm.doc.payment_for_month}-${String(frm.doc.payment_for_month).padStart(2, '0')}`
//             : `${currentYear}-${currentMonth}`;

//         const pick_month_html = `
//             <div class="form-group">
//                 <label class="control-label">Select Month</label>
//                 <input type="month"
//                        id="rent_month_picker"
//                        class="form-control"
//                        min="${currentYear}-${currentMonth}"
//                        value="${value}"
//                        style="width: 200px">
//             </div>
//         `;

//         // رسم الـ HTML
//         $(wrapper).html(pick_month_html);

//         // إزالة أي listener سابق ثم إضافة واحد جديد
//         $(wrapper).off('change', '#rent_month_picker');
//         $(wrapper).on('change', '#rent_month_picker', function () {
//             const val = $(this).val(); // YYYY-MM
//             if (!val) return;

//             const [year, month] = val.split('-').map(Number);

//             frm.set_value('payment_for_month', month+"-"+year );

//             frm.refresh_field('payment_for_month');
//         });

// }
