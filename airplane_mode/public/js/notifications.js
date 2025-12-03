frappe.realtime.on("custom_notification", (data) => {
    frappe.show_alert({message: data.message, indicator: 'green'}, 5);
    console.log(data);
});
frappe.realtime.on('global_notification', (data) => {
    if (data.title && data.content) {
        frappe.desk.show_alert({
            message: data.content,
            title: data.title,
            indicator: 'info'
        });
        frappe.utils.play_sound("email"); // Optional sound effect
    }
});