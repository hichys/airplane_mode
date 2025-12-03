import frappe

def hourly():
    # persistent Desk notification

    # real-time popup for online users
    frappe.publish_realtime(
        event="custom_notification",
        message="Hourly job completed!",
        user=frappe.session.user
    )


def everyday():
    frappe.publish_realtime(
        event="global_notification",
        message={
            "title": "Daily Notification",
            "content": "This is a scheduled alert."
        },
        user="Administrator",
        after_commit=True # Using after_commit=True is often safer in scheduled jobs
    )
    frappe.logger().error("Daily job ran successfully")
