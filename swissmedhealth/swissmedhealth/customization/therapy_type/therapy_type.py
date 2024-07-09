import frappe
from healthcare.healthcare.doctype.therapy_type.therapy_type import TherapyType
from healthcare.healthcare.doctype.clinical_procedure_template.clinical_procedure_template import (
	make_item_price,
)


class CustomTherapyType(TherapyType):
	def after_insert(self):
		create_item_from_therapy(self)

def create_item_from_therapy(doc):
	disabled = doc.disabled
	if doc.is_billable and not doc.disabled:
		disabled = 0

	uom = frappe.db.exists("UOM", "Unit") or frappe.db.get_single_value("Stock Settings", "stock_uom")

	if frappe.db.exists("Item", doc.item_code):
		item = frappe.get_doc("Item", doc.item_code)
	else:
		item = frappe.get_doc(
			{
				"doctype": "Item",
				"item_code": doc.item_code,
				"item_name": doc.item_name,
				"item_group": doc.item_group,
				"description": doc.description,
				"is_sales_item": 1,
				"is_service_item": 1,
				"is_purchase_item": 0,
				"is_stock_item": 0,
				"show_in_website": 0,
				"is_pro_applicable": 0,
				"disabled": disabled,
				"stock_uom": uom,
			}
		).insert(ignore_permissions=True, ignore_mandatory=True)
		make_item_price(item.name, doc.rate)

	doc.db_set("item", item.name)