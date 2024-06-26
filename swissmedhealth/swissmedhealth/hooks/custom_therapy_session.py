import frappe
from frappe.utils import flt
from datetime import datetime

@frappe.whitelist()
def merge_therapy_sessions_to_invoice(therapy_sessions):
    if not therapy_sessions:
        frappe.throw("No Therapy Sessions provided")

    therapy_sessions = frappe.parse_json(therapy_sessions)
    print(":::::::::::therapy_sessions 1:::::::",therapy_sessions)
    
    patient = None
    merged_items = []
    total = 0

    for session_name in therapy_sessions:
        session_doc = frappe.get_doc("Therapy Session", session_name)
        print(":::::session_doc:::::",session_doc)
        print(":::::session_doc.therapy_type:::::",session_doc.therapy_type)
        therapy_type = frappe.get_doc("Therapy Type", session_doc.therapy_type)
        print(":::::session_doc.rate:::::",session_doc.rate)
        print(":::::therapy_type:::::",therapy_type)
        print ("::::::::therapy_type.item:::::::",therapy_type.item)
        if not patient:
            patient = session_doc.patient
        elif patient != session_doc.patient:
            frappe.throw("All selected Therapy Sessions must belong to the same patient")
        
        merged_items.append({
            'item_code': therapy_type.item,
            'rate': session_doc.rate,
            'qty': 1,  # Assuming 1 unit per session, adjust as needed
            'amount': flt(session_doc.rate)
        })
        total += flt(session_doc.rate)

        session_doc.invoice = 'Merged'
        session_doc.save()

    if not patient:
        frappe.throw("No valid Therapy Sessions found")

    customer = frappe.db.get_value("Patient", patient, "customer")
    new_invoice = frappe.get_doc({
        'doctype': 'Sales Invoice',
        'patient': patient,
        'customer': customer,
        # 'payment_terms_template': payment_term_name,
        'items': merged_items,
        'due_date': datetime.now().date()
    })
    new_invoice.insert()
    # new_invoice.submit()

    return new_invoice.name

