frappe.ui.form.on("Rent Payment", {
    refresh(frm) {
        // init_date_picker(frm);

    }
});


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