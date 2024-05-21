import frappe

from erpnext.crm.doctype.lead.lead import Lead as OriginalLead

class Lead(OriginalLead):
    def create_contact(self):
        if not self.lead_name:
            self.set_full_name()
            self.set_lead_name()

        if self.custom_relative_first_name:
            contact = frappe.new_doc("Contact")
            contact.update(
                {
                    "first_name": self.custom_relative_first_name,
                    "last_name": self.custom_relative_last_name,
                    "salutation": self.custom_relative_salutation,
                    "gender": self.custom_relative_gender,
                    "is_primary_contact": 0,
                    "custom_relation": self.custom_relation,
                }
            )

            if self.custom_relative_email_id:
                contact.append("email_ids", {"email_id": self.custom_relative_email_id, "is_primary": 1})

            if self.custom_relative_phone:
                contact.append("phone_nos", {"phone": self.custom_relative_phone, "is_primary_phone": 1})


            contact.insert(ignore_permissions=True)
            contact.reload()  # load changes by hooks on contact
            self.relative_contact_doc = contact
        else:
            self.relative_contact_doc = None

        # call the original method
        contact = super(Lead, self).create_contact()
        contact.is_primary_contact = 1
        contact.save()
        return contact
    
    def link_to_contact(self):
        # call the original method
        super(Lead, self).link_to_contact()

        if self.relative_contact_doc:
            self.relative_contact_doc.append(
				"links", {"link_doctype": "Lead", "link_name": self.name, "link_title": self.lead_name}
			)
            self.relative_contact_doc.save()

def after_insert(doc, method):
    medical_history = frappe.new_doc("Medical History")
    medical_history.insert(ignore_permissions=True)
    doc.db_set('custom_medical_history', medical_history.name)

    dental_history = frappe.new_doc("Dental History")
    dental_history.insert(ignore_permissions=True)
    doc.db_set('custom_dental_history', dental_history.name)

    customer_consent = frappe.new_doc("Customer Consent")
    customer_consent.insert(ignore_permissions=True)
    doc.db_set('custom_customer_consent', customer_consent.name)

    doc.reload()

# Hook: before delete
def after_delete(doc, method):
    # if custom_dental_history is not empty
    if doc.get('custom_dental_history'):
        # delete the dental history document
        frappe.delete_doc("Dental History", doc.get('custom_dental_history'))
    # if custom_customer_consent is not empty
    if doc.get('custom_customer_consent'):
        # delete the customer consent document
        frappe.delete_doc("Customer Consent", doc.get('custom_customer_consent'))
    if doc.get('custom_medical_history'):
        # delete the customer consent document
        frappe.delete_doc("Medical History", doc.get('custom_medical_history'))
