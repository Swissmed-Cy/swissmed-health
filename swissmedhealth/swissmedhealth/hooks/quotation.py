import frappe
from frappe import _

@frappe.whitelist()
def create_therapy_plan(quotation_name):
    # Fetch the Sales Quotation document
    quotation = frappe.get_doc('Quotation', quotation_name)
    
    # Create a new Therapy Plan document
    therapy_plan = frappe.new_doc('Therapy Plan')
    
    # Map fields from Sales Quotation to Therapy Plan
    therapy_plan.patient = quotation.customer_name
    therapy_plan.start_date = quotation.transaction_date
    # therapy_plan.quotation = quotation_name
    
    # Example of mapping items (customize as needed)
    therapy_plan_details = []
    for item in quotation.items:
        print("::::::::::::::::::::",item.name)
        therapy_plan_details.append({
            'therapy_type': item.item_name,
            'name': item.item_name,
            'no_of_sessions': item.qty,
            # 'item_name': item.item_name,
            # 'qty': item.qty
        })
    therapy_plan.set("therapy_plan_details", therapy_plan_details)
    # therapy_plan.therapy_plan_details = therapy_plan_details
    
    # Insert the new Therapy Plan document into the database
    therapy_plan.save()
    frappe.db.commit()
    
    return therapy_plan.name