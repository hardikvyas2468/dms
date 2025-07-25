import frappe


def execute():
    all_entities = frappe.db.get_list("DMS File", fields=["name", "title", "owner", "creation"])

    for i in all_entities:
        doc = frappe.new_doc("DMS Entity Activity Log")
        doc.entity = i.name
        doc.action_type = "create"
        doc.message = f"Created {i.title}"
        doc.save()
        frappe.db.set_value("DMS Entity Activity Log", doc.name, "owner", i.owner)
        frappe.db.set_value("DMS Entity Activity Log", doc.name, "creation", i.creation)
