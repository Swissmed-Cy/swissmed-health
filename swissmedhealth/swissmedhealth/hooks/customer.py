import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_patient(source_name, target_doc=None):
	return _make_patient(source_name, target_doc)

def _make_patient(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		# Get customer document from source_name
		customer = frappe.get_doc("Customer", source_name)
		target.first_name = customer.salutation+" "+target.first_name
		target.customer_group = customer.customer_group
		target.territory = customer.territory
		target.customer = customer.name
		target.default_price_list = customer.default_price_list
		target.default_currency = customer.default_currency
		target.customer_group = frappe.db.get_default("Customer Group")
		
    # Get the lead_name of the customer
	lead_name = frappe.db.get_value("Customer", source_name, "lead_name")

	doclist = get_mapped_doc(
		"Lead",
		lead_name,
		{
			"Lead": {
				"doctype": "Patient",
				"field_map": {
					"name": "lead_name",
					"first_name": "first_name",
					"middle_name": "middle_name",
					"last_name": "last_name",
					"gender": "sex",        
					"custom_dob": "dob",           
				},
				"field_no_map": ["disabled"],
			}
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	return doclist

def before_insert(doc, method):
	if doc.lead_name:
		# Get the custom_sales_partner and custom_commision_rate from the lead
		doc.default_sales_partner = frappe.db.get_value("Lead", doc.lead_name, "custom_sales_partner")
		doc.default_commission_rate = frappe.db.get_value("Lead", doc.lead_name, "custom_commission_rate")
			