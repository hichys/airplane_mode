// Copyright (c) 2026, awad mohamed and contributors
// For license information, please see license.txt

async function get_default_rent_amount() {
    const default_rent_amount = await frappe.db.get_single_value("Shop Setting", "default_rent_amount");
    return default_rent_amount;
}
function generate_random_shop_number(frm)
{
    b_generate = frm.add_custom_button(__("Generate Shop Number"), function() {
        frappe.call(
            {
                method:"airplane_mode.api.get_random_shop_number",
                callback: function(r)
                {
                    if(r.message)
                    {
                        frm.set_value("shop_number",r.message)
                        frm.refresh_field('shop_number');
                    }
                }
            }
        )
    });

    

    return b_generate
}
frappe.ui.form.on("Shop", {
    async refresh(frm) {
        if (frm.doc.rent_amount === 0 && frm.is_new()) {
            const default_rent_amount = await get_default_rent_amount();
            frm.set_value("rent_amount", default_rent_amount);
        }
        
        frm.set_query('shop_type', () => {
            return {
                filters: {
                    enabled: 1
                }
            }
        })
        // if(frm.doc.shop_number)
        
    },
    shop_number: function(frm) {
        if (!frm.doc.shop_number){
            frm.set_df_property(
                'shop_number',
                'description',
                '<span style="color:blue"></span>'
            );
            generate_button = generate_random_shop_number(frm)
        }
        // Call server-side API
        frappe.call({
            method: "airplane_mode.api.is_shop_number_exits",
            args: { new_shop_number: frm.doc.shop_number },
            callback: function(r) {
                if (r.message) {
                    // Number exists
                    frm.set_df_property(
                        'shop_number',
                        'description',
                        '<span style="color:red">⚠ Shop Number already exists!</span>'
                    );
                    generate_random_shop_number(frm)
                } else {
                    // Number available
                    frm.set_df_property(
                        'shop_number',
                        'description',
                        '<span style="color:green">✔ Shop Number is available</span>'
                    );
                    frm.remove_custom_button('Generate Shop Number');

                }
                frm.refresh_field('shop_number');
            }
        });
    
},
    
    async onload(frm) {
        
        // frappe.msgprint("on_load");
        // get the default Rent Amount 
        get_default_rent_amount().then(result => {
            if(frm.is_new())
            {
                frm.set_value("rent_amount", result);
            }
        });

        if(!frm.doc.shop_number && frm.is_new())
        frappe.call({
            method: "airplane_mode.api.get_random_shop_number",
            callback: function(r) {
                if (r.message) {
                        frm.set_value("shop_number", r.message);
                }
            }
        });
       
    },
    
});
