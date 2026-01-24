import frappe

def trigger_bell_notification(doctype,docname,recipient, message, subject="New Update"):
    # Create a new Notification Log entry
    notification = frappe.new_doc("Notification Log")
    notification.for_user = recipient         # User ID (email) of the receiver
    notification.subject = subject            # Short text shown in the list
    notification.email_content = message      # Full message (supports HTML/Markdown)
    notification.type = "Alert"                # General type
    
    # Optional: Link to a specific document so clicking the notification opens it
    notification.document_type = doctype
    notification.document_name = docname
    
    notification.insert(ignore_permissions=True)