import frappe

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist(allow_guest=True)
def get_dental_history_details(email_id):
	lead = frappe.db.get_value("Lead", {"email_id": email_id}, ["custom_dental_history"], as_dict=True)
	# if empty lead throw error
	if not lead:
		frappe.throw("Not found")
	
	# get the dental history document from the lead
	dental_history = frappe.get_value("Dental History", lead.custom_dental_history, ["*"], as_dict=True)
	return dental_history

@frappe.whitelist(allow_guest=True)
def save(doc):
	# doc is in json format. Convert it to dict
	doc = frappe.parse_json(doc)
	# Get the lead from the doc.name assign all values from doc to lead and save
	lead = frappe.get_doc("Dental History", doc.name)
	lead.update(doc)
	lead.save(ignore_permissions=True)
	return lead