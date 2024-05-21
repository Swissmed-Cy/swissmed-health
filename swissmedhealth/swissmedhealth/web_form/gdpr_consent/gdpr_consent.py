import frappe

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist(allow_guest=True)
def get_customer_consent_details(email_id):
	lead = frappe.db.get_value("Lead", {"email_id": email_id}, ["custom_customer_consent"], as_dict=True)
	# if empty lead throw error
	if not lead:
		frappe.throw("Not found")
	
	# get the dental history document from the lead
	customer_consent = frappe.get_value("Customer Consent", lead.custom_customer_consent, ["*"], as_dict=True)
	return customer_consent

@frappe.whitelist(allow_guest=True)
def save(doc):
	# doc is in json format. Convert it to dict
	doc = frappe.parse_json(doc)
	# Get the lead from the doc.name assign all values from doc to lead and save
	lead = frappe.get_doc("Customer Consent", doc.name)
	lead.update(doc)
	lead.save(ignore_permissions=True)
	return lead