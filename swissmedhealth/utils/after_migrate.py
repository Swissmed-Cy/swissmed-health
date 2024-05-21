import frappe

def set_default_print_format():
	# Set default print format for "Lead" to "Patient Form"
	frappe.make_property_setter(
			{
				"doctype_or_field": "DocType",
				"doctype": "Lead",
				"property": "default_print_format",
				"value": "Patient Form",
			}
		)