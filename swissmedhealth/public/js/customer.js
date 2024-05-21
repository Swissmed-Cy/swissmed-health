frappe.ui.form.on('Customer', {
    refresh: function (frm) {

        let doc = frm.doc;

        // Get patient linked with customer
        let patient = frappe.get_doc("Patient", { "customer": doc.name });

        // If the lead is saved, then add the button to create a patient
        if (!frm.is_new() && doc.__onload && patient == null && doc.lead_name) {
            frm.add_custom_button(__('Create Patient'), function () {
                frappe.model.open_mapped_doc({
                    method: "swissmedhealth.swissmedhealth.hooks.customer.make_patient",
                    frm: frm
                });
            }).addClass('btn-primary');
        }
    },
});
